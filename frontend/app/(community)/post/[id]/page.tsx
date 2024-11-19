"use client";
import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import axios from "axios";
import { Post } from "@/app/type/posts";
import ProtectedRoute from "@/app/components/ProtectedRoute";

export default function SinglePostPage() {
  const params = useParams();
  const router = useRouter();
  const [post, setPost] = useState<Post | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const tokenResponse = await axios.get("/api/getAccessToken");
        const { access_token } = tokenResponse.data;

        const response = await axios.get(
          `http://localhost:8000/posts/${params.id}`,
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          },
        );

        setPost(response.data);
      } catch (err) {
        console.error("Error fetching post:", err);
        setError("Failed to fetch post");
      } finally {
        setLoading(false);
      }
    };

    if (params.id) {
      fetchPost();
    }
  }, [params.id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="text-red-500">{error}</div>;
  if (!post) return <div>Post not found</div>;

  return (
    <ProtectedRoute>
      <div className="container mx-auto px-4 py-8">
        <button
          onClick={() => router.back()}
          className="mb-6 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          ← Back to Forum
        </button>

        <div className="bg-white p-8 rounded-lg shadow-lg">
          <h1 className="text-3xl font-bold mb-4">{post.title}</h1>

          <div className="flex items-center gap-4 text-gray-500 mb-6">
            <span>Posted by User {post.user_id}</span>
            <span>•</span>
            <span>{new Date(post.created_at).toLocaleString()}</span>
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full">
              {post.topic}
            </span>
          </div>

          <div className="prose max-w-none">
            <p>{post.content}</p>
          </div>

          {post.image_urls && post.image_urls.length > 0 && (
            <div className="mt-6 grid grid-cols-2 gap-4">
              {post.image_urls.map((url, index) => (
                <img
                  key={index}
                  src={url}
                  alt={`Post image ${index + 1}`}
                  className="rounded-lg w-full h-auto object-cover"
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
