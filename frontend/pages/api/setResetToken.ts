// pages/apit/setResetToken.ts

import { NextApiResponse, NextApiRequest } from "next";
import { serialize } from "cookie";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { reset_token } = req.body;
  if (!reset_token) {
    return res
      .status(400)
      .json({ error: "reset token is not found in setResetToken" });
  }

  const cookie = serialize("reset_token", reset_token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: 60 * 15,
  });
  res.setHeader("Set-Cookie", cookie);
  res.status(200).json({ message: "Reset token stored in cookie" });
}
