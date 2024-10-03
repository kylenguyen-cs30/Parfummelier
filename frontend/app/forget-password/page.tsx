"use client";
import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Button from "../components/ui/button";
import Header from "../components/Header";
import { useAuth } from "../components/AuthContext";

const ForgetPassword = () => {
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  // const [resetToken, setResetToken] = useState<string | null>(null);
  const [twoFactorCode, setTwoFactorCode] = useState<string>("");
  const [email, setEmail] = useState("");
  const router = useRouter();
  const { setIsVerified } = useAuth();
  const { setResetToken } = useAuth();

  // NOTE: send data to backend email and username for verification
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setMessage(null);
    try {
      const response = await axios.post(
        "http://localhost:5002/forget-password",
        { email: email },
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

  // NOTE: verifying code for 2FA
  const handle2FASubmit = async () => {
    try {
      const response = await axios.post("http://localhost:5002/verify-code", {
        email: email,
        code: twoFactorCode,
      });

      // NOTE: Check condition
      if (response.status === 200) {
        const reset_token = response.data.reset_token;
        // setResetToken(reset_token); // Store reset TOKEN in localStorage and state
        localStorage.setItem("resetToken", reset_token);
        setIsModalOpen(false);
        router.push("/change-password");
      } else {
        setError("Invalid 2FA Code");
        return;
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
      {error && <p className="text-red-900">{error}</p>}
      {message && <p className="text-green-600">{message}</p>}

      {/* Display Message  */}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label>
          <input
            type="email"
            name="email"
            // value={formData.email}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full border rounded px-2 py-1"
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
