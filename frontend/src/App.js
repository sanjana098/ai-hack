import React, { useState } from "react";
import "./App.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState("");

  const sendMessage = (event) => {
    event.preventDefault();

    if (currentMessage.trim().length === 0) return;

    // API Call to API endpoint would go here.
    fetch("http://127.0.0.1:5000/api/response", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(currentMessage)}).then(response => response.json()).then(data => console.log(data))

    const newMessage = {
      id: messages.length,
      text: currentMessage,
      user: "User",
    };

    setMessages([...messages, newMessage]);

    setCurrentMessage("");
  };

  return (
    <div className="App h-screen">
      <header className="App-header">
        <h1 class="text-2xl">Clinical Trials AI Assistant</h1>
      </header>
      <main className="App-main">
        {/* <div className="Chat-box">
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
        </form> */}
        <div className="chat-box">
          <form className="chat-input" onSubmit={sendMessage}>
            <input

              type="text"
              value={currentMessage}
              onChange={(event) => setCurrentMessage(event.target.value)}
              placeholder="Type your question..."
            />
            <button type="submit">Send</button>
          </form>
        </div>
      </main>
    </div>
  );
};

export default App;
