"use client";

import { GetServerSideProps } from "next";
import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Button from "../components/ui/button/page";
import Header from "../components/ui/navbar/page";
import { useAuth } from "../components/AuthContext";

type SignInProps = {
  initialError?: string;
};

const SignIn = ({ initialError }: SignInProps) => {
  const { setAccessToken } = useAuth(); // AuthContext
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
        "http://localhost:5002/login", //We can add API endpoint here
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
        setAccessToken(access_token);
        router.push("/main-page");
      }
    } catch (error: any) {
      console.error("Error logging in: ", error);
      setError(
        error.response?.data?.error || "An error occurred while signing in.",
      );
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
    </div>
  );
};

export const getServerSideProps: GetServerSideProps = async (context) => {
  try {
    // Optionally check for any pre-existing cookies or tokens
    const accessToken = context.req.cookies.accessToken;
    if (accessToken) {
      return {
        redirect: {
          destination: "/main-page",
          permanent: false,
        },
      };
    }
    return {
      props: {},
    };
  } catch (error) {
    console.error("Error during SSR: ", error);
    return {
      props: {
        initialError: "Failed to load the page ",
      },
    };
  }
};

export default SignIn;
