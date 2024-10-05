import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const resetToken = request.cookies.get("reset_token")?.value;

  if (!resetToken) {
    return NextResponse.redirect(new URL("/signin", request.url));
  }
  return NextResponse.next(); // proceed next step
}

export const config = {
  matcher: ["/change-password", "/main-page"],
};
