"use client";

import { useState, useRef } from "react";

interface Message {
  type: "user" | "ai";
  text: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [showMenu, setShowMenu] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const BACKEND_URL =
    process.env.NEXT_PUBLIC_BACKEND_URL ||
    "http://127.0.0.1:8000";

  const handleFileSelect = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) return;

    setFile(selectedFile);

    const icon = selectedFile.type.includes("pdf")
      ? "📄"
      : "📷";

    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        text: `${icon} ${selectedFile.name}`,
      },
    ]);
  };

  const sendMessage = async () => {
    if (!question.trim() && !file) return;

    const userQuestion = question;

    if (userQuestion.trim()) {
      setMessages((prev) => [
        ...prev,
        {
          type: "user",
          text: userQuestion,
        },
      ]);
    }

    setQuestion("");

    try {
      // ==========================
      // FILE UPLOAD
      // ==========================
      if (file) {
        const formData = new FormData();
        formData.append("file", file);

        // PDF Upload
        if (file.type.includes("pdf")) {
          const response = await fetch(
            `${BACKEND_URL}/upload-document`,
            {
              method: "POST",
              body: formData,
            }
          );

          const data = await response.json();
          console.log("upload-document response:", data);

          setMessages((prev) => [
            ...prev,
            {
              type: "ai",
              text:
                data.summary || data.error || "PDF uploaded successfully",
            },
          ]);

          setFile(null);
          return;
        }

        // Image Upload
        formData.append(
          "question",
          userQuestion || "Describe this image"
        );

        const response = await fetch(
          `${BACKEND_URL}/analyze`,
          {
            method: "POST",
            body: formData,
          }
        );

        const data = await response.json();

        setMessages((prev) => [
          ...prev,
          {
            type: "ai",
            text:
              data.answer ||
              data.description ||
              "No response",
          },
        ]);

        setFile(null);
        return;
      }

      // ==========================
      // MEMORY / RAG QUESTION
      // ==========================
      const formData = new FormData();

      formData.append(
        "question",
        userQuestion
      );

      const response = await fetch(
        `${BACKEND_URL}/ask`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          text:
            data.answer ||
            "No answer found",
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          text: "Backend Error",
        },
      ]);
    }
  };

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="header">
        <h1>Ani's Chatbot</h1>
      </div>

      {/* Chat Area */}
      <div className="chat-area">
        {messages.length === 0 ? (
          <div className="welcome">
            <h2>Welcome to Ani's Chatbot 🤖</h2>

            <p>
              Upload images, PDFs and ask
              questions from memory.
            </p>
          </div>
        ) : (
          messages.map(
            (message, index) => (
              <div
                key={index}
                className={`message ${message.type}`}
              >
                {message.text}
              </div>
            )
          )
        )}
      </div>

      {/* Bottom Input Bar */}
      <div className="input-bar">
        <button
          className="upload-btn"
          onClick={() =>
            setShowMenu(!showMenu)
          }
        >
          +
        </button>

        {showMenu && (
          <div className="upload-menu">
            <div
              className="menu-item"
              onClick={() => {
                fileInputRef.current?.click();
                setShowMenu(false);
              }}
            >
              📎 Add photos & files
            </div>
          </div>
        )}

        <input
          ref={fileInputRef}
          type="file"
          accept="image/*,.pdf"
          style={{
            display: "none",
          }}
          onChange={handleFileSelect}
        />

        <input
          className="chat-input"
          type="text"
          placeholder="Message Ani..."
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
        />

        <button
          className="send-btn"
          onClick={sendMessage}
        >
          ↑
        </button>
      </div>
    </div>
  );
}