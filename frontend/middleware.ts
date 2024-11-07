import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import ChangePassword from "./app/change-password/page";
import { NextURL } from "next/dist/server/web/next-url";

// Define public routes that don't require authentication

// Move Routes to a separate config file for better maintaince
const AUTH_CONFIG = {
  publicRoutes = [
    "/change-password",
    "/signin",
    "/signup",
    "/", // Adding root path as public
    "/api", // Adding API routes as public
  ],
  protectedRoutes: ["/main", "/user-profile", "/chat", "/basket"],

  specialRoutes: {
    changePassword: "/change-password",
    defaultRedirect: "/main",
    authRedirect: "/signin",
  },
} as const;

export async function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;

  const matchesRoute = (path: string, routes: string[]) =>
    routes.some((route) => path === route || path.startsWith(`${route}/`));

  // Get Tokens from cookies
  const accessToken = request.cookies.get("access_token")?.value;
  const resetToken = request.cookies.get("reset_token")?.value;

  // handle special routes first
  if (path === AUTH_CONFIG.specialRoutes.changePassword) {
    if (!resetToken) {
      return NextResponse.redirect(
        new URL(AUTH_CONFIG.specialRoutes.authRedirect, request.url),
      );
    }
    return NextResponse.next();
  }

  // Check for public routes
  const isPublicRoute = matchesRoute(path, AUTH_CONFIG.publicRoutes);

  // if user is authenticated and tries to access auth pages (signin/signup)
  if (accessToken && path.match(/^\sign(in|up)/)) {
    return NextResponse.redirect(
      new URL(AUTH_CONFIG.specialRoutes.defaultRedirect, request.url),
    );
  }

  //protected route check
  if (!isPublicRoute && !accessToken) {
    const response = NextResponse.redirect(
      new URL(AUTH_CONFIG.specialRoutes.authRedirect, request.url),
    );

    response.cookies.set("redirectTo", path, {
      path: "/",
      httpOnly: true,
      sameSite: "lax",
      maxAge: 300,
    });
    return response;
  }

  return NextResponse.next();
}

// Update the matcher to include all routes except _next and static files
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (public folder)
     */
    "/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:jpg|jpeg|gif|png|svg|ico|webp)$).*)",
  ],
};
