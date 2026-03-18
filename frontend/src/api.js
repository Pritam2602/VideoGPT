const API_BASE = "http://localhost:8000";

/**
 * Generate an article from a video URL.
 * POST /summarize
 */
export async function summarizeVideo(url) {
  const res = await fetch(`${API_BASE}/summarize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Server error" }));
    throw new Error(err.detail || "Failed to generate article");
  }

  return res.json(); // { article, video_id }
}

/**
 * Stream chat responses via the RAG endpoint.
 * GET /chat?query=...&video_id=...
 *
 * @param {string} query
 * @param {string|null} videoId
 * @param {(chunk: string) => void} onChunk — called for every text chunk
 * @returns {Promise<string>} full accumulated response
 */
export async function chatStream(query, videoId, onChunk) {
  const params = new URLSearchParams({ query });
  if (videoId) params.set("video_id", videoId);

  const res = await fetch(`${API_BASE}/chat?${params}`);

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Server error" }));
    throw new Error(err.detail || "Chat request failed");
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let full = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const text = decoder.decode(value, { stream: true });
    full += text;
    onChunk(text);
  }

  return full;
}
