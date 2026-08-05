import json
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from utils.youtube import extract_video_id
from services.transcript import get_transcript
from services.vectorstore import create_retriever
from services.rag import build_chain

# ---------------- CACHE ---------------- #

retriever_cache = {}
chain_cache = {}

# --------------------------------------- #


def ask_question(video_url, question):

    video_id = extract_video_id(video_url)

    if not video_id:
        return "Invalid YouTube URL."

    # ---------- Retriever ---------- #

    if video_id in retriever_cache:

        print(f"Using Cached Retriever : {video_id}", file=sys.stderr)

        retriever = retriever_cache[video_id]

    else:

        print(f"Creating Retriever : {video_id}", file=sys.stderr)

        text = get_transcript(video_id)

        retriever = create_retriever(
            text=text,
            video_id=video_id
        )

        retriever_cache[video_id] = retriever

    # ---------- Chain ---------- #

    if video_id in chain_cache:

        chain = chain_cache[video_id]

    else:

        chain = build_chain(retriever)

        chain_cache[video_id] = chain

    return chain.invoke(question)


# ---------------- Worker ---------------- #

while True:

    try:

        line = input()

        if not line.strip():
            continue

        request = json.loads(line)

        answer = ask_question(
            request["url"],
            request["question"]
        )

        # ONLY JSON ON STDOUT
        print(
            json.dumps({
                "answer": answer
            }),
            flush=True
        )

    except EOFError:
        break

    except Exception as e:

        print(
            json.dumps({
                "error": str(e)
            }),
            flush=True
        )