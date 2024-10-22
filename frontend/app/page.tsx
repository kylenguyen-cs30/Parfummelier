"use client";
import React from "react";
import Button from "./components/ui/button/Button";
import { useRouter } from "next/navigation";
import "./styles/landing-page.css";

export default function Home() {
  const router = useRouter();

  const handleClick = (type: "signin" | "signup" | "profile") => {
    console.log(`Redirecting to ${type}`);
    //TODO: if it register, router.push("/signup") otherwise, router.push("/signin")
    if (type === "signup") {
      router.push("/signup");
    } else if (type === "signin") {
      router.push("/signin");
    } else {
      router.push("/user-profile-page");
    }
  };
  return (
    <div className="full-screen-container">
      <div className="welcome-box">
        <h1 className="welcome-title">Welcome to Parfummelier</h1>
        <div className="buttons-container">
          <Button
            className="custom-button"
            type="button"
            onClick={() => handleClick("signup")}
          >
            Register
          </Button>
          <Button
            className="custom-button"
            type="button"
            onClick={() => handleClick("signin")}
          >
            Sign in
          </Button>
          <Button
            className="custom-button"
            type="button"
            onClick={() => handleClick("profile")}
          >
            Profile
          </Button>
        </div>
      </div>
    </div>
  );
}
