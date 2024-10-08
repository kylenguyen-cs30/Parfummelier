"use client";
import React, { createContext, useState, useContext } from "react";
import { useRouter } from "next/navigation";

interface AuthContextProps {
  isVerified: boolean;
  setIsVerified: (isVerified: boolean) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isVerified, setIsVerified] = useState<boolean>(false);

  // router for page changing
  const router = useRouter();

  //NOTE: logout context
  const logout = async () => {
    try {
      await fetch("/api/logout", { method: "POST" });
      setIsVerified(false);
      router.push("/signin");
    } catch (error) {
      console.error("error logging out: ", error);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        logout,
        isVerified,
        setIsVerified,
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
// // Load resetToken from localStorage when the app starts
// useEffect(() => {
//   const token = localStorage.getItem("resetToken");
//   if (token) {
//     setResetTokenState(token);
//   }
// }, []);
//
//
// const setAccessToken = (token: string | null) => {
//   if (token) {
//     localStorage.setItem("accessToken", token);
//   } else {
//     localStorage.removeItem("accessToken");
//   }
//   setAccessTokenState(token);
// };
//
// useEffect(() => {
//   const token = localStorage.getItem("accessToken");
//   if (token) {
//     setAccessTokenState(token);
//   }
// }, []);
//
