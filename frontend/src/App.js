import React, { useState } from "react";
import "./App.css";
import { generateResponse } from "./Utils/actions";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState("");

  const sendMessage = (event) => {
    event.preventDefault();

    if (currentMessage.trim().length === 0) return;

    const data = { message: currentMessage };

    generateResponse(data)
      .then((response) => {
        const newMessage = {
          id: messages.length,
          text: response.response,
          user: "AI",
        };

        setMessages([...messages, newMessage]);
        setCurrentMessage("");
      })
      .catch((error) => console.error(error));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Clinical Trials AI Assistant</h1>
      </header>
      <main className="App-main">
        <div className="Chat-box">
          {messages.map((message) => (
            <div key={message.id} className={message.user}>
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
          />
          <button type="submit">Send</button>
        </form>
      </main>
    </div>
  );
};

export default App;
