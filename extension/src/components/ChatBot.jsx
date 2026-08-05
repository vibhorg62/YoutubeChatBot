import { useEffect, useRef, useState } from "react";
import Input from "./Input";
import Message from "./Message";
import Loader from "./Loader";

function ChatBot() {

    const [messages, setMessages] = useState([
        {
            sender: "bot",
            text: "👋 Hi! Ask me anything about the current YouTube video."
        }
    ]);

    const [loading, setLoading] = useState(false);

    const [videoUrl, setVideoUrl] = useState("");

    const chatRef = useRef(null);

    useEffect(() => {

        chrome.tabs.query(
            {
                active: true,
                currentWindow: true
            },
            (tabs) => {

                if (tabs.length) {

                    console.log("Video URL:", tabs[0].url);

                    setVideoUrl(tabs[0].url);

                }

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

            console.log("Sending Request...");

            const response = await fetch(
                "http://localhost:8000/api/chat",
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

            console.log("Status:", response.status);

            if (!response.ok) {
                throw new Error("Server Error");
            }

            const data = await response.json();

            console.log("Backend Response:", data);

            setMessages(prev => [
                ...prev,
                {
                    sender: "bot",
                    text: data.data || "No response received."
                }
            ]);

        }
        catch (err) {

            console.error(err);

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

        <div className="flex-1 flex flex-col">

            <div
                ref={chatRef}
                className="flex-1 overflow-y-auto p-4 space-y-4"
            >

                <div className="text-xs text-zinc-400 bg-zinc-900 rounded-lg p-3 break-all">

                    📺 {videoUrl || "Open a YouTube Video"}

                </div>

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

            <Input
                onSend={sendMessage}
            />

        </div>

    );

}

export default ChatBot;