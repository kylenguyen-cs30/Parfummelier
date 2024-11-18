"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import Button from "../ui/button/Button";

interface SignupFormData {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
  userName: string;
  dob: string;
}

export const SignupForm = () => {
  const [formData, setFormData] = useState<SignupFormData>({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
    userName: "",
    dob: "",
  });

  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [passwordsMatch, setPasswordsMatch] = useState(true);
  const router = useRouter();

  // Check passwords match whenever either password field changes
  useEffect(() => {
    setPasswordsMatch(formData.password === formData.confirmPassword);
  }, [formData.password, formData.confirmPassword]);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (!passwordsMatch) {
      setError("Passwords do not match");
      return;
    }

    try {
      // Remove confirmPassword before sending to API
      const { confirmPassword, ...submitData } = formData;

      const response = await axios.post(
        "http://localhost:8000/user/register",
        submitData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      if (response.status === 202) {
        setSuccessMessage("User Registered Successfully!");
        router.push("/signin");
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        setError(
          error.response?.data?.error || "An error occurred while verifying",
        );
      } else {
        setError("An error occurred");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label className="block">First Name</label>
        <input
          type="text"
          name="firstName"
          value={formData.firstName}
          onChange={handleChange}
          required
          className="w-full border rounded px-2 py-1"
        />
      </div>
      <div>
        <label className="block">Last Name</label>
        <input
          type="text"
          name="lastName"
          value={formData.lastName}
          onChange={handleChange}
          required
          className="w-full border rounded px-2 py-1"
        />
      </div>

      <div>
        <label className="block">Email</label>
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
        <label className="block">UserName</label>
        <input
          type="text"
          name="userName"
          value={formData.userName}
          onChange={handleChange}
          required
          className="w-full border rounded px-2 py-1"
        />
      </div>

      <div>
        <label className="block">Date of Birth </label>
        <input
          type="date"
          name="dob"
          value={formData.dob}
          onChange={handleChange}
          required
          className="w-full border rounded px-2 py-1"
        />
      </div>

      <div>
        <label className="block">Password</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          className="w-full border rounded px-2 py-1"
        />
      </div>
      <div>
        <label className="block">Confirm Password</label>
        <input
          type="password"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
          className={`w-full border rounded px-2 py-1 ${
            !passwordsMatch ? "border-red-500" : ""
          }`}
        />
        {!passwordsMatch && (
          <p className="text-red-500 text-sm">Passwords do not match</p>
        )}
      </div>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      {successMessage && (
        <div className="text-green-500 mb-4">{successMessage}</div>
      )}
      <Button type="submit" disabled={!passwordsMatch}>
        Sign Up
      </Button>
    </form>
  );
};
