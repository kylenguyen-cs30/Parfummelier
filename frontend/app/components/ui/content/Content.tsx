import React, { ReactNode } from "react";
import "./Content.css";  // Import the CSS file

interface ContentProps {
  children: ReactNode;
}

const Content: React.FC<ContentProps> = ({ children }) => {
  return (
    <div className="content-container">  {/* Use new CSS class */}
      {children}
    </div>
  );
};

export default Content;
