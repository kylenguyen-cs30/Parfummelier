import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;

  // Get tokens from the cookies
  const accessToken = request.cookies.get("access_token")?.value;
  const refreshToken = request.cookies.get("refresh_token")?.value;
  const resetToken = request.cookies.get("reset_token")?.value;

  // Define the logic for each type of token

  // For routes requiring a reset token (e.g., change-password)
  if (path === "/change-password") {
    if (!resetToken) {
      return NextResponse.redirect(new URL("/signin", request.url));
    }
  }

  // For routes requiring an access token (e.g., main-page)
  if (path === "/main-page") {
    if (!accessToken) {
      return NextResponse.redirect(new URL("/", request.url));
    }
  }


  // For routes that require token refresh logic
  if (path === "/protected-resource") {
    if (!accessToken && refreshToken) {
      // In this case, refresh the access token using refreshToken
      return NextResponse.redirect(new URL("/refresh-token", request.url));
    } else if (!accessToken && !refreshToken) {
      return NextResponse.redirect(new URL("/signin", request.url)); // Require login if both tokens are missing
    }
  }

  return NextResponse.next(); // Proceed to the requested route if everything is valid
}

export const config = {
  matcher: ["/change-password", "/main-page", "/protected-resource"], // Protect routes
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
