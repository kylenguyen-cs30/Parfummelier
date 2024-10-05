"use client";
import { useEffect, useState } from "react";
import axios from "axios";

export default function Profile() {
  const [userInfo, setUserInfo] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch user data from the backend
  useEffect(() => {
    axios
      .get("") // Adjust the API endpoint if necessary
      .then((response) => {
        setUserInfo(response.data); // Store user data
        setLoading(false); // Set loading to false once data is fetched
      })
      .catch((err) => {
        console.error("Error fetching user details:", err);
        setError("Failed to fetch user details");
        setLoading(false);
      });
  }, []);

  // Loading state
  if (loading) return <p>Loading...</p>;

  // Error state
  if (error) return <p>{error}</p>;

  // Render the user information
  return (
    <div className="container mx-auto">
      <h1 className="text-2xl font-bold mb-6">User Profile</h1>
      {userInfo && (
        <div>
          <p>
            <strong>Email:</strong> {userInfo.email}
          </p>
          <p>
            <strong>First Name:</strong> {userInfo.firstName}
          </p>
          <p>
            <strong>Last Name:</strong> {userInfo.lastName}
          </p>
          <p>
            <strong>Date of Birth:</strong> {userInfo.dob}
          </p>
          <p>
            <strong>Scent ID:</strong> {userInfo.scent_id}
          </p>
        </div>
      )}
    </div>
  );
}
