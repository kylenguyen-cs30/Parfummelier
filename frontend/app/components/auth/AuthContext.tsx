"use client";
import React, {
  createContext,
  useState,
  useContext,
  useEffect,
  useCallback,
} from "react";
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

  //NOTE: logout context
  const logout = useCallback(async () => {
    try {
      await axios.post("/api/logout");
      setUser(null);
      setIsAuthenticated(false);
      router.push("/");
    } catch (error) {
      console.error("error logging out : ", error);
    }
  }, [router]);

  // simplified checkauth function - no need for validate token
  const checkAuth = useCallback(async () => {
    if (isAuthenticated) {
      console.log("Checking auth...");
      try {
        const tokenResponse = await axios.get("/api/getAccessToken", {
          // add silent handling of 401s
          validateStatus: (status) => status >= 200 && status < 500,
        });

        // if it is 200 for the first response
        if (tokenResponse.status === 200 && tokenResponse.data.access_token) {
          try {
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
          } catch (error) {
            // Silect handle user info fetch error

            setUser(null);
            setIsAuthenticated(false);
          }
        } else {
          // Silent handle user info fetch errors
          setUser(null);
          setIsAuthenticated(false);
        }
      } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status !== 401) {
          console.error("Auth check failed:", error);
        }
        setUser(null);
        setIsAuthenticated(false);
      }
    }
    // always set loading to false at the end
    setIsLoading(false);
  }, [isAuthenticated]);

  // Initialize the auth state on mount
  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  // set up token refresh interval when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      const refreshInterval = setInterval(
        async () => {
          try {
            const response = await axios.post(
              "http://localhost:8000/auth/refresh",
            );
            if (response.status === 200) {
              await axios.post("/api/setAccessToken", {
                access_token: response.data.access_token,
              });
            }
          } catch (error) {
            console.error("Token Refresh Failed: ", error);
            logout();
          }
        },
        14 * 60 * 1000,
      );
      return () => clearInterval(refreshInterval);
    }
  }, [isAuthenticated, logout]);

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
