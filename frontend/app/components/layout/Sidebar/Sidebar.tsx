import React from "react";
import { useAuth } from "../../AuthContext";
import Link from "next/link";
import "./Sidebar.css";

const Sidebar = () => {
  const { user, logout } = useAuth();

  // handler for logout click
  const handleLogout = async (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    await logout();
  };
  return (
    <div className="sidebar-container">
      <h2 className="sidebar-title">
        Welcome, {user?.firstName || "Parfummelier"}
      </h2>
      <ul className="sidebar-list">
        <li>
          <Link href="/main" className="sidebar-link">
            Home
          </Link>
        </li>
        <li>
          <Link href="/user-profile" className="sidebar-link">
            Profile
          </Link>
        </li>
        <li>
          <Link href="/all-products" className="sidebar-link">
            Products
          </Link>
        </li>
        <li>
          <Link href="/quiz" className="sidebar-link">
            Quiz
          </Link>
        </li>
        <li>
          <Link href="/forum" className="sidebar-link">
            Forum
          </Link>
        </li>
        <li>
          <Link href="/settings" className="sidebar-link">
            Settings
          </Link>
        </li>
        <li>
          <a href="#" onClick={handleLogout} className="sidebar-link">
            Logout
          </a>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
