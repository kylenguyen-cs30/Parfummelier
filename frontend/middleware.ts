import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { jwtVerify } from "jose";

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
  "/main/*",
  "/chat/*",
  "/forum/*",
  "/inbox/*",
  "/timeline/*",
  "/history/*",
  "/quiz/*",
  "/settings/*",
  "/user-profile/*",
  "/product/*",
];

export async function middleware(request: NextRequest) {
  console.log("Middleware path: ", request.nextUrl.pathname);
  console.log("Cookies: ", request.cookies.getAll());
  const path = request.nextUrl.pathname;

  // Skip middleware for static files and API routes
  if (
    path.includes("/_next") ||
    path.includes("/api") ||
    path.match(/\.(jpg|jpeg|png|gif|ico|svg|css|js)$/)
  ) {
    return NextResponse.next();
  }

  const isProtectedPath = (path: string) => {
    return PROTECTED_ROUTES.some((route) => {
      if (route.includes("*")) {
        return path.startsWith(route.replace("*", ""));
      }
      return path === route;
    });
  };

  const accessToken = request.cookies.get("access_token")?.value;
  const resetToken = request.cookies.get("reset_token")?.value;

  // Special handling for change-password route
  if (path === "/change-password") {
    if (!resetToken) {
      return NextResponse.redirect(new URL("/forget-password", request.url));
    }
    return NextResponse.next();
  }

  // Verify access token
  let isValidToken = false;
  if (accessToken) {
    try {
      const secret = new TextEncoder().encode(process.env.JWT_SECRET);
      await jwtVerify(accessToken, secret);
      isValidToken = true;
    } catch {
      isValidToken = false;
    }
  }

  if (isValidToken && PUBLIC_ROUTES.includes("path")) {
    return NextResponse.redirect(new URL("/main", request.url));
  } else if (!isValidToken && isProtectedPath(path)) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|api|.*\\..*).*)", "/"],
};
