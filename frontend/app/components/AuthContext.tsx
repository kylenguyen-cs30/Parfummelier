"use client";
import React, { createContext, useState, useContext, useEffect } from "react";
// import axios from "axios";
import { useRouter } from "next/navigation";
import { document } from "postcss";

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

  const router = useRouter();

  //NOTE: logout context
  const logout = () => {
    setAccessToken(null);
    setResetToken(null);
    setIsVerified(false); // reset verifications
    document.cookie = "accessToken=; max-age=0";
    document.cookie = "resetToken=; max-age=0";
    router.push("/signin");
  };

  // NOTE: Temporarily store in localStorage
  // Save resetToken to localStorage
  //
  // const setResetToken = (token: string | null) => {
  //   if (token) {
  //     localStorage.setItem("resetToken", token);
  //   } else {
  //     localStorage.removeItem("resetToken");
  //   }
  //   setResetTokenState(token);
  // };
  //

  // Load resetToken from localStorage when the app starts
  // useEffect(() => {
  //   const token = localStorage.getItem("resetToken");
  //   if (token) {
  //     setResetTokenState(token);
  //   }
  // }, []);

  // NOTE: localStorage for accessToken
  //
  // const setAccessToken = (token: string | null) => {
  //   if (token) {
  //     localStorage.setItem("accessToken", token);
  //   } else {
  //     localStorage.removeItem("accessToken");
  //   }
  //   setAccessTokenState(token);
  // };

  // useEffect(() => {
  //   const token = localStorage.getItem("accessToken");
  //   if (token) {
  //     setAccessTokenState(token);
  //   }
  // }, []);

  // NOTE: Cookie Implementation
  const setResetToken = (token: string | null) => {
    if (token) {
      document.cookie = `resetToken=${token}; max-age=86400`;
    } else {
      document.cookie = "resetToken=;max-age=0";
    }
    setResetTokenState(token);
  };

  useEffect(() => {
    const token = document.cookie
      .split("; ")
      .find((row) => startsWith("resetToken="))
      ?.split("=")[1];
    if (token) {
      setResetTokenState(token);
    }
  }, []);

  const setAccessToken = (token: string | null) => {
    if (token) {
      document.cookie = `accessToken=${token}; max-age=86400`;
    } else {
      document.cookie = "accessToken=; max-age=0";
    }
    setAccessTokenState(token);
  };

  useEffect(() => {
    const token = document.cookie
      .split("; ")
      .find((row) => startsWith("resetToken="))
      ?.split("=")[1];
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
