"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import ChatRoom from "../components/ui/chat/ChatRoom/ChatRoom";
import axios from "axios";

// NOTE:
// interface variable is capturing
// chatroom information
interface ChatInfo {
  roomId: string;
  otheruser: {
    id: number;
    userName: string;
    firstName: string;
    lastName: string;
  };
}

export default function ChatPage() {
  const searchParams = useSearchParams();
  const roomId = searchParams.get("roomId");
  const [chatInfo, setChatInfo] = useState<ChatInfo | null>(null);
  const [error, setError] = useState<string | null>(null);

  // NOTE:
  // Establishing the connection in the backend with HTTP API Endpoint first
  // when it return 201, chatInfo is avaialble and then throw greenlight to
  // useEffect then conditionally render the ChatRoom Component

  useEffect(() => {
    const fetchChatInfo = async () => {
      try {
        const tokenResponse = await axios.get("/api/getAccessToken");
        const { access_token } = tokenResponse.data;
        const response = await axios.get(
          `http://localhost:5004/chat/chatroom/${roomId}/info`,
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
            withCredentials: true,
          },
        );
        setChatInfo(response.data);
      } catch (err) {
        setError("Failed to load chat information");
        console.error("Error", err);
      }
    };

    if (roomId) {
      fetchChatInfo();
    }
  }, [roomId]);

  if (!roomId) {
    return <div className="p-4">No room ID provided</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {chatInfo && (
        <div className="mb-4">
          <h1 className="text-2xl font-bold">
            Chat with {chatInfo.otheruser.firstName}{" "}
            {chatInfo.otheruser.lastName}
          </h1>
        </div>
      )}
      <div className="h-[calc(100vh-200px)]">
        <ChatRoom roomId={roomId} />
      </div>
    </div>
  );
}
