function Message({ sender, text }) {

    const isUser = sender === "user";

    return (

        <div

            className={`flex ${isUser ? "justify-end" : "justify-start"}`}

        >

            <div

                className={`

                    max-w-[85%]

                    px-4

                    py-3

                    rounded-xl

                    whitespace-pre-wrap

                    break-words

                    ${

                        isUser

                        ?

                        "bg-blue-600"

                        :

                        "bg-zinc-800"

                    }

                `}

            >

                {text}

            </div>

        </div>

    );

}

export default Message;