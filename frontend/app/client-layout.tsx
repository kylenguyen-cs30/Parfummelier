"use client";
import { useEffect } from "react";
import { useAuth } from "./components/auth/AuthContext";
import { usePathname, useRouter } from "next/navigation";
import Header from "./components/layout/Header/Header";
import LoadingScreen from "./components/common/LoadingScreen/LoadingScreen";

// Updated routes to match your folder structure
const PUBLIC_ROUTES = [
  "/",
  "/auth/signin",
  "/auth/signup",
  "/auth/forget-password",
  "/auth/change-password",
  "/(static)/about-us",
  "/(static)/contact-us",
  "/(static)/support",
];

const AUTH_ROUTES = ["/auth/signin", "/auth/signup"];

export default function ClientLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isLoading, isAuthenticated } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  const isPublicRoute = PUBLIC_ROUTES.includes(pathname);
  const isAuthRoute = AUTH_ROUTES.includes(pathname);

  useEffect(() => {
    if (!isLoading) {
      // Redirect authenticated users trying to access auth routes
      if (isAuthenticated && isAuthRoute) {
        router.push("/(main)/main");
        return;
      }

      // Redirect authenticated users on landing page
      if (isAuthenticated && pathname === "/") {
        router.push("/(main)/main");
        return;
      }

      // Redirect unauthenticated users trying to access protected routes
      if (!isAuthenticated && !isPublicRoute) {
        router.push("/");
        return;
      }
    }
  }, [
    isLoading,
    isAuthenticated,
    pathname,
    router,
    isPublicRoute,
    isAuthRoute,
  ]);

  // Show loading screen while checking authentication
  if (isLoading) {
    return <LoadingScreen />;
  }

  // Public layout (no header)
  if (isPublicRoute) {
    return <div className="min-h-screen bg-gray-50">{children}</div>;
  }

  // Protected layout (with header)
  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <main className="container mx-auto px-4 py-8">{children}</main>
    </div>
  );
}
