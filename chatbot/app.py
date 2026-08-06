import json
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.stdin.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

from utils.youtube import extract_video_id
from services.transcript import get_transcript
from services.vectorstore import create_retriever
from services.rag import build_chain


# ---------------- CACHE ---------------- #

retriever_cache = {}

# --------------------------------------- #


def clean_text(text):
    if isinstance(text, str):
        return text.encode("utf-8", "replace").decode("utf-8")
    return text


def ask_question(video_url, question, history):

    print("1. ask_question()", file=sys.stderr)

    video_id = extract_video_id(video_url)

    print(f"2. Video ID : {video_id}", file=sys.stderr)

    if not video_id:
        return "Invalid YouTube URL."

    question = clean_text(question)

    cleaned_history = []

    for item in history:

        cleaned_history.append({
            "role": clean_text(item.get("role", "")),
            "content": clean_text(item.get("content", ""))
        })

    # ---------- Retriever ---------- #

    if video_id in retriever_cache:

        print("3. Using Cached Retriever", file=sys.stderr)

        retriever = retriever_cache[video_id]

    else:

        print("4. Fetching Transcript...", file=sys.stderr)

        # ✅ Supadata uses full YouTube URL
        text = get_transcript(video_url)

        print("5. Transcript Fetched", file=sys.stderr)

        text = clean_text(text)

        print("6. Creating Retriever...", file=sys.stderr)

        retriever = create_retriever(
            text=text,
            video_id=video_id
        )

        print("7. Retriever Created", file=sys.stderr)

        retriever_cache[video_id] = retriever

    # ---------- Chain ---------- #

    print("8. Building Chain...", file=sys.stderr)

    chain = build_chain(
        retriever,
        cleaned_history
    )

    print("9. Chain Built", file=sys.stderr)

    print("10. Calling LLM...", file=sys.stderr)

    answer = chain.invoke(question)

    print("11. LLM Finished", file=sys.stderr)

    answer = clean_text(str(answer))

    print("12. Returning Answer", file=sys.stderr)

    return answer


# ---------------- Worker ---------------- #

print("✅ Python Worker Started", file=sys.stderr)

while True:

    try:

        line = input()

        if not line.strip():
            continue

        print("📩 Request Received From Node", file=sys.stderr)

        request = json.loads(line)

        url = request["url"]
        question = request["question"]
        history = request.get("history", [])

        answer = ask_question(
            url,
            question,
            history
        )

        print("📤 Sending Response To Node", file=sys.stderr)

        print(
            json.dumps(
                {
                    "answer": answer
                },
                ensure_ascii=False
            ),
            flush=True
        )

    except EOFError:
        break

    except Exception as e:

        err_msg = clean_text(str(e))

        print("❌ Exception :", err_msg, file=sys.stderr)

        print(
            json.dumps(
                {
                    "error": err_msg
                },
                ensure_ascii=False
            ),
            flush=True
        )