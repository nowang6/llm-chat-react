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
      const eventSource = new EventSource(`http://localhost:5000/chat?input_text=${encodeURIComponent(inputText)}`);
      
      eventSource.onmessage = (event) => {
        if (event.data === '[DONE]') {
          console.log("Stream finished");
          eventSource.close();
          setLoading(false);
        } else {
          const data = JSON.parse(event.data);
          console.log("Received chunk:", data.content);
          setResponseText((prev) => prev + data.content);
        }
      };

      eventSource.onerror = (error) => {
        console.error("EventSource failed:", error);
        eventSource.close();
        setLoading(false);
      };

      eventSource.onopen = () => {
        console.log("EventSource connection opened");
      };

    } catch (error) {
      console.error("Error setting up EventSource", error);
      setResponseText("Error fetching the API");
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chat with AI</h1>
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            value={inputText} 
            onChange={handleInputChange} 
            placeholder="Type your message here"
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Sending...' : 'Send'}
          </button>
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