"user server";
import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/router";
import Button from "../components/ui/button";
import Header from "../components/Header";
import { useAuth } from "../components/AuthContext";

const ForgetPassword = () => {
  const [formData, setFormData] = useState({
    email: "",
    userName: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [resetToken, setResetToken] = useState<string | null>(null);
  const [twoFactorCode, setTwoFactorCode] = useState<string>("");
  const router = useRouter();
  const { setIsVerified } = useAuth();

  // NOTE: map input
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  // NOTE: send data to backend email and username for verification
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    try {
      const response = await axios.post(
        "http://localhost:5002/forget-password/",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      // NOTE: found result
      if (response.status === 200) {
        setIsVerified(true);
        setIsModalOpen(true);
        setMessage(response.data.message);
      } else {
        console.log("email not found");
      }
    } catch (error: any) {
      setError(
        error.response?.data?.error || "An Error occured while verfiying",
      );
    }
  };

  // NOTE:
  const handle2FASubmit = async () => {
    try {
      const response = await axios.post(
        "http://localhost:5003/verify-code",
        {
          email: formData.email,
          code: twoFactorCode,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      // NOTE: Check condition
      if (response.status === 200) {
        const reset_token = response.data.reset_token;
        setResetToken(reset_token);
        setIsModalOpen(false);

        // navigate to change-password page with reset_token and user_id
        router.push({
          pathname: "/change-password",
          query: {
            reset_token: reset_token,
          },
        });
      } else {
        setError("Invalid 2FA Code");
      }
    } catch (error: any) {
      setError("An Error occured while verifying 2FA code");
    }
  };

  const handleTestApi = async () => {
    try {
      const response = await axios.get("http://localhost:5002/");
      if (response.status === 200) {
        alert("backend is online");
      }
    } catch (error: any) {
      setMessage("Failed to fetch message");
    }
  };

  return (
    <div className="container mx-auto">
      {/* 2FA Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-lg font-bold mb-4">Enter 6-Digit Code</h2>
            <input
              type="text"
              maxLength={6}
              value={twoFactorCode}
              onChange={(e) => setTwoFactorCode(e.target.value)}
              className="w-full border rounded px-2 py-1 mb-4"
              placeholder="Enter 6-digit code"
            />
            <Button onClick={handle2FASubmit}>Verify Code</Button>
          </div>
        </div>
      )}
      {/* TODO: we need Modal for entering 6 digits code for 2-F-A  */}
      <Header />
      <h1>Forget Password</h1>
      {error && <p>{error}</p>}
      {/* Display Message  */}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full border rounded px-2 py-1"
          />
        </div>
        <div>
          <label>User Name</label>
          <input
            type="text"
            name="userName"
            value={formData.userName}
            onChange={handleChange}
            required
            className="w-full border rounded py-2 px-1"
          />
        </div>
        <Button type="submit">Submit</Button>
      </form>
      <Button type="button" onClick={handleTestApi}>
        Test Connection
      </Button>
    </div>
  );
};

export default ForgetPassword;
