import React from "react";
import "./Sidebar.css";

const Sidebar = () => {
  return (
    <div className="sidebar-container">
      <h2 className="sidebar-title">Welcome, Parfummelier</h2>
      <ul className="sidebar-list">
        <li>
          <a href="home" className="sidebar-link">
            Home
          </a>
        </li>
        <li>
          <a href="profile" className="sidebar-link">
            Profile
          </a>
        </li>
        <li>
          <a href="products" className="sidebar-link">
            Products
          </a>
        </li>
        <li>
          <a href="quiz" className="sidebar-link">
            Quiz
          </a>
        </li>
        <li>
          <a href="forum" className="sidebar-link">
            Forum
          </a>
        </li>
        <li>
          <a href="settings" className="sidebar-link">
            Settings
          </a>
        </li>
        <li>
          <a href="logout" className="sidebar-link">
            Logout
          </a>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
