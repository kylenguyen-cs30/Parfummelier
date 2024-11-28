import React, { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../../auth/AuthContext";

interface User {
  user_id: number;
  userName: string;
  firstName: string;
  lastName: string;
}

interface Comment {
  id: number;
  post_id: number;
  user_id: number;
  content: string;
  parent_id: number | null;
  created_at: string;
  updated_at: string;
  user?: User;
  replies: Comment[];
}

interface CommentFormProps {
  postId: number;
  parentId?: number | null;
  onCommentAdded: () => void;
  onCancel?: () => void;
}

//NOTE: This is the comment form for user to enter comment or reply
const CommentForm: React.FC<CommentFormProps> = ({
  postId,
  parentId,
  onCommentAdded,
  onCancel,
}) => {
  const [content, setContent] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) {
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const tokenResponse = await axios.get("/api/getAccessToken");
      const { access_token } = tokenResponse.data;

      //NOTE: send request to the forum service and along the parentId
      //if this is a reply. if this is a regular comment then it will add a comment

      await axios.post(
        `http://localhost:8000/comments/${postId}/`,
        {
          content: content.trim(),
          parent_id: parentId || null,
        },
        {
          headers: {
            Authorization: `Bearer ${access_token}`,
            "Content-Type": "application/json",
          },
        },
      );

      setContent("");
      onCommentAdded();

      if (onCancel) {
        onCancel();
      }
    } catch (err) {
      console.error("Error posting comment: ", err);
      setError(err instanceof Error ? err.message : "Failed to post comment");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4 space-y-4">
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Write your comment..."
        className="w-full p-3 border rounded-lg focus:ring-blue-500 focus:border-blue-500"
        rows={3}
      ></textarea>
      {error && <p className="text-red-500 text-sm">{error}</p>}

      <div className="flex gap-2">
        <button
          type="submit"
          disabled={isSubmitting || !content.trim()}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {isSubmitting ? "Posting..." : "Post Comment"}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-200  text-gray-700 rounded-lg hover:bg-gray-300"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

const CommentItem: React.FC<{
  comment: Comment;
  postId: number;
  onCommentAdded: () => void;
}> = ({ comment, postId, onCommentAdded }) => {
  const [showReplyForm, setShowReplyForm] = useState(false);
  const { user } = useAuth();

  // heper function to get initials
  const getInitials = (firstName?: string, lastName?: string) => {
    if (!firstName && !lastName) {
      return "U";
    }
    return `${firstName?.[0] || ""}${lastName?.[0] || ""}`;
  };

  return (
    <div className="border-l-2 border-gray-200 pl-3 mb-4">
      <div className="bg-gray-50 p-4 rounded-lg">
        <div className="flex items-center gap-3 mb-2">
          {/* Profile Picture */}
          <div className="w-8 h-8 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full flex items-center justify-center text-white text-sm font-bold">
            {getInitials(comment.user?.firstName, comment.user?.lastName)}
          </div>

          <div className="flex flex-col">
            <span className="font-medium">
              {comment.user?.userName || `User ${comment.user_id}`}
            </span>
            <span className="text-gray-500 text-xs">
              {new Date(comment.created_at).toLocaleString()}
              {comment.updated_at !== comment.created_at && (
                <span className="text-gray-400 ml-2">(edited)</span>
              )}
            </span>
          </div>
        </div>

        <div className="ml-11">
          {" "}
          {/* Align content with the username */}
          <p className="text-gray-700 whitespace-pre-wrap">{comment.content}</p>
          {user && (
            <button
              className="text-blue-600 text-sm mt-2 hover:underline"
              onClick={() => setShowReplyForm(!showReplyForm)}
            >
              Reply
            </button>
          )}
          {showReplyForm && (
            <CommentForm
              postId={postId}
              parentId={comment.id}
              onCommentAdded={() => {
                onCommentAdded();
                setShowReplyForm(false);
              }}
              onCancel={() => setShowReplyForm(false)}
            />
          )}
        </div>
      </div>

      {comment.replies && comment.replies.length > 0 && (
        <div className="ml-8 mt-4">
          {comment.replies.map((reply) => (
            <CommentItem
              key={reply.id}
              comment={reply}
              postId={postId}
              onCommentAdded={onCommentAdded}
            />
          ))}
        </div>
      )}
    </div>
  );
};

const CommentSection: React.FC<{ postId: number }> = ({ postId }) => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  const fetchComments = async () => {
    try {
      const tokenResponse = await axios.get("/api/getAccessToken");
      const { access_token } = tokenResponse.data;
      const response = await axios.get(
        `http://localhost:8000/comments/post/${postId}/`,
        {
          headers: {
            Authorization: `Bearer ${access_token}`,
            "Content-Type": "application/json",
          },
          withCredentials: true, // Add this to handle cookie properly
        },
      );
      setComments(response.data || []);
      setError(null);
    } catch (err) {
      console.error("Error fetching comments: ", err);
      if (axios.isAxiosError(err)) {
        console.error("Error details :", {
          status: err.response?.status,
          data: err.response?.data,
          headers: err.response?.headers,
        });

        // NOTE: Handle specific error cases
        if (err.response?.status === 404) {
          setComments([]);
          setError(null);
        } else if (err.response?.status === 422) {
          setError("Invalid request. Please check input paramenters.");
        } else if (err.response?.status === 401) {
          setError("Authentication failed. Please log in again.");
        } else {
          setError("Failed to load comments");
        }
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComments();
  }, [postId]);

  if (loading) {
    return (
      <div className="mt-8 flex justify-center items-center">
        <div className="mt-8 text-center">Loading comments...</div>;
      </div>
    );
  }

  if (error) {
    return (
      <div className="mt-8 bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="mt-8 text-red-500 text-center">{error}</div>
      </div>
    );
  }

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-6">Comments</h2>
      {/*NOTE: fetching comments components */}
      {user && (
        <CommentForm
          postId={postId}
          onCommentAdded={fetchComments}
        ></CommentForm>
      )}

      <div className="mt-8 space-y-6">
        {comments.length === 0 ? (
          <p className="text-gray-500 text-center">
            No Comments yet. Be the first{" "}
          </p>
        ) : (
          comments.map((comment) => (
            <CommentItem
              key={comment.id}
              comment={comment}
              postId={postId}
              onCommentAdded={fetchComments}
            ></CommentItem>
          ))
        )}
      </div>
    </div>
  );
};

export default CommentSection;
