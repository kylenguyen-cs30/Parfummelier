"use client";
import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import axios from "axios";
import { Post } from "@/app/type/posts";
import ProtectedRoute from "@/app/components/ProtectedRoute";
import CommentSection from "@/app/components/forum/CommentSection/CommentSection";
import Image from "next/image";

// NOTE: Post User interface
interface PostUser {
  userName: string;
  firstName: string;
  lastName: string;
}

interface Post {
  id: number;
  title: string;
  content: string;
  topic: string;
  user_id: number;
  created_at: string;
  updated_at: string;
  image_urls?: string[];
  user: PostUser;
}

export default function SinglePostPage() {
  const params = useParams();
  const router = useRouter();
  const [post, setPost] = useState<Post | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // NOTE: Fetch POST API call
  useEffect(() => {
    const fetchPost = async () => {
      if (!params.id) {
        setError("No post ID provided");
        setLoading(false);
        return;
      }

      try {
        const tokenResponse = await axios.get("/api/getAccessToken");
        const { access_token } = tokenResponse.data;

        const response = await axios.get(
          `http://localhost:8000/posts/${params.id}/`,
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
            withCrendentials: true,
          },
        );

        // NOTE: Check if we got data
        if (!response.data) {
          throw new Error("No data received from server");
        }

        setPost(response.data);
        setError(null);
      } catch (err) {
        console.error("Error fetching post:", err);
        if (axios.isAxiosError(err)) {
          if (err.response?.status === 404) {
            setError("Post not found");
          } else if (err.response?.status === 401) {
            setError("Unauthorized - Please sign in again");
            router.push("/signin");
          } else {
            setError(
              `Failed to fetch post: ${err.response?.data?.detail || err.message}`,
            );
          }
        } else {
          setError("An unexpected error occurred");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [params.id, router]);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-xl">Loading post...</div>
        </div>
      </div>
    );
  }

  // NOTE: Error fetching data from the backend
  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 p-4 rounded-lg">
          <div className="text-red-700">{error}</div>
          <button
            onClick={() => router.push("/forum")}
            className="mt-4 px-4 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg transition-colors"
          >
            Return to Forum
          </button>
        </div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <div className="text-xl mb-4">Post not found</div>
          <button
            onClick={() => router.push("/forum")}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Return to Forum
          </button>
        </div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="container mx-auto px-4 py-8">
        <button
          onClick={() => router.push("/forum")}
          className="mb-6 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          ← Back to Forum
        </button>
        <div className="bg-white p-8 rounded-lg shadow-lg">
          <h1 className="text-3xl font-bold mb-4">{post?.title}</h1>

          {/* NOTE: User detail of who post the post */}
          <div className="flex items-center gap-4 text-gray-500 mb-6">
            <span>
              Posted by User {post?.user?.userName || `User ${post?.user_id}`}
            </span>
            <span>•</span>
            <span>{new Date(post?.created_at || "").toLocaleString()}</span>
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full">
              {post?.topic}
            </span>
          </div>

          <div className="prose max-w-none">
            <p className="whitespace-pre-wrap">{post.content}</p>
          </div>

          {post.image_urls && post.image_urls.length > 0 && (
            <div className="mt-6 grid grid-cols-2 gap-4">
              {post.image_urls.map((url, index) => (
                <Image
                  key={index}
                  src={url}
                  alt={`Post image ${index + 1}`}
                  className="rounded-lg w-full h-auto object-cover"
                />
              ))}
            </div>
          )}
        </div>
        {/* NOTE: Add Comment Section */}
        <div>
          <CommentSection postId={Number(params.id)} />
        </div>
      </div>
    </ProtectedRoute>
  );
}
