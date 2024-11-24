import React from "react";
import Image from "next/image";

interface UserProfileProps {
  user: {
    name: string;
    email: string;
    profileImage: string;
    scentId: number;
  };
}

const UserProfile: React.FC<UserProfileProps> = () => {
  // Example user data (this would typically come from props or state)
  const user = {
    name: "John Doe",
    email: "john.doe@example.com",
    profileImage: "/images/profile1.png", // Path to profile image
    scentId: 123,
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <div className="bg-white p-6 rounded-lg shadow-md max-w-sm mx-auto text-center">
          <div className="relative w-32 h-32 mx-auto mb-4">
            <Image
              src={user.profileImage}
              alt={`${user.name}'s profile image`}
              layout="fill"
              objectFit="cover"
              className="rounded-full"
            />
          </div>
          <h1 className="text-2xl font-bold mb-2">{user.name}</h1>
          <p className="text-gray-600">{user.email}</p>
          <p className="text-gray-600">Scent ID: {user.scentId}</p>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
