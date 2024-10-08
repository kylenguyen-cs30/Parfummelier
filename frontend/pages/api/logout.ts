import { NextApiResponse, NextApiRequest } from "next";
import { serialize } from "cookie";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  // Invalidate both access_token and refresh_token by setting Max-Age
  const accessTokenCookie = serialize("access_token", "", {
    httpOnly: true,
    maxAge: 0,
    path: "/",
  });

  const refreshTokenCookie = serialize("refresh_token", "", {
    httpOnly: true,
    maxAge: 0,
    path: "/",
  });

  // set both cookies in the response header
  res.setHeader("Set-Cookie", [accessTokenCookie, refreshTokenCookie]);
  res.status(200).json({ message: "Logged out succesfully" });
}
