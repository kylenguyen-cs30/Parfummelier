import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../components/AuthContext";

export function useRequireAuth() {
  const { user, isLoading, isAuthenticated } = useAuth();

  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/signin");
    }
  }, [isLoading, isAuthenticated, router]);
  return { user, isLoading };
}
