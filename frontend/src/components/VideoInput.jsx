import { useState } from "react";

export default function VideoInput({ onSubmit, isLoading }) {
  const [url, setUrl] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!url.trim() || isLoading) return;
    onSubmit(url.trim());
    setUrl("");
  }

  return (
    <form className="video-input" onSubmit={handleSubmit}>
      <input
        id="video-url-input"
        className="video-input__field"
        type="url"
        placeholder="Paste a video URL (YouTube, Vimeo, etc.)"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        disabled={isLoading}
      />
      <button
        id="generate-article-btn"
        className="video-input__btn"
        type="submit"
        disabled={!url.trim() || isLoading}
      >
        {isLoading ? <span className="spinner" /> : "Generate Article"}
      </button>
    </form>
  );
}
