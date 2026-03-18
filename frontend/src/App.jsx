import { useState, useRef, useEffect, useCallback } from "react";
import "./App.css";
import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import VideoInput from "./components/VideoInput";
import ChatInput from "./components/ChatInput";
import { summarizeVideo, chatStream } from "./api";

/**
 * A single conversation has an id, title, videoId, and list of messages.
 * Each message: { role: "user" | "assistant", content: string }
 */
function createConversation(title = "New chat") {
  return {
    id: crypto.randomUUID(),
    title,
    videoId: null,
    messages: [],
  };
}

export default function App() {
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const chatEndRef = useRef(null);

  // Derived: active conversation
  const active = conversations.find((c) => c.id === activeId) || null;

  // Auto-scroll on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [active?.messages?.length, isStreaming]);

  // ------- helpers to mutate conversation state -------
  const updateConversation = useCallback((id, updater) => {
    setConversations((prev) =>
      prev.map((c) => (c.id === id ? updater(c) : c))
    );
  }, []);

  const pushMessage = useCallback(
    (id, msg) => {
      updateConversation(id, (c) => ({
        ...c,
        messages: [...c.messages, msg],
      }));
    },
    [updateConversation]
  );

  const updateLastAssistant = useCallback(
    (id, chunk) => {
      updateConversation(id, (c) => {
        const msgs = [...c.messages];
        const last = msgs[msgs.length - 1];
        if (last && last.role === "assistant") {
          msgs[msgs.length - 1] = { ...last, content: last.content + chunk };
        }
        return { ...c, messages: msgs };
      });
    },
    [updateConversation]
  );

  // ------- actions -------
  function handleNewChat() {
    const conv = createConversation();
    setConversations((prev) => [conv, ...prev]);
    setActiveId(conv.id);
  }

  async function handleSubmitVideo(url) {
  if (!url.trim()) return;

  let convId = activeId;

  if (!convId) {
    const conv = createConversation(url);
    setConversations((prev) => [conv, ...prev]);
    setActiveId(conv.id);
    convId = conv.id;
  }

  updateConversation(convId, (c) => ({ ...c, title: url }));

  pushMessage(convId, {
    role: "user",
    content: ` Generate article from: ${url}`,
  });

  
  pushMessage(convId, {
    role: "assistant",
    content: " Processing video... please wait",
  });

  setIsProcessing(true);

  try {
    const { article, video_id } = await summarizeVideo(url);

    updateConversation(convId, (c) => ({ ...c, videoId: video_id }));

    //  Replace last message instead of adding new
    updateConversation(convId, (c) => {
      const msgs = [...c.messages];
      msgs[msgs.length - 1] = {
        role: "assistant",
        content: article,
      };
      return { ...c, messages: msgs };
    });
  } catch (err) {
    updateLastAssistant(convId, ` Error: ${err.message}`);
  } finally {
    setIsProcessing(false);
  }
}

  async function handleSendChat(query) {
    if (!query.trim() || !active) return;

    pushMessage(active.id, { role: "user", content: query });
    pushMessage(active.id, { role: "assistant", content: "" });

    setIsStreaming(true);
    try {
      await chatStream(query, active.videoId, (chunk) => {
        updateLastAssistant(active.id, chunk);
      });
    } catch (err) {
      updateLastAssistant(active.id, `\n\n Error: ${err.message}`);
    } finally {
      setIsStreaming(false);
    }
  }

  return (
    <div className="app">
      <Sidebar
        conversations={conversations}
        activeId={activeId}
        onSelect={setActiveId}
        onNewChat={handleNewChat}
      />

      <div className="main">
        <div className="main__header">
          <span className="main__header-title">
            {active ? active.title : "VideoGPT"}
          </span>
          {active?.videoId && (
            <span className="main__header-badge">RAG Active</span>
          )}
        </div>

        <ChatArea
          messages={active?.messages || []}
          isStreaming={isStreaming}
          chatEndRef={chatEndRef}
          hasConversation={!!active}
        />

        <div className="input-area">
          <div className="input-area__inner">
            <VideoInput
              onSubmit={handleSubmitVideo}
              isLoading={isProcessing}
            />
            <ChatInput
              onSend={handleSendChat}
              disabled={!active?.videoId || isStreaming || isProcessing}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
