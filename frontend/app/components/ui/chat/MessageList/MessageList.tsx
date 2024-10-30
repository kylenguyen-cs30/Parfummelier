import React from "react";

interface Message {
  id: string;
  sender: string;
  content: string;
  timestamp: Date;
}

interface MessageListProps {
  messages: Message[];
}

const Message: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="space-y-4 p-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className="flex flex-col"
        >
          <div className="flex items-center gap-2">
            <span className="font-medium">{message.sender}</span>
            <span className="text-sm text-gray-500">
              {new Date(message.timestamp).toLocaleTimeString()}
            </span>
          </div>
          <div className="mt-1 p-3 bg-gray-100 rounded-lg">
            {message.content}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Message;
