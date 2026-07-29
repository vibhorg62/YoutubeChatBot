import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate

load_dotenv()

#<----------------------------------------------------------- STEP - 1 ---------------------------------------------------------------------->

# indexing(Document Ingestion)

video_id = "Gfr50f6ZBvo" # youtube video ki id dalna hoga yahan pe

try:
    ytt_api = YouTubeTranscriptApi()

    transcript = ytt_api.fetch(video_id)

    text = " ".join(chunk.text for chunk in transcript)

    # print(text[:500])      
    # print(f"\nLength: {len(text)}")

except TranscriptsDisabled:
    print("No captions available for this video.")

except Exception as e:
    print(e)
    

# indexing (Text Splitting)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = text_splitter.create_documents([text])

# print(f"Total Chunks: {len(docs)}")
# print(docs[0].page_content[:300])


# indexing (Embedding and Vector Stores)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vector_store = FAISS.from_documents(
    documents=docs,
    embedding=embeddings
)

#print("Vector Store Created Successfully")

#<----------------------------------------------------------------- STEP - 2 --------------------------------------------------------->

# Retreival

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# query = "What is this video about?"

# docs = retriever.invoke(query)

# print(f"Retrieved {len(docs)} chunks\n")

# for i, doc in enumerate(docs):
#     print(f"Chunk {i+1}")
#     print(doc.page_content[:300])
#     print("-"*50)


#<------------------------------------------------------------------ STEP - 3 ----------------------------------------------------------->

# Augmentation

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant.

Use ONLY the provided transcript context to answer the question.

If the context contains partial information, answer using that information.

Only say "I don't know based on the provided transcript." if the context contains absolutely no relevant information.

Context:
{context}

Question:
{question}

Answer:
""")

# question = "What topics are discussed in this podcast?"

# retrieved_docs = retriever.invoke(question)

# context = "\n\n".join(doc.page_content for doc in retrieved_docs)

# # print(prompt.format(
# #     context=context,
# #     question=question
# # ))

#<----------------------------------------------------------------------- STEP - 4 ------------------------------------------------------------------------>

#Generation

from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


parallel_chain = RunnableParallel(
    {
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    }
)

parser = StrOutputParser()

main_chain = (
    parallel_chain
    | prompt
    | llm
    | parser
)

def ask_question(question):
    return main_chain.invoke(question)

while True:
    question = input("\nYou : ")

    if question.lower() == "exit":
        break

    answer = ask_question(question)

    print("\nBot :", answer)