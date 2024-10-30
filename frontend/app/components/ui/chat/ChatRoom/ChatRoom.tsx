// app/components/ui/chat/ChatRoom/ChatRoom.tsx
import React, { useEffect, useState } from "react";
import MessageList from "../MessageList/MessageList"
import ChatInput from "../ChatInput/ChatInput"
import axios from "axios";

interface Message {
  id: string;
  sender: string;
  content: string;
  timestamp: Date;
  status: "sent" | "delivered" | "read";
}

interface ChatRoomProps {
  roomId: string;
}

const ChatRoom: React.FC<ChatRoomProps> = ({ roomId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [wsConnection, setWsConnection] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let ws: WebSocket | null = null;

    const connectWebSocket = async () => {
      try {
        // First, establish WebSocket connection
        ws = new WebSocket(`ws://localhost:5004/chat?room=${roomId}`);
        
        ws.onopen = () => {
          setIsConnected(true);
          setWsConnection(ws);
          setError(null);
        };

        ws.onmessage = (event) => {
          const message = JSON.parse(event.data);
          setMessages(prev => [...prev, message]);
        };

        ws.onclose = () => {
          setIsConnected(false);
          setWsConnection(null);
          setError('Connection Lost. Reconnecting...');
          // attempt to reconnect after 3 seconds
          setTimeout(connectWebSocket, 3000);
        };

        ws.onerror = () => {
          setError("Connection error occurred");
        };

      } catch (err) {
        setError("Failed to establish connection");
        setTimeout(connectWebSocket, 3000);
      }
    };

    // load initial messages
    const loadInitialMessages = async () => {
      try {
        const response = await axios.get(`http://localhost:5004/chat/messages/${roomId}`, {
          withCredentials: true
        });
        setMessages(response.data.messages);
      } catch (err) {
        setError('Failed to load messages');
      }
    };

    loadInitialMessages();
    connectWebSocket();

    // Cleanup function
    return () => {
      if (ws) {
        ws.close();
        setWsConnection(null);
        setIsConnected(false);
      }
    };
  }, [roomId]);

  const sendMessage = async (content: string) => {
    if (!wsConnection || !isConnected) {
      return;
    }

    const message = {
      type: 'message',
      content,
      roomId,
      timestamp: new Date().toISOString()
    };

    try {
      wsConnection.send(JSON.stringify(message));
    } catch (err) {
      setError("Failed to send message");
    }
  };

  // Moved JSX return outside of sendMessage function
  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded">
          {error}
        </div>
      )}
      <div className="flex-grow overflow-y-auto">
        <MessageList messages={messages} />
      </div>
      <div className="border-t">
        <ChatInput onSendMessage={sendMessage} isConnected={isConnected} />
      </div>
    </div>
  );
};

export default ChatRoom;
