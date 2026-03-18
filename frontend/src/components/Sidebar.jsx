export default function Sidebar({ conversations, activeId, onSelect, onNewChat }) {
  return (
    <aside className="sidebar">
      <div className="sidebar__header">
        <div className="sidebar__brand">
          <div className="sidebar__logo">⚡</div>
          <span className="sidebar__title">VideoGPT</span>
        </div>
        <button className="sidebar__new-btn" onClick={onNewChat} id="new-chat-btn">
          ＋ New Chat
        </button>
      </div>

      <div className="sidebar__list">
        {conversations.length === 0 ? (
          <div className="sidebar__empty">
            No conversations yet.<br />
            Paste a video URL to start!
          </div>
        ) : (
          conversations.map((conv, i) => (
            <div
              key={conv.id}
              className={`sidebar__item ${conv.id === activeId ? "sidebar__item--active" : ""}`}
              onClick={() => onSelect(conv.id)}
              style={{ animationDelay: `${i * 50}ms` }}
              title={conv.title}
            >
              📹 {conv.title || "New chat"}
            </div>
          ))
        )}
      </div>
    </aside>
  );
}
