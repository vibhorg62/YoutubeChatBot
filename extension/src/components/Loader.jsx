function Loader() {

    return (

        <div className="flex justify-start">

            <div className="bg-zinc-800 rounded-xl px-4 py-3">

                <div className="flex gap-2">

                    <span className="w-2 h-2 bg-white rounded-full animate-bounce"></span>

                    <span
                        className="w-2 h-2 bg-white rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                    ></span>

                    <span
                        className="w-2 h-2 bg-white rounded-full animate-bounce"
                        style={{ animationDelay: "0.4s" }}
                    ></span>

                </div>

            </div>

        </div>

    );

}

export default Loader;