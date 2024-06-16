// src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState("");
  const [responseText, setResponseText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponseText("");  // Clear previous response
    setLoading(true);
    console.log("Submitting input:", inputText);

    try {
      const response = await fetch(`http://my:8001/chat?input_text=${encodeURIComponent(inputText)}`);
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let done = false;
      while (!done) {
        const { value, done: streamDone } = await reader.read();
        done = streamDone;
        const chunk = decoder.decode(value);
        console.log("Received chunk:", chunk);
        setResponseText((prev) => prev + chunk);
      }
    } catch (error) {
      console.error("Error fetching the API", error);
      setResponseText("Error fetching the API");
    }

    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chat with AI</h1>
        <form onSubmit={handleSubmit}>
          <input type="text" value={inputText} onChange={handleInputChange} />
          <button type="submit" disabled={loading}>Send</button>
        </form>
        <div>
          <h2>Response:</h2>
          <pre>{responseText}</pre>
        </div>
      </header>
    </div>
  );
}

export default App;
