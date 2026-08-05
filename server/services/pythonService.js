import { spawn } from "child_process";

const python = spawn("python", ["../chatbot/app.py"]);

python.stdout.setEncoding("utf8");
python.stderr.setEncoding("utf8");

let buffer = "";

const queue = [];
let busy = false;

// ---------------- STDERR ---------------- //

python.stderr.on("data", (data) => {

    console.log("[PYTHON]", data.toString());

});

// ---------------- STDOUT ---------------- //

python.stdout.on("data", (data) => {

    buffer += data;

    const lines = buffer.split("\n");

    buffer = lines.pop();

    for (const line of lines) {

        if (!line.trim()) continue;

        let response;

        try {

            response = JSON.parse(line);

        } catch {

            console.log("[IGNORED]", line);

            continue;

        }

        const current = queue.shift();

        if (!current) continue;

        busy = false;

        if (response.error) {

            current.reject(new Error(response.error));

        } else {

            current.resolve(response.answer);

        }

        processQueue();

    }

});

// ---------------- PROCESS ---------------- //

python.on("close", (code) => {

    console.log("Python Worker Closed:", code);

});

python.on("error", (err) => {

    console.error(err);

});

// ---------------- QUEUE ---------------- //

function processQueue() {

    if (busy) return;

    if (queue.length === 0) return;

    busy = true;

    const current = queue[0];

    python.stdin.write(

        JSON.stringify({

            url: current.url,
            question: current.question,
            history: current.history

        }) + "\n"

    );

}

// ---------------- API ---------------- //

export const askPython = (url, question, history) => {

    return new Promise((resolve, reject) => {

        queue.push({

            url,
            question,
            history,
            resolve,
            reject

        });

        processQueue();

    });

};