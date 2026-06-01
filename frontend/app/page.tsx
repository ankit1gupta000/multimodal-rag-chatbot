"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState("");

  const [question, setQuestion] = useState("");
  const [memoryQuestion, setMemoryQuestion] = useState("");

  const [description, setDescription] = useState("");
  const [answer, setAnswer] = useState("");
  const [memoryAnswer, setMemoryAnswer] = useState("");

  const [loading, setLoading] = useState(false);

  // Change this after deployment
  const BACKEND_URL = "http://127.0.0.1:8000";

  const handleFileChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const selectedFile = e.target.files?.[0];

    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      alert("Please upload an image");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question);

    try {
      const response = await fetch(
        `${BACKEND_URL}/analyze`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setDescription(data.description || "");
      setAnswer(data.answer || "");
    } catch (error) {
      console.error(error);
      alert("Backend Error");
    }

    setLoading(false);
  };

  const handleMemoryAsk = async () => {
    if (!memoryQuestion) {
      alert("Enter a question");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append(
      "question",
      memoryQuestion
    );

    try {
      const response = await fetch(
        `${BACKEND_URL}/ask`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setMemoryAnswer(
        data.answer || "No answer found"
      );
    } catch (error) {
      console.error(error);
      alert("Backend Error");
    }

    setLoading(false);
  };

  return (
    <main
      style={{
        maxWidth: "1000px",
        margin: "auto",
        padding: "30px",
        fontFamily: "Arial",
      }}
    >
      <h1
        style={{
          textAlign: "center",
          fontSize: "50px",
          fontWeight: "bold",
          marginBottom: "10px",
        }}
      >
        Welcome to Ani's Chatbot
      </h1>

      <p
        style={{
          textAlign: "center",
          color: "#666",
          marginBottom: "30px",
        }}
      >
        Multimodal RAG using Gemini Vision + Pinecone
      </p>

      <div
        style={{
          border: "1px solid #ddd",
          padding: "20px",
          borderRadius: "10px",
          marginBottom: "30px",
        }}
      >
        <h2>Upload Image</h2>

        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
        />

        <br />
        <br />

        {preview && (
          <img
            src={preview}
            alt="preview"
            style={{
              width: "250px",
              borderRadius: "10px",
              marginBottom: "20px",
            }}
          />
        )}

        <input
          type="text"
          placeholder="Ask about this image..."
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          style={{
            width: "100%",
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #ccc",
          }}
        />

        <br />
        <br />

        <button
          onClick={handleAnalyze}
          style={{
            width: "100%",
            padding: "15px",
            fontSize: "18px",
            backgroundColor: "#000",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
          }}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Image"}
        </button>
      </div>

      <div
        style={{
          border: "1px solid #ddd",
          padding: "20px",
          borderRadius: "10px",
          marginBottom: "30px",
        }}
      >
        <h2>Image Description</h2>

        <div
          style={{
            minHeight: "120px",
            background: "#f5f5f5",
            padding: "15px",
            borderRadius: "8px",
          }}
        >
          {description ||
            "Description will appear here"}
        </div>

        <br />

        <h2>Answer</h2>

        <div
          style={{
            minHeight: "120px",
            background: "#f5f5f5",
            padding: "15px",
            borderRadius: "8px",
          }}
        >
          {answer ||
            "Answer will appear here"}
        </div>
      </div>

      <div
        style={{
          border: "1px solid #ddd",
          padding: "20px",
          borderRadius: "10px",
        }}
      >
        <h2>Ask Memory (RAG)</h2>

        <input
          type="text"
          placeholder="Ask about previous uploaded images..."
          value={memoryQuestion}
          onChange={(e) =>
            setMemoryQuestion(
              e.target.value
            )
          }
          style={{
            width: "100%",
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #ccc",
          }}
        />

        <br />
        <br />

        <button
          onClick={handleMemoryAsk}
          style={{
            width: "100%",
            padding: "15px",
            fontSize: "18px",
            backgroundColor: "#000",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
          }}
        >
          Ask Memory
        </button>

        <br />
        <br />

        <h2>Memory Answer</h2>

        <div
          style={{
            minHeight: "120px",
            background: "#f5f5f5",
            padding: "15px",
            borderRadius: "8px",
          }}
        >
          {memoryAnswer ||
            "Memory answer will appear here"}
        </div>
      </div>
    </main>
  );
}