import ReactMarkdown from "react-markdown";

function Message({ sender, text }) {

    const isUser = sender === "user";

    const copyText = () => {

        navigator.clipboard.writeText(text);

    };

    return (

        <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>

            <div
                className={`
                    max-w-[85%]
                    rounded-2xl
                    px-4
                    py-3
                    shadow-md
                    ${
                        isUser
                            ? "bg-blue-600 text-white rounded-br-sm"
                            : "bg-zinc-900 border border-zinc-800 rounded-bl-sm"
                    }
                `}
            >

                <div className="prose prose-invert prose-sm max-w-none">

                    <ReactMarkdown>

                        {text}

                    </ReactMarkdown>

                </div>

                {

                    !isUser && (

                        <button

                            onClick={copyText}

                            className="mt-3 text-xs text-zinc-400 hover:text-white"

                        >

                            Copy

                        </button>

                    )

                }

            </div>

        </div>

    );

}

export default Message;