"use client"
import React, { useEffect, useState } from "react"
import axios from "axios"
import { useRouter } from "next/navigation"

interface User {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
}

interface ForumPost {
  id: string;
  title: string;
  content: string;
  author: string;
  timestamp: Date;
  topic: string;

}


const DUMMY_POST: ForumPost[] = [
  {
    id: '1',
    title: 'Best Summer Fragrances 2024',
    content: 'What are your favorite summer fragrances this year?',
    author: 'John Doe',
    timestamp: new Date(),
    topic: 'Summer Scents'
  },
  {
    id: '2',
    title: 'Perfume Longevity Tips',
    content: 'Share your tips for making fragrances last longer!',
    author: 'Jane Smith',
    timestamp: new Date(),
    topic: 'Tip & Tricks'
  }
]

export default function ForumPage() {
  const [users, setUsers] = useState<User[]>([])
  const [selectedUser, setSelectedUser] = useState<User | null>(null)
  const [posts] = useState<ForumPost[]>(DUMMY_POST)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter();

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        // First get the access token
        const tokenResponse = await axios.get('/api/getAccessToken');
        const { access_token } = tokenResponse.data;

        console.log('Making request with token:', access_token); // Debug log

        const response = await axios.get('http://localhost:8000/user/users', {
          headers: {
            'Authorization': `Bearer ${access_token}`,
            'Content-Type': 'application/json',
          },
          withCredentials: true
        });
        
        setUsers(response.data);
      } catch (err) {
        if (axios.isAxiosError(err)) {
          if (err.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.error('Error response:', {
              data: err.response.data,
              status: err.response.status,
              headers: err.response.headers,
            });
            
            if (err.response.status === 401) {
              setError('Please sign in to view users');
              router.push('/signin');
            } else {
              setError(`Server error: ${err.response.data?.error || 'Unknown error'}`);
            }
          } else if (err.request) {
            // The request was made but no response was received
            console.error('No response received:', err.request);
            setError('No response from server');
          } else {
            // Something happened in setting up the request
            console.error('Error setting up request:', err.message);
            setError('Failed to make request');
          }
        } else {
          console.error('Non-Axios error:', err);
          setError('An unexpected error occurred');
        }
      }
    };

    fetchUsers();
  }, [router]);

  const handleUserClick = (user: User) => {
    setSelectedUser(user);
  };

  const handleStartChat = async () => {
    if (!selectedUser) return;

    try {
      // Get the access token
      const tokenResponse = await axios.get('/api/getAccessToken');
      const { access_token } = tokenResponse.data;

      // Create chatroom with authorization header
      const response = await axios.post('http://localhost:5004/chat/chatroom', {
        participants: [selectedUser.id]
      }, {
        withCredentials: true,
        headers: {
          'Authorization': `Bearer ${access_token}`
        }
      });

      const { chatroom_id } = response.data;
      router.push(`/chat-page?roomId=${chatroom_id}`);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        setError('Please sign in to start a chat');
        router.push('/signin');
      } else {
        setError('Failed to create chat room');
        console.error('Error creating chat room:', err);
      }
    }

  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-12 gap-6">
        {/* Forum Posts - Left Side */}
        <div className="col-span-8">
          <h2 className="text-2xl font-bold mb-6">Forum Discussions</h2>
          <div className="space-y-6">
            {posts.map((post) => (
              <div
                key={post.id}
                className="bg-white p-6 rounded-lg shadow"
              >
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-xl font-semibold">{post.title}</h3>
                  <span className="text-sm text-gray-500">
                    {new Date(post.timestamp).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-gray-600 mb-4">{post.content}</p>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-500">By {post.author}</span>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                    {post.topic}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Online Users - Right Side */}
        <div className="col-span-4">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-bold mb-4">Online Users</h2>
            {error && (
              <div className="text-red-500 mb-4">{error}</div>
            )}
            <div className="space-y-2">
              {users.map((user) => (
                <div key={user.id} className="p-3 hover:bg-gray-50 rounded-lg">
                  <button
                    onClick={() => handleUserClick(user)}
                    className="w-full text-left"
                  >
                    <span className="font-medium">
                      {user.firstName} {user.lastName}
                    </span>
                  </button>

                  {selectedUser?.id === user.id && (
                    <button
                      onClick={handleStartChat}
                      className="mt-2 w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                    >
                      Direct Message
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
