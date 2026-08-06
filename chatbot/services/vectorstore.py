import os
import sys

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Lazy Loading
embeddings = None


def get_embeddings():

    global embeddings

    if embeddings is None:

        print("Loading Embedding Model...", file=sys.stderr)

        embeddings = HuggingFaceEmbeddings(
            model_name=MODEL_NAME
        )

        print("Embedding Model Loaded", file=sys.stderr)

    return embeddings


def create_retriever(text, video_id):

    print("A. create_retriever()", file=sys.stderr)

    # Create parent directory
    os.makedirs("vectorstore", exist_ok=True)

    folder_path = os.path.join("vectorstore", video_id)

    print(f"VectorStore Path : {folder_path}", file=sys.stderr)

    # Load embedding model only when needed
    embedding_model = get_embeddings()

    # ---------------- LOAD ---------------- #

    if os.path.exists(folder_path):

        print("B. Loading Existing VectorStore...", file=sys.stderr)

        vector_store = FAISS.load_local(
            folder_path,
            embedding_model,
            allow_dangerous_deserialization=True
        )

        print("C. Existing VectorStore Loaded", file=sys.stderr)

    # ---------------- CREATE ---------------- #

    else:

        print("D. Splitting Transcript...", file=sys.stderr)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = splitter.create_documents([text])

        print(f"E. Total Chunks : {len(docs)}", file=sys.stderr)

        print("F. Creating FAISS...", file=sys.stderr)

        vector_store = FAISS.from_documents(
            docs,
            embedding_model
        )

        print("G. FAISS Created", file=sys.stderr)

        print("H. Saving VectorStore...", file=sys.stderr)

        vector_store.save_local(folder_path)

        print("I. VectorStore Saved", file=sys.stderr)

    # ---------------- RETRIEVER ---------------- #

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    print("J. Retriever Ready", file=sys.stderr)

    return retriever