"use client";

import ChatRoom from '../components/ui/chat/ChatRoom/ChatRoom';
import Header from '../components/ui/header/Header';

export default function ChatPage() {
  return (
    <div className="container mx-auto px-4">
      <Header />
      <div className="h-[calc(100vh-100px)] mt-6">
        <ChatRoom roomId="default-room" />
      </div>
    </div>
  );
}
