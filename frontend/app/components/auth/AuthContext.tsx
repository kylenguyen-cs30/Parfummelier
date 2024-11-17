"use client";
import React, {
  createContext,
  useState,
  useContext,
  useEffect,
  useCallback,
} from "react";
import { useRouter, usePathname } from "next/navigation";
import { AuthState } from "../../type/auth";
import axios from "axios";

interface AuthContextProps extends AuthState {
  logout: () => Promise<void>;
  refreshToken: () => Promise<boolean>;
  login: (email: string, password: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  // Set state of the user authentication
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
  });

  // const [user, setUser] = useState<User | null>(null);
  // const [isLoading, setIsLoading] = useState(true);
  // const [isAuthenticated, setIsAuthenticated] = useState(false);
  // router for page changing
  const router = useRouter();
  const pathname = usePathname();

  //NOTE: logout context
  const logout = useCallback(async () => {
    try {
      await axios.post("/api/logout");
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
      });
      router.push("/");
    } catch (error) {
      console.error("error logging out : ", error);
    }
  }, [router]);

  // NOTE: Refresh token function
  const refreshToken = useCallback(async (): Promise<boolean> => {
    try {
      // refresh token will be automatically included in the request
      // as an HTTP-only cookie because the endpoint matches the cookie's path
      const response = await axios.post(
        "http://localhost:8000/auth/refresh",
        {}, // empty body since there is no payload
        {
          withCredentials: true,
        },
      );

      if (response.status === 200) {
        const { access_token } = response.data;
        await axios.post("/api/setAccessToken", { access_token });

        // update user state if needed
        const userResponse = await axios.get(
          "http://localhost:8000/user/current-user/info",
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          },
        );

        if (userResponse.status === 200) {
          setState((prev) => ({
            ...prev,
            user: userResponse.data,
            isAuthenticated: true,
          }));
        }

        return true;
      }
      return false;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 401) {
          // refresh token expired or invalid
          setState({
            user: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      }
      console.error(`Failed to refresh token ${error}`);
      return false;
    }
  }, []);

  // NOTE: Authentication Status Checker
  const checkAuth = useCallback(async () => {
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
          setState({
            user: userResponse.data,
            isAuthenticated: true,
            isLoading: false,
          });
          return;
        }
      }

      // NOTE: try refresh token if the access token fail
      const refreshed = await refreshToken();
      if (refreshed) {
        //retry getting user info after refresh
        const userResponse = await axios.get(
          "http://localhost:8000/user/current-user/info",
          {
            headers: {
              Authorization: `Bearer ${(await axios.get("/api/getAccessToken")).data.access_token}`,
            },
          },
        );
        if (userResponse.status === 200) {
          setState({
            user: userResponse.data,
            isAuthenticated: true,
            isLoading: false,
          });
          return;
        }
      }

      setState({ user: null, isAuthenticated: false, isLoading: false });
    } catch (error) {
      console.error(`Error in refresh new tokne ${error}`);
      setState({ user: null, isAuthenticated: false, isLoading: false });
    }
  }, [refreshToken]);

  // NOTE: login function
  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post("http://localhost:8000/auth/login", {
        email,
        password,
      });

      if (response.status === 200) {
        const { access_token, user } = response.data;
        await axios.post("/api/setAccessToken", { access_token });

        setState({
          user,
          isAuthenticated: true,
          isLoading: false,
        });

        router.push("/main");
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(
          error.response?.data?.error || "An error occured while logging in",
        );
      }
      throw new Error("An error occured");
    }
  };

  // Initialize the auth state on mount
  useEffect(() => {
    checkAuth();
  }, [checkAuth, pathname]);

  // set up token refresh interval when authenticated
  useEffect(() => {
    if (state.isAuthenticated) {
      const refreshInterval = setInterval(
        async () => {
          const refreshed = await refreshToken();
          if (!refreshed) {
            logout();
          }
        },
        14 * 60 * 1000,
      );
      return () => clearInterval(refreshInterval);
    }
  }, [state.isAuthenticated, logout, refreshToken]);

  return (
    <AuthContext.Provider
      value={{
        ...state,
        login,
        logout,
        refreshToken,
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
