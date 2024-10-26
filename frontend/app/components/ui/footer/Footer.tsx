import Image from "next/image";
import "./Header.css";  // Import the CSS file

const Header = () => {
  return (
    <header className="header-container">
      <span className="header-title">Parfummelier</span>

      <div className="header-profile">
        <button className="profile-button">
          <Image
            src="/logo/Logo.webp"
            alt="Profile"
            width={32}
            height={32}
            className="profile-image"
          />
        </button>
      </div>
    </header>
  );
};

export default Header;
