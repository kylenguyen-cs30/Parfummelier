"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { timeStamp } from "console";

interface ChatPreview {
  chatroom_id: string;
  other_user: {
    id: number;
    userName: string;
    firstName: string;
    lastName: string;
  };
  latest_message?: {
    content: string;
    timestamp: string;
  };
  last_message_at: string;
}

export default function InboxPage() {
  const [chatrooms, setChatrooms] = useState<ChatPreview[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchChatrooms = async () => {
      try {
        const tokenResponse = await axios.get("/api/getAccessToken");
        const { access_token } = tokenResponse.data;

        const response = await axios.get(
          "http://localhost:5004/chat/user/chatrooms",
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
            withCredentials: true,
          },
        );
        setChatrooms(response.data.chatrooms);
      } catch (err) {
        console.error("Failed to load chatrooms:", err);
        setError("Failed tp load conversations");
      } finally {
        setLoading(false);
      }
    };

    fetchChatrooms();
  }, []);

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    if (date.toDateString() === now.toDateString()) {
      return date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
    }
    return date.toLocaleDateString();
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Messages</h1>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4">
          {error}
        </div>
      )}
      {loading ? (
        <div className="text-center py-4">Loading conversations...</div>
      ) : (
        <div className="space-y-4">
          {chatrooms.map((room) => (
            <div
              key={room.chatroom_id}
              onClick={() =>
                router.push(`/chat-page?roomId=${room.chatroom_id}`)
              }
              className="bg-white p-4 rounded-lg shadow hover:bg-gray-50 cursor-pointer transition-colors"
            ></div>
          ))}
        </div>
      )}
    </div>
  );
}
