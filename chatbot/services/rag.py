from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)

from langchain_core.output_parsers import StrOutputParser


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_chain(retriever):

    # LLM ko yahin initialize karo
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant.

Use ONLY the provided transcript context to answer the user's question.

If the transcript is in Hindi or any other language, first understand it and then answer in clear, fluent English.

Do not invent facts that are not present in the transcript.

If the answer cannot be found in the transcript, reply:
"I don't know based on the provided transcript."

Context:
{context}

Question:
{question}

Answer:
""")

    parser = StrOutputParser()

    parallel_chain = RunnableParallel(
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        }
    )

    chain = (
        parallel_chain
        | prompt
        | llm
        | parser
    )

    return chain