import React from "react";

interface Message {
  id?: string;
  _id?: string;
  sender?: string;
  content: string;
  timestamp: Date;
  userName?: string;
  firstName?: string;
  lastName?: string;
}

interface MessageListProps {
  messages: Message[];
}

const Message: React.FC<MessageListProps> = ({ messages }) => {
  // Ensure messages is an array 
  const messagesArray = Array.isArray(messages) ? messages : [];
  return (
    <div className="space-y-4 p-4">
      {messagesArray.length === 0 ? (
        <div className="text-center text-gray-500">
          No message yet
        </div>
      ) : (
        messagesArray.map((message) => (
          <div
            key={message.id || message._id}
            className="flex flex-col"
          >
            <div className="flex items-center gap-2">
              <span className="font-medium">
                {message.sender || message.userName || `${message.firstName} ${message.lastName}`}
              </span>
              <span>
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <div className="mt-1 p-3 bg-gray-100 rounded-lg">
              {message.content}
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default Message;
