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

    video_id = extract_video_id(video_url)

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

        print(
            f"Using Cached Retriever : {video_id}",
            file=sys.stderr
        )

        retriever = retriever_cache[video_id]

    else:

        print(
            f"Creating Retriever : {video_id}",
            file=sys.stderr
        )

        text = get_transcript(video_id)
        text = clean_text(text)

        retriever = create_retriever(
            text=text,
            video_id=video_id
        )

        retriever_cache[video_id] = retriever

    # ---------- Chain ---------- #

    chain = build_chain(
        retriever,
        cleaned_history
    )

    answer = chain.invoke(question)

    return clean_text(str(answer))


# ---------------- Worker ---------------- #

while True:

    try:

        line = input()

        if not line.strip():
            continue

        request = json.loads(line)

        url = request["url"]
        question = request["question"]
        history = request.get("history", [])

        answer = ask_question(
            url,
            question,
            history
        )

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

        print(
            json.dumps(
                {
                    "error": err_msg
                },
                ensure_ascii=False
            ),
            flush=True
        )