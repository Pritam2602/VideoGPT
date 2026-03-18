import { useState } from "react";

export default function ChatInput({ onSend, disabled }) {
  const [text, setText] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!text.trim() || disabled) return;
    onSend(text.trim());
    setText("");
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <textarea
        id="chat-input-field"
        className="chat-input__field"
        rows={1}
        placeholder={
          disabled
            ? "Process a video first to start chatting..."
            : "Ask a question about the video..."
        }
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
      />
      <button
        id="send-chat-btn"
        className="chat-input__send"
        type="submit"
        disabled={disabled || !text.trim()}
        title="Send message"
      >
        ➤
      </button>
    </form>
  );
}
