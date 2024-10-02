"use client";
import React, { createContext, useState, useContext, useEffect } from "react";
// import axios from "axios";
import { useRouter } from "next/navigation";

interface AuthContextProps {
  accessToken: string | null;
  setAccessToken: (token: string | null) => void;
  isVerified: boolean;
  setIsVerified: (isVerified: boolean) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isVerified, setIsVerified] = useState<boolean>(false);

  const router = useRouter();

  // Function to handle logout
  const logout = () => {
    setAccessToken(null);
    setIsVerified(false); // reset verifications
    router.push("/signin");
  };

  return (
    <AuthContext.Provider
      value={{ accessToken, setAccessToken, logout, isVerified, setIsVerified }}
    >
      {children}
    </AuthContext.Provider>
  );
};
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("UseAuth must be used with as AuthProvider");
  }
  return context;
};
