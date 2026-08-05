import { useState } from "react";
import { SendHorizontal } from "lucide-react";

function Input({ onSend }) {

    const [question, setQuestion] = useState("");

    const handleSend = () => {

        if (!question.trim()) return;

        onSend(question);

        setQuestion("");

    };

    const handleKeyDown = (e) => {

        if (e.key === "Enter") {

            handleSend();

        }

    };

    return (

        <div className="border-t border-zinc-800 p-3 flex gap-2">

            <input

                type="text"

                placeholder="Ask anything..."

                value={question}

                onChange={(e) => setQuestion(e.target.value)}

                onKeyDown={handleKeyDown}

                className="flex-1 bg-zinc-900 rounded-lg px-4 py-2 outline-none"

            />

            <button

                onClick={handleSend}

                className="bg-blue-600 hover:bg-blue-700 transition p-3 rounded-lg"

            >

                <SendHorizontal size={18} />

            </button>

        </div>

    );

}

export default Input;