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
  const [messages, setMessages] = useState<Message[]>([])
  const [wsConnection, setWsConnection] = useState<WebSocket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const connectWebSocket = async () => {
      try {
        // First, establish Websocket connection 
        // the cookie will be automatiacally included because it's httpOnly
        const ws = new WebSocket(`ws://localhost:5004/chat?room=${roomId}`)
        ws.onopen = () => {
          setIsConnected(true)
          setWsConnection(ws)
          setError(null)
        }

        ws.onmessage = (event) => {
          const message = JSON.parse(event.data)
          setMessages(prev => [...prev, message])
        }

        ws.onclose = () => {
          setIsConnected(false)
          setError('Connection Lost. Reconnecting...')
          // attempt to reconnect after 3 seconds 
          setTimeout(connectWebSocket, 3000)
        }
        ws.onerror = () => {
          setError("Connection error occurred")
        }

        return ws

      } catch (err) {
        setError("Fail to establish connection")
        setTimeout(connectWebSocket, 3000)
        return null

      }
    }

    // load initial messages 
    const loadInitialMessages = async () => {
      try {
        const response = await axios.get(`http://localhost:5004/chat/messages/${roomId}`, {
          withCredentials: true
        })
        setMessages(response.data.messages)
      } catch (err) {

        setError('Fail to load messages')
      }
    }

    loadInitialMessages()
    const ws = connectWebSocket()

    return () => {
      if (ws) ws.close()
    }


  }, [roomId])

  const sendMessage = async (content: string) => {
    if (!wsConnection || !isConnected) {
      return;
    }

    const message = {
      type: 'message',
      content,
      roomId,
      timestamp: new Date().toISOString()
    }

    try {
      wsConnection.send(JSON.stringify(message))
    } catch (err) {
      setError("Failed to send message")

    }
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
    )



  }
}


export default ChatRoom;
