"use client";

import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Button from "../components/ui/button/Button";
import Header from "../components/ui/header/Header";

const SignIn = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState<string | null>(null);
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
        "http://108.225.73.225:8000/login", //We can add API endpoint here
        // "http://108.225.73.225/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      // NOTE: login successfully
      if (response.status === 200) {
        const { access_token } = response.data;

        // ensure user access_token set in cookie
        await axios.post(
          "/api/setAccessToken",
          { access_token },
          { headers: { "Content-Type": "application/json" } },
        );

        // safely push user into main-page
        router.push("/main-page");
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

  const handleTestApi = async () => {
    try {
      // Make a GET request to your API
      const response = await axios.get(
        "http://108.225.73.225:8000/auth",
        // "http://108.225.73.225/auth",
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      // Log the response to the console (or handle it in any way)
      console.log("API Response: ", response.data);
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
    <div className="container mx-auto">
      <Header />
      <h1 className="text-2xl font-bold mb-6">Sign In</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
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
          <a href="/forget-password" className="text-blue-500">
            Forgot My Password?
          </a>
        </div>

        <Button type="submit">Sign In</Button>
      </form>
      <Button type="button" onClick={handleTestApi}>
        Test Api
      </Button>
    </div>
  );
};

export default SignIn;
