"use client"
import React, { useEffect, useState } from "react"
import axios from "axios"
import { useRouter } from "next/navigation"
import { timeStamp } from "console";

interface ChatPreview {
  chatroom: string;
  other_user: {
    id: number,
    userName: string,
    firstName: string,
    lastName: string,
  };
  latest_message?: {
    content: string;
    timestamp: string;
  };
  last_message_at: string;
}


export default function InboxPage() {
  const [chatrooms, setChatrooms] = useState<ChatPreview[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    const fetchChatrooms = async () => {

      try {
        const tokenResponse = await axios.get('/api/getAccessToken')
        const { access_token } = tokenResponse.data

        const response = await axios.get(
          'http://localhost:5004/chat/user/chatrooms',
          {
            headers: {
              Authorization: `Bearer ${access_token}`
            },
            withCredentials: true
          }
        );
        setChatrooms(response.data.chatrooms)
      } catch (err) {
        console.error('Failed to load chatrooms:', err)
        setError('Failed tp load conversations')
      } finally {
        setLoading(false)
      }
    }

    fetchChatrooms()
  }, [])


  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date();
    if (date.toDateString() === now.toDateString()) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    return date.toLocaleDateString()
  }

}

