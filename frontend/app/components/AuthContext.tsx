"use client";
import React, { createContext, useState, useContext, useEffect } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

interface User {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  userName: string;
}

interface AuthContextProps {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // router for page changing
  const router = useRouter();

  // simplified checkauth function - no need for validate token
  const checkAuth = async () => {
    try {
      const tokenResponse = await axios.get("/api/getAccessToken");

      if (tokenResponse.status === 200) {
        const userResponse = await axios.get(
          "http://localhost:8000/user/current-user/info",
          {
            headers: {
              Authorization: `Bearer ${tokenResponse.data.access_token}`,
            },
          },
        );

        if (userResponse.status === 200) {
          setUser(userResponse.data);
          setIsAuthenticated(true);
        }
      }
    } catch (error) {
      console.error("Auth Check Failed: ", error);
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      const refreshInterval = setInterval(refreshToken, 14 * 60 * 1000); // 14 minutes
      return () => clearInterval(refreshInterval);
    }
  }, [isAuthenticated]);

  // Refresh Token Function
  const refreshToken = async () => {
    try {
      const response = await axios.post("http://localhost:8000/auth/refresh");
      if (response.status === 200) {
        await axios.post("/api/setAccessToken", {
          access_token: response.data.access_token,
        });
      }
    } catch (error) {
      logout();
    }
  };

  //NOTE: logout context
  const logout = async () => {
    try {
      await axios.post("/api/logout");
      setUser(null);
      setIsAuthenticated(false);
      router.push("/signin");
    } catch (error) {
      console.error("error logging out: ", error);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated,
        logout,
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
