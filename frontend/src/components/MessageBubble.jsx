import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function MessageBubble({ role, content }) {
  const isUser = role === "user";

  return (
    <div className={`message ${isUser ? "message--user" : ""}`}>
      <div
        className={`message__avatar ${
          isUser ? "message__avatar--user" : "message__avatar--assistant"
        }`}
      >
        {isUser ? "U" : "⚡"}
      </div>

      <div className="message__content">
        <div className="message__role">
          {isUser ? "You" : "VideoGPT"}
        </div>

        {/*  THIS IS THE FIX */}
        <div className="message__text">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}