import React, { ReactNode } from "react";
import "./Content.css"; // Import the CSS file

interface ContentProps {
  children: ReactNode;
}

const Content: React.FC<ContentProps> = ({ children }) => {
  return (
    <div className="content-container text-orange-100 text-3xl flex w-auto items-center justify-center flex-col">
      {" "}
      {/* Use new CSS class */}
      {children}
    </div>
  );
};

export default Content;
