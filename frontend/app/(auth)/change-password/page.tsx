"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import Button from "@/app/components/ui/button/Button";

//-------------------------------------------------------------------------//
// NOTE:
// this page help user to change the password when user passed their 2-F-A
// and verify their email.
//
// WARNING:
// this page need test before testing with network layer and API call
// traceroute.
//
//-------------------------------------------------------------------------//

const ChangePassword = () => {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  // NOTE: router search params

  const router = useRouter();

  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      const token = document.cookie
        .split("; ")
        .find((row) => row.startsWith("reset_token="))
        ?.split("=")[1];

      if (!token) {
        setError("Reset token is missing");
        return;
      }

      const response = await axios.post(
        "http://localhost:5002/change-password",
        { reset_token: token, new_password: newPassword },
      );

      if (response.status === 200) {
        setMessage(response.data.message);

        // set reset token back to null
        await axios.post("/api/setResetToken", { reset_token: null });
        router.push("/signin");
      }
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        setError(
          error.response?.data?.error || "An Error occured while verfiying",
        );
      } else {
        setError("An Error occurred");
      }
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
