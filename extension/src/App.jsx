import Header from "./components/Header";
import ChatBot from "./components/ChatBot";

function App() {
  return (
    <div className="w-100 h-150 bg-zinc-950 text-white flex flex-col">
      <Header />
      <ChatBot />
    </div>
  );
}

export default App;