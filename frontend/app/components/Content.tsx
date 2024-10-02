import React, { ReactNode } from "react";

interface ContentProps {
  children: ReactNode;
}

const Content: React.FC<ContentProps> = ({ children }) => {
  return (
    <div className="flex justify-center items-center h-64 bg-gray-200">
      {children}
    </div>
  );
};

export default Content;
