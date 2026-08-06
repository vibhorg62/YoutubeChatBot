import { useEffect, useRef, useState } from "react";
import Input from "./Input";
import Message from "./Message";
import Loader from "./Loader";

function ChatBot() {

    const [messages, setMessages] = useState([
        {
            sender: "bot",
            text: "Hi! Ask anything related to this video."
        }
    ]);

    const [loading, setLoading] = useState(false);

    const [videoUrl, setVideoUrl] = useState("");

    const [videoTitle, setVideoTitle] = useState("");

    const chatRef = useRef(null);

    useEffect(() => {

        chrome.tabs.query(
            {
                active: true,
                currentWindow: true
            },
            (tabs) => {

                if (!tabs.length) return;

                setVideoUrl(tabs[0].url);

                setVideoTitle(tabs[0].title);

            }
        );

    }, []);

    useEffect(() => {

        chatRef.current?.scrollTo({
            top: chatRef.current.scrollHeight,
            behavior: "smooth"
        });

    }, [messages, loading]);



    const sendMessage = async (question) => {

        if (!question.trim()) return;

        setMessages(prev => [
            ...prev,
            {
                sender: "user",
                text: question
            }
        ]);

        setLoading(true);

        try {

            const response = await fetch(
                "https://youtube-ai-chat.onrender.com/api/chat",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        url: videoUrl,
                        question
                    })
                }
            );

            if (!response.ok) {
                throw new Error("Server Error");
            }

            const data = await response.json();

            setMessages(prev => [
                ...prev,
                {
                    sender: "bot",
                    text: data.data || "No response."
                }
            ]);

        }

        catch (err) {

            setMessages(prev => [
                ...prev,
                {
                    sender: "bot",
                    text: err.message
                }
            ]);

        }

        finally {

            setLoading(false);

        }

    };



    return (

        <div className="flex flex-col h-screen bg-zinc-950 text-white">

            {/* Header */}

            {/* Current Video */}

            <div className="px-4 py-3">

                <div className="bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3">

                    <p className="text-xs text-zinc-500">

                        Current Video

                    </p>

                    <p className="mt-1 text-sm font-medium truncate">

                        {videoTitle || "Open any YouTube Video"}

                    </p>

                </div>

            </div>

            {/* Chat */}

            <div
                ref={chatRef}
                className="flex-1 overflow-y-auto px-4 pb-4"
            >

                <div className="space-y-4">

                    {

                        messages.map((msg, index) => (

                            <Message
                                key={index}
                                sender={msg.sender}
                                text={msg.text}
                            />

                        ))

                    }

                    {

                        loading && <Loader />

                    }

                </div>

            </div>

            {/* Input */}

            <Input
                onSend={sendMessage}
                loading={loading}
            />

        </div>

    );

}

export default ChatBot;