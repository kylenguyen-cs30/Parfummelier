import { useAuth } from "./components/auth/AuthContext";
import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";
import Header from "./components/layout/Header/Header";
import LoadingScreen from "./components/common/LoadingScreen/LoadingScreen";

const PUBLIC_ROUTES = [
  "/",
  "/signin",
  "/signup",
  "/forget-password",
  "/about-us",
  "/contact-us",
  "/support",
];

const PROTECTED_ROUTES = [
  "/main",
  "/chat",
  "/forum",
  "/inbox",
  "/timeline",
  "/history",
  "/quiz",
  "/settings",
  "/user-profile",
];

export default function ClientLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isLoading, isAuthenticated, refreshToken } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    const handleAuthRedirect = async () => {
      if (!isLoading) {
        if (isAuthenticated && PUBLIC_ROUTES.includes(pathname)) {
          router.replace("/main");
        } else if (!isAuthenticated && PROTECTED_ROUTES.includes(pathname)) {
          const refreshed = await refreshToken();
          if (!refreshed) {
            router.replace("/");
          }
        }
      }
    };

    handleAuthRedirect();
  }, [isLoading, isAuthenticated, pathname, refreshToken, router]);

  if (isLoading) {
    return <LoadingScreen />;
  }

  const isPublicRoute = PUBLIC_ROUTES.includes(pathname);

  if (isPublicRoute) {
    return <div className="min-h-screen bg-gray-50">{children}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <main className="container mx-auto px-4 py-8">{children}</main>
    </div>
  );
}
