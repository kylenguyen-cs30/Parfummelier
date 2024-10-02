"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
// import { useRouter } from "next/router";
import axios from "axios";
import Button from "../components/ui/button";
import { useAuth } from "../components/AuthContext";

const ChangePassword = () => {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  // const { isVerified, setIsVerified } = useAuth(); // Using AuthContext
  const { resetToken, setResetToken } = useAuth();

  // NOTE: router search params

  const router = useRouter();
  // const searchParams = useSearchParams();
  // const reset_token = searchParams.get("reset-token");

  // NOTE: prevent unauthorized access
  //
  // useEffect(() => {
  //   if (!isVerified) {
  //     router.push("/");
  //   }
  // }, [isVerified, router]);

  // NOTE: handle case no reset_token
  useEffect(() => {
    console.log(resetToken);
    if (!resetToken) {
      router.push("/");
    }
  }, [resetToken, router]);

  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) {
      setError("password do not match");
      return;
    }
    try {
      const response = await axios.post(
        "http://localhost:5002/change-password",
        { resetToken, new_password: newPassword },
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      if (response.status === 200) {
        setMessage(response.data.message);
        setResetToken(null);
        // clear verifcation status after changing the password
        // setIsVerified(false);
        router.push("/login");
      }
    } catch (error: any) {
      setError("Failed to change password");
    }
  };

  return (
    <div className="mx-auto container flex flex-col">
      {error && <h1 className=" text-red-950 ">{error}</h1>}
      {message && <h1 className="text-green-900">{message}</h1>}
      <div className="border rounded shadow-lg flex flex-col justify-center items-center">
        <div className="flex flex-row justify-center">
          <h1>Change your Password</h1>
          <div>
            <label>New Password</label>
            <input
              type="password"
              name="password"
              onChange={(event) => setNewPassword(event.target.value)}
              className="border w-full px-2 py-1"
            />
          </div>

          <div>
            <label>Confirm Password</label>
            <input
              type="password"
              name="confirmPassword"
              onChange={(event) => setConfirmPassword(event.target.value)}
              className="border w-full px-2 py-1"
            />
          </div>
        </div>

        <Button type="button" onClick={handleChangePassword}>
          Submit
        </Button>
      </div>
    </div>
  );
};

export default ChangePassword;
