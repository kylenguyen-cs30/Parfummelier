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

export async function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;

  // Skip middleware for static files and API routes
  if (
    path.includes("/_next") ||
    path.includes("/api") ||
    path.match(/\.(jpg|jpeg|png|gif|ico|svg|css|js)$/)
  ) {
    return NextResponse.next();
  }

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

  // Handle authentication redirects
  if (isValidToken) {
    // Redirect authenticated users from public routes to main
    if (PUBLIC_ROUTES.includes(path)) {
      return NextResponse.redirect(new URL("/main", request.url));
    }
  } else {
    // Redirect unauthenticated users from protected routes to home
    if (!PUBLIC_ROUTES.includes(path)) {
      return NextResponse.redirect(new URL("/", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|api|.*\\..*).*)", "/"],
};
