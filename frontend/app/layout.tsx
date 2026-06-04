import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ani's Chatbot",
  description:
    "Multimodal RAG Chatbot using Groq and Pinecone",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}