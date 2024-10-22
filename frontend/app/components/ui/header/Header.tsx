import React from "react";
import Image from "next/image";
import "../../ui/header/header.css"; // Import CSS

const Header = () => {
  return (
    <header className="header-container">
      <span className="header-title">Parfummelier</span>

      {/* Right side: Profile Button */}
      <div className="profile-button">
        <Image
          src="/logo/Logo.webp"
          alt="Profile"
          width={32} // Adjust width here for profile image
          height={32} // Adjust height here for profile image
          className="rounded-full"
        />
      </div>
    </header>
  );
};

export default Header;
