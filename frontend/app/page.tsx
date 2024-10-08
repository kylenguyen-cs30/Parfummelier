"use client";
import React from "react";
import Button from "./components/ui/button/Button";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  const handleClick = (type: "signin" | "signup") => {
    //TODO: if it register, router.push("/signup") otherwise, router.push("/signin")
    if (type === "signup") {
      router.push("/signup");
    } else {
      router.push("/signin");
    }
  };
  return (
    <div className="h-screen  bg-cover flex  items-center bg-main-background">
      <div className="ml-36 ">
        <div className="justify-between flex flex-col bg-white bg-opacity-90 p-10 rounded-lg text-center shadow-lg  ">
          <h1 className="text-2xl font-semibold mb-4">
            Welcome to Parfummelier
          </h1>
          <div className="flex flex-row gap-4">
            <Button type="button" onClick={() => handleClick("signup")}>
              Register
            </Button>
            <Button type="button" onClick={() => handleClick("signin")}>
              Sign in
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
