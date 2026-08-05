import os
import sys
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME
)


def create_retriever(text, video_id):

    folder_path = os.path.join("vectorstore", video_id)

    if os.path.exists(folder_path):

        print("Loading Existing VectorStore...", file=sys.stderr)

        vector_store = FAISS.load_local(
            folder_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

    else:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = splitter.create_documents([text])

        vector_store = FAISS.from_documents(
            docs,
            embeddings
        )

        vector_store.save_local(folder_path)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k":4}
    )

    return retriever