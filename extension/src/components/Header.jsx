import { Bot } from "lucide-react";

function Header() {
  return (
    <div className="flex items-center gap-3 border-b border-zinc-800 px-5 py-4">

      <div className="bg-blue-600 p-2 rounded-xl">
        <Bot size={22} />
      </div>

      <div>
        <h1 className="text-lg font-bold">
          YouTube AI Chat
        </h1>

        <p className="text-xs text-zinc-400">
          Chat with the current YouTube video
        </p>
      </div>

    </div>
  );
}

export default Header;