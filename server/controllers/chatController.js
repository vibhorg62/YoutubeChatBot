import { askPython } from "../services/pythonService.js";

export const chat = async (req, res) => {

    try {

        const { url, question } = req.body;

        const answer = await askPython(url, question);

        res.json({
            success: true,
            data: answer
        });

    } catch (err) {

        console.error(err);

        res.status(500).json({
            success: false,
            message: err.message
        });

    }

};