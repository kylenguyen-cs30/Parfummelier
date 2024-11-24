"use client";
import React, { useEffect } from "react";
import Button from "./components/ui/button/Button";
import { useRouter } from "next/navigation";
import { useAuth } from "./components/auth/AuthContext";
import LoadingScreen from "./components/common/LoadingScreen/LoadingScreen";

export default function Home() {
  const router = useRouter();
  const { isLoading, isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.replace("/main");
    }
  }, [isLoading, isAuthenticated, router]);

  // Show loading screen while checking auth
  if (isLoading || isAuthenticated) {
    return <LoadingScreen />;
  }

  const handleClick = (type: "signin" | "signup") => {
    router.push(`/${type}`);
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
