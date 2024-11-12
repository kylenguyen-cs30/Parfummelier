// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { jwtVerify } from "jose";

const PUBLIC_ROUTES = [
  "/",
  "/(auth)/sigin",
  "/(auth)/signup",
  "/(auth)/forget-password",
  "/(static)/about-us",
  "/(static)/contact-us",
  "/(static)/support",
];

const AUTH_ROUTES = ["/(auth)/signin", "/(auth)/signup"];

export async function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;

  // Skip middleware for static files
  if (
    path.includes("/_next") ||
    path.includes("/api") ||
    path.match(/\.(jpg|jpeg|png|gif|ico|svg|css|js)$/)
  ) {
    return NextResponse.next();
  }

  const accessToken = request.cookies.get("access_token")?.value;
  const resetToken = request.cookies.get("reset_token")?.value;

  // Handle change-password
  if (path === "/(auth)/change-password") {
    if (!resetToken) {
      return NextResponse.redirect(
        new URL("/(auth)/forget-password", request.url),
      );
    }
    return NextResponse.next();
  }

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

  // Landing page redirect
  if (path === "/" && isValidToken) {
    return NextResponse.redirect(new URL("/(main)/main", request.url));
  }

  // Auth routes protection
  if (isValidToken && AUTH_ROUTES.includes(path)) {
    return NextResponse.redirect(new URL("/(main)/main", request.url));
  }

  // Protected routes
  if (!isValidToken && !PUBLIC_ROUTES.includes(path)) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    // Match all paths except static files and api
    "/((?!_next/static|_next/image|api|.*\\..*).*)",
    // Include root path
    "/",
  ],
};
