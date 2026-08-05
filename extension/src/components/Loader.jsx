function Loader() {

    return (

        <div className="flex justify-start">

            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl rounded-bl-sm px-4 py-3">

                <div className="flex items-center gap-3">

                    <div className="flex gap-1">

                        <span className="w-2 h-2 rounded-full bg-blue-500 animate-bounce"></span>

                        <span
                            className="w-2 h-2 rounded-full bg-blue-500 animate-bounce"
                            style={{ animationDelay: "0.15s" }}
                        ></span>

                        <span
                            className="w-2 h-2 rounded-full bg-blue-500 animate-bounce"
                            style={{ animationDelay: "0.3s" }}
                        ></span>

                    </div>

                    <p className="text-sm text-zinc-400">

                        Thinking...

                    </p>

                </div>

            </div>

        </div>

    );

}

export default Loader;