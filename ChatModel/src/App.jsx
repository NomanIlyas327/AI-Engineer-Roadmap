import React, { useState, useEffect, useRef } from 'react';

const MessageBubble = ({ msg }) => {
  const isUser = msg.sender === 'user';
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(msg.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-lg transition-all duration-200 relative group ${
          isUser
            ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-br-none'
            : 'bg-slate-800/90 text-slate-100 border border-slate-700/50 rounded-bl-none backdrop-blur-md'
        }`}
      >
        <div className="flex items-center gap-2 mb-1 opacity-70 text-xs font-semibold uppercase tracking-wider">
          <span>{isUser ? 'You' : 'PakShop AI'}</span>
          <span className="text-[10px]">
            {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>

        <div className="text-sm leading-relaxed whitespace-pre-wrap font-sans">{msg.text}</div>

        {!isUser && (
          <button
            onClick={copyToClipboard}
            className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-slate-700 rounded text-xs text-slate-400 hover:text-white"
            title="Copy Message"
          >
            {copied ? '✓ Copied' : '📋 Copy'}
          </button>
        )}
      </div>
    </div>
  );
};

export default function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: 'Assalam-o-Alaikum! Main PakShop AI Assistant hoon. Aaj main aap ki kya madad kar sakta hoon?',
      timestamp: new Date().toISOString(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const suggestions = [
    'Order track kaise karein?',
    'Payment methods konsay hain?',
    'Return policy kya hai?',
  ];

  const handleSend = async (textToSend) => {
    const query = textToSend || input;
    if (!query.trim() || isLoading) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: query,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: query }),
      });

      if (!response.ok) throw new Error('Network error');

      const data = await response.json();

      const botMsg = {
        id: Date.now() + 1,
        sender: 'bot',
        text: data.reply || 'No response received.',
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'bot',
          text: '⚠️ Connection Error: FastAPI server run nahi ho raha ya response fail ho gaya hai.',
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: Date.now(),
        sender: 'bot',
        text: 'Chat history cleared. Aap naya sawal pooch sakte hain!',
        timestamp: new Date().toISOString(),
      },
    ]);
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-slate-950 text-slate-100 font-sans overflow-hidden">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 bg-slate-900/80 border-b border-slate-800 backdrop-blur-md z-10">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-500 to-indigo-500 flex items-center justify-center shadow-lg text-xl font-bold">
              🤖
            </div>
            <span className="absolute bottom-0 right-0 w-3 h-3 bg-emerald-500 border-2 border-slate-900 rounded-full animate-pulse"></span>
          </div>
          <div>
            <h1 className="font-bold text-lg bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
              PakShop AI Assistant
            </h1>
            <p className="text-xs text-emerald-400 font-medium flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Online & Connected
            </p>
          </div>
        </div>

        <button
          onClick={clearChat}
          className="px-3 py-1.5 text-xs font-semibold text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg transition-all cursor-pointer"
        >
          🗑️ Clear Chat
        </button>
      </header>

      {/* Main Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 max-w-4xl w-full mx-auto">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} msg={msg} />
        ))}

        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-slate-800/90 text-slate-400 border border-slate-700/50 rounded-2xl rounded-bl-none px-4 py-3 flex items-center gap-2">
              <span className="text-xs font-semibold">AI is thinking</span>
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></span>
                <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce [animation-delay:0.4s]"></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Suggestion Chips */}
      {messages.length < 3 && (
        <div className="max-w-4xl w-full mx-auto px-4 mb-2 flex gap-2 overflow-x-auto">
          {suggestions.map((item, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(item)}
              className="whitespace-nowrap px-3 py-1.5 text-xs bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-full transition-all shadow-sm cursor-pointer"
            >
              💡 {item}
            </button>
          ))}
        </div>
      )}

      {/* Input Box Footer */}
      <footer className="p-4 bg-slate-900/80 border-t border-slate-800 backdrop-blur-md">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Apna sawaal likhein... (Press Enter to Send)"
            disabled={isLoading}
            className="flex-1 bg-slate-950 border border-slate-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 outline-none transition-all disabled:opacity-50"
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || isLoading}
            className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold px-5 py-3 rounded-xl text-sm transition-all shadow-lg hover:shadow-indigo-500/25 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 cursor-pointer"
          >
            <span>Send</span>
            <span>🚀</span>
          </button>
        </div>
      </footer>
    </div>
  );
}