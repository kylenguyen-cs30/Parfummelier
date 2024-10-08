const Sidebar = () => {
  return (
    <div
      style={{
        width: "200px",
        background: "#2c3e50",
        padding: "20px",
        height: "100vh",
        color: "white",
      }}
    >
      <h2 style={{ marginBottom: "40px" }}>Dashboard</h2>
      <ul style={{ listStyle: "none", padding: 0 }}>
        <li>
          <a href="home" style={{ color: "white" }}>
            Home
          </a>
        </li>
        <li>
          <a href="profile" style={{ color: "white" }}>
            Profile
          </a>
        </li>
        <li>
          <a href="products" style={{ color: "white" }}>
            Products
          </a>
        </li>
        <li>
          <a href="quiz" style={{ color: "white" }}>
            Quiz
          </a>
        </li>
        <li>
          <a href="forum" style={{ color: "white" }}>
            Forum
          </a>
        </li>
        <li>
          <a href="settings" style={{ color: "white" }}>
            Settings
          </a>
        </li>
        <li>
          <a href="logout" style={{ color: "white" }}>
            Logout
          </a>
        </li>
      </ul>
    </div>
  );
};
export default Sidebar;
