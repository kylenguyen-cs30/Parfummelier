import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Define public routes that don't require authentication
const publicRoutes = [
  "/change-password",
  "/signin",
  "/signup",
  "/manage-user-profile-page",
  "/", // Adding root path as public
  "/api", // Adding API routes as public
];

export async function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;

  // Get tokens from the cookies
  const accessToken = request.cookies.get("access_token")?.value;
  const resetToken = request.cookies.get("reset_token")?.value;

  // Special case for change-password route
  if (path === "/change-password") {
    if (!resetToken) {
      return NextResponse.redirect(new URL("/signin", request.url));
    }
    return NextResponse.next();
  }

  // Check if the current path is a public route
  const isPublicRoute = publicRoutes.some(route =>
    path === route || path.startsWith(`${route}/`)
  );

  // If it's not a public route and there's no access token, redirect to signin
  if (!isPublicRoute && !accessToken) {
    return NextResponse.redirect(new URL("/signin", request.url));
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



// BUG:
// this part still have bugs. we need to investigate
//
// if (path === "/main-page") {
//   if (!accessToken) {
//     return NextResponse.redirect(new URL("/signin", request.url)); // If no access token, redirect to login
//   }
//
//   // Check if the access token is valid
//   const validateTokenResponse = await fetch(
//     "http://localhost:5002/validate-token",
//     {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ access_token: accessToken }),
//     },
//   );
//
//   if (validateTokenResponse.status === 401) {
//     const responseData = await validateTokenResponse.json();
//
//     // If the token is expired, refresh it
//     if (responseData.status === "expired" && refreshToken) {
//       // Call the /refresh endpoint to get a new access_token and refresh_token
//       const refreshResponse = await fetch("http://localhost:5002/refresh", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         credentials: "include", // Ensure cookies are sent with the request
//       });
//
//       if (refreshResponse.status === 200) {
//         return NextResponse.next(); // Proceed if the token is refreshed successfully
//       } else {
//         return NextResponse.redirect(new URL("/signin", request.url)); // Redirect to login if refresh failed
//       }
//     } else {
//       return NextResponse.redirect(new URL("/signin", request.url)); // Redirect to login if no refresh token
//     }
//   }
// }
