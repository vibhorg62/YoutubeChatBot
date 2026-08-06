import { askPython } from "../services/pythonService.js";

// ---------------- Conversation Memory ---------------- //

let currentVideo = "";
let history = [];

// ----------------------------------------------------- //

export const chat = async (req, res) => {
    console.log("✅ Request Received");

    try {

        const { url, question } = req.body;

        // Reset history if video changes

        if (url !== currentVideo) {

            currentVideo = url;

            history = [];

        }

        const answer = await askPython(

            url,
            question,
            history

        );

        // Save current conversation

        history.push({

            role: "user",

            content: question

        });

        history.push({

            role: "assistant",

            content: answer

        });

        // Keep only last 10 exchanges (20 messages)

        if (history.length > 20) {

            history = history.slice(-20);

        }

        res.json({

            success: true,

            data: answer

        });

    }

    catch (err) {

        console.error(err);

        res.status(500).json({

            success: false,

            message: err.message

        });

    }

};