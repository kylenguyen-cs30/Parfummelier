"use client";

import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Button from "../components/ui/button/Button";
import Header from "../components/ui/header/Header";

const SignUp = () => {
  const [formData, setFormData] = useState({
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
  const router = useRouter();

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setSuccessMessage(null);

    //Check if passwords match
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match!");
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:5001/register",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 202) {
        setSuccessMessage("User Register Successfully!");
        router.push("/signin");
      }
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        setError(
          error.response?.data?.error || "An Error occured while verfiying"
        );
      } else {
        setError("An Error occurred");
      }
    }
  };

  return (
    <div className="container mx-auto">
      <Header></Header> <h1 className="text-2xl font-bold mb-6">Sign Up</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      {successMessage && (
        <div className="text-red-500 mb-4">{successMessage}</div>
      )}
      {/* NOTE: Form for sign up */}
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
        <Button type="submit"> Sign Up</Button>
      </form>
    </div>
  );
};

export default SignUp;
