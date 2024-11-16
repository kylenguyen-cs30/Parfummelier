"use client";
import { useAuth } from "./components/auth/AuthContext";
import { usePathname } from "next/navigation";
import Header from "./components/layout/Header/Header";
import LoadingScreen from "./components/common/LoadingScreen/LoadingScreen";

// Updated routes to match your folder structure
const PUBLIC_ROUTES = [
  "/",
  "/signin",
  "/signup",
  "/forget-password",
  "/change-password",
  "/about-us",
  "/contact-us",
  "/support",
];

export default function ClientLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isLoading } = useAuth();
  const pathname = usePathname();

  const isPublicRoute = PUBLIC_ROUTES.includes(pathname);

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
