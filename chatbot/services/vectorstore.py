import os
import sys

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FastEmbedEmbeddings


embeddings = None


def get_embeddings():

    global embeddings

    if embeddings is None:

        print("Loading FastEmbed...", file=sys.stderr)

        embeddings = FastEmbedEmbeddings()

        print("FastEmbed Loaded", file=sys.stderr)

    return embeddings


def create_retriever(text, video_id):

    print("Creating Retriever...", file=sys.stderr)

    folder_path = os.path.join("vectorstore", video_id)

    os.makedirs("vectorstore", exist_ok=True)

    embedding_model = get_embeddings()

    if os.path.exists(folder_path):

        print("Loading Existing VectorStore...", file=sys.stderr)

        vector_store = FAISS.load_local(
            folder_path,
            embedding_model,
            allow_dangerous_deserialization=True
        )

    else:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = splitter.create_documents([text])

        print(f"Chunks : {len(docs)}", file=sys.stderr)

        vector_store = FAISS.from_documents(
            docs,
            embedding_model
        )

        vector_store.save_local(folder_path)

    print("Retriever Ready", file=sys.stderr)

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k":4}
    )