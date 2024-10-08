import { NextApiRequest, NextApiResponse } from "next";
import { serialize } from "cookie";

export default function hanlder(req: NextApiRequest, res: NextApiResponse) {
  const { access_token } = req.body;

  if (!access_token) {
    return res.status(400).json({ error: "No access token provided" });
  }

  const cookie = serialize("access_token", access_token, {
    httpOnly: true,
    // secure: process.env.NODE_ENV === "production",
    maxAge: 60 * 15, // 15 mins
    path: "/",
  });
  res.setHeader("Set-Cookie", cookie);
  res.status(200).json({ message: "access token set in cookie" });
}
