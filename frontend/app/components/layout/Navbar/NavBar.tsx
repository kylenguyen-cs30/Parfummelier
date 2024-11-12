import React from "react";
import "./Navbar.css";

interface NavbarProps {
  children: React.ReactNode;
}

const Navbar: React.FC<NavbarProps> = ({ children }) => {
  const text = "Parfummelier store";
  return (
    <nav className="navbar-container">
      <div className="navbar-content">
        <h1 className="navbar-title">{text}</h1>
        <div className="navbar-children">{children}</div>
      </div>
    </nav>
  );
};

export default Navbar;
