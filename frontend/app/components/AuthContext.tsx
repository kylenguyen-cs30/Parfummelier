"use client";
import React, { createContext, useState, useContext, useEffect } from "react";
import { useRouter } from "next/navigation";

interface AuthContextProps {
  accessToken: string | null;
  setAccessToken: (token: string | null) => void;
  isVerified: boolean;
  setIsVerified: (isVerified: boolean) => void;
  resetToken: string | null;
  setResetToken: (token: string | null) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [accessToken, setAccessTokenState] = useState<string | null>(null);
  const [isVerified, setIsVerified] = useState<boolean>(false);
  const [resetToken, setResetTokenState] = useState<string | null>(null);

  // router for page changing
  const router = useRouter();

  //NOTE: logout context
  const logout = () => {
    setAccessToken(null);
    // setResetToken(null); // reset token
    setIsVerified(false); // reset verifications
    router.push("/signin");
  };

  // NOTE: Temporarily store in localStorage
  // Save resetToken to localStorage
  const setResetToken = (token: string | null) => {
    if (token) {
      localStorage.setItem("resetToken", token);
    } else {
      localStorage.removeItem("resetToken");
    }
    setResetTokenState(token);
  };

  // Load resetToken from localStorage when the app starts
  useEffect(() => {
    const token = localStorage.getItem("resetToken");
    if (token) {
      setResetTokenState(token);
    }
  }, []);

  // NOTE: localStorage for accessToken

  const setAccessToken = (token: string | null) => {
    if (token) {
      localStorage.setItem("accessToken", token);
    } else {
      localStorage.removeItem("accessToken");
    }
    setAccessTokenState(token);
  };

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      setAccessTokenState(token);
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        accessToken,
        setAccessToken,
        logout,
        isVerified,
        setIsVerified,
        resetToken,
        setResetToken,
      }}
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
