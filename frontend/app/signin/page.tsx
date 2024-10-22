"use client";

import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Button from "../components/ui/button/Button";
import Header from "../components/ui/header/Header";
import "../styles/signin.css";

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
        "http://api-gateway:8000/auth/login",
        // "http://localhost:8000/auth/login", // TODO: Need to test this endpoint
        // "http://localhost:5002/login",
        // `${process.env.NEXT_PUBLIC_API_URL}/auth/login`,
        formData
      );

      // NOTE: login successfully
      if (response.status === 200) {
        const { access_token } = response.data;

        // ensure user access_token set in cookie
        await axios.post("/api/setAccessToken", { access_token });

        // safely push user into main-page
        router.push("/main-page");
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
    <div className="signin-container">
      <div className="signin-form-container">
        <h1 className="signin-title">Sign In</h1>
        {error && <div className="signin-error">{error}</div>}
        <form onSubmit={handleSubmit} className="signin-form">
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              className="form-input"
            />
          </div>

          <div className="form-link">
            <a href="/forget-password" className="forgot-password">
              Forgot My Password?
            </a>
          </div>

          <Button type="submit" className="signin-button">
            Sign In
          </Button>
        </form>
      </div>
    </div>
  );
};

export default SignIn;
