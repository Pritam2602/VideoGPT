# 🎥 VidMind AI

VidMind AI is a full-stack Generative AI application that transforms video content into structured knowledge and enables conversational querying using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

* 🔗 Supports multiple video platforms (YouTube, Vimeo, etc.)
* 🧠 Automatic transcription using Whisper
* ✂️ Smart chunking for long videos
* 📊 Vector embeddings using FAISS
* 💬 Chat with video content (RAG pipeline)
* ⚡ Real-time streaming responses
* 🎨 ChatGPT-like UI with multi-chat support

---

## 🧠 Tech Stack

### Backend

* FastAPI
* LangChain
* OpenAI
* Whisper
* FAISS

### Frontend

* React (Vite)
* Streaming API (ReadableStream)

---

## ⚙️ How It Works

1. User inputs a video link
2. Audio is extracted using yt-dlp
3. Whisper generates transcript
4. Transcript is split into chunks
5. Chunks are embedded and stored in FAISS
6. User queries → relevant chunks retrieved
7. LLM generates context-aware response

---

## 🖥️ Project Structure

```
VideoGPT/
├── backend/
│   ├── app.py
│   ├── run.py
│   ├── services/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   └── package.json
│
└── README.md
```

---

## 🧪 How to Run Locally

### 1️⃣ Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Backend will run at:

```
http://127.0.0.1:8000
```

---

### 2️⃣ Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at:

```
http://localhost:5173
```

---

## 💡 Example Queries

* "Summarize this video"
* "What are the key points?"
* "Explain the main concept"
* "Give important takeaways"

---

## 🔥 Key Highlights

* Handles long videos using chunking + map-reduce summarization
* Uses RAG (Retrieval-Augmented Generation) for accurate answers
* Streams responses in real-time like ChatGPT
* Supports multi-conversation workflow

---

## 🚧 Future Improvements

* User authentication
* Cloud deployment (AWS / Vercel / Render)
* Vector DB upgrade (Pinecone / Weaviate)
* Voice input & output
* PDF export of summaries

---

## 🧑‍💻 Author

**Pritam S**

---

## 💬 Project Description

VidMind AI converts videos into searchable knowledge and enables chat-based querying using RAG and LLMs. It uses transcription, chunking, and vector embeddings for accurate, context-aware responses with real-time streaming.

---
