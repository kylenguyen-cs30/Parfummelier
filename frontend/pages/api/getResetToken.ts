// pages/api/getResetToken.ts

import { NextApiResponse, NextApiRequest } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const resetToken = req.cookies.reset_token;

  if (!resetToken) {
    return res.status(400).json({ error: "reset token is not found" });
  }
  res.status(200).json({ resetToken });
}
