import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { jwtVerify } from "jose";

// define route types
const PUBLIC_ROUTES = [
  "/",
  "/signin",
  "signup",
  "forget-password",
  "about-us",
].map((route) => route.toLowerCase());
const AUTH_ROUTES = ["/signin", "/signup"].map((route) => route.toLowerCase());
// const PROTECTED_ROUTES = [
//   "/main",
//   "/user-profile",
//   "/basket",
//   "/chat",
//   "/forum",
//   "product",
//   "/quiz",
//   "/inbox",
//   "/support",
//   "contact-us",
//   "all-products",
//   "gift-guide",
// ];

export async function middleware(request: NextRequest) {
  // path variable as interceptor
  const path = request.nextUrl.pathname.toLowerCase();

  // get tokens
  const accessToken = request.cookies.get("access_token")?.value;
  const resetToken = request.cookies.get("reset_token")?.value;

  // NOTE:
  // 1. handle change-password special case
  if (path === "/change-password") {
    if (!resetToken) {
      return NextResponse.redirect(new URL("/forget-password", request.url));
    }
    return NextResponse.next();
  }

  // NOTE:
  // 2. check token validity
  let isValidToken = false;
  if (accessToken) {
    try {
      await jwtVerify(
        accessToken,
        new TextEncoder().encode(process.env.JWT_SECRET),
      );
      isValidToken = true;
    } catch (error) {
      console.error("Token validation failed: ", error);
      isValidToken = false;
    }
  }

  // NOTE:
  // 3. handle different scenarios

  // CASE: User is on landing page

  if (path === "/") {
    if (isValidToken) {
      return NextResponse.redirect(new URL("/main", request.url));
    }

    return NextResponse.next();
  }

  // CASE: User is on auth routes but already authenticated
  if (isValidToken && AUTH_ROUTES.includes(path)) {
    return NextResponse.redirect(new URL("/main", request.url));
  }

  // CASE: User tries to access protected rotues without valid tokens

  if (!isValidToken && !PUBLIC_ROUTES.includes(path)) {
    return NextResponse.redirect(new URL("/", request.url));
  }
  return NextResponse.next();
}

// Update the matcher to include all routes except _next and static files
export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(png|jpg|jpeg|svg|gif)$).*)",
  ],
};
