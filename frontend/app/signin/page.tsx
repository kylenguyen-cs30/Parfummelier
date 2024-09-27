"use client";

import React, { useState } from "react";
import axios, { AxiosError } from "axios";
import { useRouter } from "next/navigation";
import Button from "../components/ui/button";
import Header from "../components/Navbar";

const SignIn = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null); // State to store message from home API

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
    try {
      const response = await axios.post(
        "http://localhost:5001/login", //We can add API endpoint here
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        router.push("/dashboard");
      }
    } catch (error: any) {
      setError(
        error.response?.data?.error || "An error occurred while signing in."
      );
    }
  };

  const handleTestApi = async () => {
    try {
      const response = await axios.get("http://localhost:5001/");
      setMessage(response.data.message); // Assuming the response is { message: "authentication service launched !!!" }
    } catch (error: any) {
      setMessage("Failed to fetch message.");
    }
  };

  return (
    <div className="container mx-auto">
      <Header />
      <h1 className="text-2xl font-bold mb-6">Sign In</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      {message && <div className="text-green-500 mb-4">{message}</div>}{" "}
      {/* Display message */}
      {/* Sign-In Form */}
      <form onSubmit={handleSubmit}>
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

        {/* "Forget My Password" Link */}
        <div>
          <a href="/forgot-password" className="text-blue-500">
            Forgot My Password?
          </a>
        </div>

        <Button type="submit">Sign In</Button>
      </form>
      <Button type="button" onClick={handleTestApi}>
        Test API
      </Button>
    </div>
  );
};

export default SignIn;
