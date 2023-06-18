import React, { useState } from "react";
import "./App.css";
import { generateResponse } from "./Utils/actions";
// import PieChart from "./components/PieChart";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async (event) => {
    event.preventDefault();

    if (currentMessage.trim().length === 0) return;

    const userMessage = {
      id: messages.length,
      text: currentMessage,
      user: "User",
    };

    setMessages((msgs) => [...msgs, userMessage]);
    setCurrentMessage("");
    const data = { message: currentMessage };

    setLoading(true);

    try {
      const response = await generateResponse(data);
      console.log(response);
      const aiMessage = response.message.choices[0].message.content;

      const newMessage = {
        id: messages.length + 1,
        text: aiMessage,
        user: "AI",
      };

      setMessages((msgs) => [...msgs, newMessage]);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="text-4xl font-bold">Clinical Trials AI Assistant</h1>
      </header>
      <main className="App-main">
        <div className="Chat-box">
          {messages.map((message) => (
            <div
              key={message.id}
              className={message.user === "User" ? "User" : "AI"}
            >
              <p>{message.text}</p>
            </div>
          ))}
        </div>
        <form className="Chat-input" onSubmit={sendMessage}>
          <input
            type="text"
            value={currentMessage}
            onChange={(event) => setCurrentMessage(event.target.value)}
            placeholder="Type your question..."
            className="p-2 border rounded-md"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-blue-500 text-white rounded-md disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? (<span class="loading loading-dots loading-md"></span>) : "Send"}
          </button>
        </form>
        {/* <PieChart /> */}
      </main>
    </div>
  );
};

export default App;
