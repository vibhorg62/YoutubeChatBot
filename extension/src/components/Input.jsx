import { useState } from "react";
import { SendHorizontal } from "lucide-react";

function Input({ onSend, loading }) {

    const [question, setQuestion] = useState("");

    const handleSend = () => {

        if (!question.trim() || loading) return;

        onSend(question);

        setQuestion("");

    };

    const handleKeyDown = (e) => {

        if (e.key === "Enter" && !e.shiftKey) {

            e.preventDefault();

            handleSend();

        }

    };

    return (

        <div className="border-t border-zinc-800 bg-zinc-950 p-4">

            <div className="flex items-end gap-3 bg-zinc-900 border border-zinc-700 rounded-2xl px-4 py-3">

                <textarea

                    rows={1}

                    placeholder="Ask anything about this video..."

                    value={question}

                    onChange={(e) => setQuestion(e.target.value)}

                    onKeyDown={handleKeyDown}

                    className="
                        flex-1
                        bg-transparent
                        resize-none
                        outline-none
                        text-sm
                        text-white
                        placeholder:text-zinc-500
                        max-h-32
                    "

                />

                <button

                    onClick={handleSend}

                    disabled={loading}

                    className="
                        bg-blue-600
                        hover:bg-blue-700
                        disabled:bg-zinc-700
                        disabled:cursor-not-allowed
                        p-3
                        rounded-xl
                        transition
                    "

                >

                    <SendHorizontal size={18} />

                </button>

            </div>

        </div>

    );

}

export default Input;