"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import ChatRoom from "../components/ui/chat/ChatRoom/ChatRoom";
import axios from "axios";

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

  if (!roomId) {
    return <div className="p-4">No room ID provided</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="h-[calc(100vh-200px)]">
        <ChatRoom roomId={roomId} />
      </div>
    </div>
  );
}
