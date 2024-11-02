// app/components/ui/chat/ChatRoom/ChatRoom.tsx
import React, { useEffect, useRef, useState } from "react";
import MessageList from "../MessageList/MessageList"
import ChatInput from "../ChatInput/ChatInput"
import axios from "axios";

interface Message {
  id?: string;
  _id?: string;
  sender?: string;
  userName?: string;
  firstName?: string;
  lastName?: string;
  content: string;
  timestamp: Date;
  status?: "sent" | "delivered" | "read";
}

interface ChatRoomProps {
  roomId: string;
}


interface MessageResponse {
  _id?: string;
  id?: string;
  content: string;
  timestamp: Date | string;
  userName?: string;
  firstName?: string;
  lastName?: string;
}

const ChatRoom: React.FC<ChatRoomProps> = ({ roomId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [wsConnection, setWsConnection] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);


  // Keep track of processed message IDs to prevent duplicates
  const processedMessages = useRef(new Set<string>())

  useEffect(() => {
    let ws: WebSocket | null = null; // Initialize Websocket object in useEffect

    //inline function to connect Backend Socket
    const connectWebSocket = async () => {
      try {
        // Get the access token first
        const tokenResponse = await axios.get('/api/getAccessToken');
        const { access_token } = tokenResponse.data;

        //console.log('Connecting WebSocket with token:', access_token);

        // Create WebSocket connection with token
        ws = new WebSocket(`ws://localhost:5004/chat/ws/${roomId}?token=${access_token}`);

        ws.onopen = () => {
          console.log('WebSocket connected');
          setIsConnected(true);
          setWsConnection(ws);
          setError(null);
        };

        ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data);
            console.log('Received message:', message);

            // check if we have already processed this message 
            const messageId = message._id || message.id;
            if (messageId && !processedMessages.current.has(messageId)) {
              processedMessages.current.add(messageId)
              setMessages(prev => {
                if (!Array.isArray(prev)) {
                  return [message];
                }
                return [...prev, message]
              })
            }
          } catch (err) {
            console.error('Error parsing message:', err);
          }
        };

        ws.onclose = (event) => {
          console.log('WebSocket closed:', event.code, event.reason);
          setIsConnected(false);
          setWsConnection(null);
          if (event.code === 4001) {
            setError('Authentication failed. Please sign in again.');
          } else {
            setError('Connection Lost. Reconnecting...');
            setTimeout(connectWebSocket, 3000);
          }
        };

        ws.onerror = (event) => {
          console.error('WebSocket error:', event);
          setError("Connection error occurred");
        };

      } catch (err) {
        console.error('Connection setup error:', err);
        setError("Failed to establish connection");
        setTimeout(connectWebSocket, 3000);
      }
    };

    // Load initial messages
    const loadInitialMessages = async () => {
      try {
        const tokenResponse = await axios.get('/api/getAccessToken');
        const { access_token } = tokenResponse.data;

        //console.log('Loading messages with token:', access_token);

        const response = await axios.get(
          `http://localhost:5004/chat/chatroom/${roomId}/messages`,
          {
            headers: {
              Authorization: `Bearer ${access_token}`
            },
            withCredentials: true
          }
        );

        if (Array.isArray(response.data)) {
          response.data.forEach((msg: MessageResponse) => {
            const messageId = msg._id || msg.id
            if (messageId) {
              processedMessages.current.add(messageId)
            }
          })
          setMessages(response.data)

        } else if (response.data && Array.isArray(response.data.messages)) {
          response.data.messages.forEach((msg: MessageResponse) => {
            const messageId = msg._id || msg.id
            if (messageId) {
              processedMessages.current.add(messageId)
            }
          });
          setMessages(response.data.messages)
        } else {
          console.error("Unexpected messages format: ", response.data)
          setMessages([])
        }
      } catch (err) {
        console.error('Failed to load messages:', err);
        setError('Failed to load messages');
        setMessages([])
      }
    };

    // Clear processed messages when changing rooms 
    processedMessages.current.clear()
    loadInitialMessages();
    connectWebSocket();

    // Cleanup function
    return () => {
      if (ws && ws.readyState === WebSocket.OPEN) {
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
      console.error('Send message error:', err);
      setError("Failed to send message");
    }
  };

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
