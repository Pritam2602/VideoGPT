import MessageBubble from "./MessageBubble";

export default function ChatArea({ messages, isStreaming, chatEndRef, hasConversation }) {
  if (!hasConversation || messages.length === 0) {
    return (
      <div className="chat-area">
        <div className="welcome">
          <div className="welcome__icon">🎬</div>
          <h1 className="welcome__heading">Welcome to VideoGPT</h1>
          <p className="welcome__sub">
            Transform any video into a polished article, then ask follow-up 
            questions powered by RAG. Paste a video URL below to get started.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-area" id="chat-area">
      {messages.map((msg, i) => (
        <MessageBubble key={i} role={msg.role} content={msg.content} />
      ))}
      {isStreaming && (
        <div className="message" style={{ maxWidth: 800, margin: "0 auto" }}>
          <div className="message__avatar message__avatar--assistant">⚡</div>
          <div className="typing-indicator">
            <span className="typing-indicator__dot" />
            <span className="typing-indicator__dot" />
            <span className="typing-indicator__dot" />
          </div>
        </div>
      )}
      <div ref={chatEndRef} />
    </div>
  );
}
