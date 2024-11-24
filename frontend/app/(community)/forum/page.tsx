"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";
import ProtectedRoute from "@/app/components/ProtectedRoute";
import { Post } from "@/app/type/posts";
import Link from "next/link";
import Button from "@/app/components/ui/button/Button";
import MakePostModal from "@/app/components/forum/MakePost/MakePost";
import ForumSearch from "@/app/components/forum/ForumSearch/ForumSearch";

interface User {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
}

interface TokenPayload {
  user_id: number;
  exp: number;
}

export default function ForumPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [posts, setPosts] = useState<Post[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [currentUserId, setCurrentUserId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  // When rendering the timestamp, useEffect to handle client-side update
  const [mounted, setMounted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const [isCreatePostModalOpen, setIsCreatePostModalOpen] = useState(false);
  const [filteredPosts, setFilteredPosts] = useState<Post[]>([]);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Fetch posts from API
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const tokenResponse = await axios.get("/api/getAccessToken");
        const { access_token } = tokenResponse.data;

        const response = await axios.get("http://localhost:8000/posts", {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        setPosts(response.data);
      } catch (err) {
        console.error("Error fetching posts:", err);
        setError("Failed to fetch posts");
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  // Get current user from token
  useEffect(() => {
    const getCurrentUser = async () => {
      try {
        const tokenResponse = await axios.get("/api/getAccessToken");
        const { access_token } = tokenResponse.data;

        if (!access_token) {
          setError("No access token found");
          router.push("/signin");
          return;
        }

        const decoded = jwtDecode(access_token) as TokenPayload;
        setCurrentUserId(decoded.user_id);
        console.log("Current user ID:", decoded.user_id); // Debug log
      } catch (err) {
        console.error("Error getting current user:", err);
        setError("Failed to get current user");
        router.push("/signin");
      }
    };

    getCurrentUser();
  }, [router]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        // First get the access token
        const tokenResponse = await axios.get("/api/getAccessToken");
        const { access_token } = tokenResponse.data;

        const response = await axios.get("http://localhost:8000/user/users", {
          headers: {
            Authorization: `Bearer ${access_token}`,
            "Content-Type": "application/json",
          },
          withCredentials: true,
        });

        setUsers(response.data);
      } catch (err) {
        if (axios.isAxiosError(err)) {
          if (err.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.error("Error response:", {
              data: err.response.data,
              status: err.response.status,
              headers: err.response.headers,
            });

            if (err.response.status === 401) {
              setError("Please sign in to view users");
              router.push("/signin");
            } else {
              setError(
                `Server error: ${err.response.data?.error || "Unknown error"}`,
              );
            }
          } else if (err.request) {
            // The request was made but no response was received
            console.error("No response received:", err.request);
            setError("No response from server");
          } else {
            // Something happened in setting up the request
            console.error("Error setting up request:", err.message);
            setError("Failed to make request");
          }
        } else {
          console.error("Non-Axios error:", err);
          setError("An unexpected error occurred");
        }
      }
    };

    fetchUsers();
  }, [router]);

  const handleUserClick = (user: User) => {
    setSelectedUser(user);
  };

  const handleStartChat = async () => {
    if (!selectedUser || !currentUserId) {
      setError("Please select a user to chat with");
      return;
    }

    if (selectedUser.id === currentUserId) {
      setError("You cannot start a chat with yourself");
      return;
    }

    try {
      // Get the access token
      const tokenResponse = await axios.get("/api/getAccessToken");
      const { access_token } = tokenResponse.data;

      // Create chatroom with authorization header
      const response = await axios.post(
        "http://localhost:5004/chat/chatroom",
        {
          participants: [selectedUser.id, currentUserId], // Now we have both IDs
        },
        {
          withCredentials: true,
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        },
      );

      const { chatroom_id } = response.data;
      router.push(`/chat?roomId=${chatroom_id}`);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        setError("Please sign in to start a chat");
        router.push("/signin");
      } else {
        setError("Failed to create chat room");
        console.error("Error creating chat room:", err);
      }
    }
  };

  // NOTE: refresh post
  const handleRefreshPosts = async () => {
    try {
      const tokenResponse = await axios.get("/api/getAccessToken");
      const { access_token } = tokenResponse.data;

      const response = await axios.get("http://localhost:8000/posts", {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });

      setPosts(response.data);
    } catch (err) {
      console.error("Error fetching posts:", err);
      setError("Failed to fetch posts");
    }
  };

  return (
    <ProtectedRoute>
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-12 gap-6">
          {/* Forum Posts - Left Side */}
          <div className="col-span-8">
            <h2 className="text-2xl font-bold mb-6">Forum Discussions</h2>
            <ForumSearch
              posts={posts}
              onSearch={(filtered) => setFilteredPosts(filtered)}
            />
            {/*NOTE: Create a new Post Modal */}
            <Button onClick={() => setIsCreatePostModalOpen(true)}>
              Create Post
            </Button>
            {/* NOTE:  Post mapping */}
            {loading ? (
              <div>Loading posts...</div>
            ) : error ? (
              <div className="text-red-500">{error}</div>
            ) : (
              <div className="space-y-6">
                {(filteredPosts.length > 0 ? filteredPosts : posts).map(
                  (post) => (
                    <Link href={`/forum/post/${post.id}`} key={post.id}>
                      <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow">
                        <div className="flex justify-between items-center mb-4">
                          <h3 className="text-xl font-semibold">
                            {post.title}
                          </h3>
                          <span className="text-sm text-gray-500">
                            {new Date(post.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        <p className="text-gray-600 mb-4">
                          {post.content.length > 200
                            ? `${post.content.substring(0, 100)}...`
                            : post.content}
                        </p>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-500">
                            User ID: {post.user_id}
                          </span>
                          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                            {post.topic}
                          </span>
                        </div>
                      </div>
                    </Link>
                  ),
                )}
              </div>
            )}
          </div>

          {/* Online Users - Right Side */}
          <div className="col-span-4">
            {/* Added Inbox Navigation  */}
            <div className="bg-white p-6 rounded-lg shadow mb-6">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold">Messages</h2>
                <button
                  onClick={() => router.push("/inbox")}
                  className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center gap-2"
                >
                  <span>View Inbox</span>
                  {/* Optional: Add an icon */}
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth={1.5}
                    stroke="currentColor"
                    className="w-5 h-5"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M21.75 9v.906a2.25 2.25 0 01-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 001.183 1.981l6.478 3.488m8.839 2.51l-4.66-2.51m0 0l-1.023-.55a2.25 2.25 0 00-2.134 0l-1.022.55m0 0l-4.661 2.51m16.5 1.615a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V8.844a2.25 2.25 0 011.183-1.98l7.5-4.04a2.25 2.25 0 012.134 0l7.5 4.04a2.25 2.25 0 011.183 1.98V19.5z"
                    />
                  </svg>
                </button>
              </div>
            </div>

            {/* NOTE: Online user window  */}
            <div className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-xl font-bold mb-4">Online Users</h2>
              {error && <div className="text-red-500 mb-4">{error}</div>}
              <div className="space-y-2">
                {users.map((user) => (
                  <div
                    key={user.id}
                    className="p-3 hover:bg-gray-50 rounded-lg"
                  >
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

          {/* NOTE: Make Post Modal for the Post */}
          <MakePostModal
            isOpen={isCreatePostModalOpen}
            onClose={() => setIsCreatePostModalOpen(false)}
            onSuccess={handleRefreshPosts}
          />
        </div>
      </div>
    </ProtectedRoute>
  );
}
