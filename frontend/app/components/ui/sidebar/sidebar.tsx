import React, { useState } from "react";
import "./sidebar.css";
import "boxicons/css/boxicons.min.css";

const DashboardSidebar = () => {
  // State for sidebar visibility
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // State for dark mode
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode);

    // Apply dark mode class to the body
    if (!isDarkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
  };

  return (
    <nav className={`sidebar ${isSidebarOpen ? "open" : "closed"}`}>
      <header>
        <div className="image-text">
          <div className="text header-text">
            <span className="name">Parfummelier</span>
            <span className="prof">Dashboard</span>
          </div>
        </div>
        <i
          className={`bx bx-chevron-${isSidebarOpen ? "left" : "right"} toggle`}
          onClick={toggleSidebar}
        ></i>
      </header>

      <div className="menu-bar">
        <div className="menu">
          <li className="search-box">
            <i className="bx bx-search icon"></i>
            <input type="search" placeholder="Search..." />
          </li>
          <ul className="menu-links">
            <li className="nav-link">
              <a href="#">
                <i className="bx bx-home-alt icon"></i>
                <span className="text nav-text">Home</span>
              </a>
            </li>
            <li className="nav-link">
              <a href="#">
                <i className="bx bx-child icon"></i>
                <span className="text nav-text">Profile</span>
              </a>
            </li>
            <li className="nav-link">
              <a href="#">
                <i className="bx bx-chat icon"></i>
                <span className="text nav-text">Forum</span>
              </a>
            </li>
            <li className="nav-link">
              <a href="#">
                <i className="bx bx-question-mark icon"></i>
                <span className="text nav-text">Quiz</span>
              </a>
            </li>
            <li className="nav-link">
              <a href="#">
                <i className="bx bx-cog icon"></i>
                <span className="text nav-text">Setting</span>
              </a>
            </li>
            <li className="nav-link">
              <a href="#">
                <i className="bx bx-log-out icon"></i>
                <span className="text nav-text">Logout</span>
              </a>
            </li>

            <div className="menu-separator"></div>

            <li className="mode">
              <div className="moon-sun">
                <i className="bx bx-moon icon moon"></i>
              </div>
              <span className="mode-text">
                {isDarkMode ? "Light Mode" : "Dark Mode"}
              </span>

              {/* Toggle Switch */}
              <div className="toggle-switch" onClick={toggleDarkMode}>
                <span className={`switch ${isDarkMode ? "dark" : ""}`}></span>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default DashboardSidebar;
