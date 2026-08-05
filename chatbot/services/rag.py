from langchain_groq import ChatGroq

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)

from langchain_core.output_parsers import StrOutputParser


def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


def convert_history(history):

    messages = []

    for msg in history:

        if msg["role"] == "user":

            messages.append(
                HumanMessage(
                    content=msg["content"]
                )
            )

        else:

            messages.append(
                AIMessage(
                    content=msg["content"]
                )
            )

    return messages


def build_chain(retriever, history):

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages(

        [

            (

                "system",

                """
You are a helpful AI assistant.

Use ONLY the transcript context to answer the user's question.

Conversation history is only for understanding follow-up questions.

Never invent facts.

If the answer cannot be found inside the transcript, reply exactly:

I don't know based on the provided transcript.
"""

            ),

            MessagesPlaceholder(
                variable_name="history"
            ),

            (

                "human",

                """
Transcript Context:

{context}


Question:

{question}
"""

            )

        ]

    )

    parser = StrOutputParser()

    chain = (

        RunnableParallel(

            {

                "context":

                    retriever
                    | RunnableLambda(format_docs),

                "question":

                    RunnablePassthrough(),

                "history":

                    RunnableLambda(
                        lambda _:
                        convert_history(history)
                    )

            }

        )

        | prompt

        | llm

        | parser

    )

    return chain