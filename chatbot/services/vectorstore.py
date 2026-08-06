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

    # ---------------- LOAD ---------------- #

    if os.path.exists(folder_path):

        print("Loading Existing VectorStore...", file=sys.stderr)

        vector_store = FAISS.load_local(
            folder_path,
            embedding_model,
            allow_dangerous_deserialization=True
        )

        print("Existing VectorStore Loaded", file=sys.stderr)

    # ---------------- CREATE ---------------- #

    else:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000,
            chunk_overlap=200
        )

        docs = splitter.create_documents([text])

        print(f"Chunks : {len(docs)}", file=sys.stderr)

        texts = [doc.page_content for doc in docs]

        vectors = []

        print("1. Generating Embeddings...", file=sys.stderr)

        for i, txt in enumerate(texts):

            print(f"Embedding {i+1}/{len(texts)}", file=sys.stderr)

            vec = embedding_model.embed_documents([txt])

            vectors.extend(vec)

        print("2. Embeddings Generated", file=sys.stderr)

        print("3. Creating FAISS...", file=sys.stderr)

        vector_store = FAISS.from_embeddings(
            text_embeddings=list(zip(texts, vectors)),
            embedding=embedding_model
        )

        print("4. FAISS Created", file=sys.stderr)

        print("5. Saving VectorStore...", file=sys.stderr)

        vector_store.save_local(folder_path)

        print("6. VectorStore Saved", file=sys.stderr)

    print("Retriever Ready", file=sys.stderr)

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )