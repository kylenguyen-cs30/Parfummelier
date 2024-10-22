import React from "react";
import Image from "next/image";
import "../styles/user-profile.css"; // Import specific CSS for user profile page

const UserProfile = () => {
  // Example user data (this would typically come from props or state)
  const user = {
    name: "John Doe",
    email: "john.doe@example.com",
    profileImage: "/images/profile1.png",
    note: "Rose",
    accord: "Floral",
    season: "Spring",
    scents: "Light and Fresh",
    collection: "Luxury Collection",
    product: "Rose Petal Elegance",
  };

  return (
    <div className="user-profile-container">
      <div className="user-profile-card">
        <div className="user-profile-image">
          <Image
            src={user.profileImage}
            alt={`${user.name}'s profile image`}
            layout="fill"
            objectFit="cover"
            className="rounded-full"
          />
        </div>
        <h1 className="user-profile-name">{user.name}</h1>
        <p className="user-profile-email">{user.email}</p>
        <p className="user-profile-info">
          <strong>Note:</strong> {user.note}
        </p>
        <p className="user-profile-info">
          <strong>Accord:</strong> {user.accord}
        </p>
        <p className="user-profile-info">
          <strong>Season:</strong> {user.season}
        </p>
        <p className="user-profile-info">
          <strong>Scents:</strong> {user.scents}
        </p>
        <p className="user-profile-info">
          <strong>Collection:</strong> {user.collection}
        </p>
        <p className="user-profile-info">
          <strong>Product:</strong> {user.product}
        </p>
      </div>
    </div>
  );
};

export default UserProfile;
