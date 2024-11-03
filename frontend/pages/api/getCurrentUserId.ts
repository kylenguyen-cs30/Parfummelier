import { NextApiRequest, NextApiResponse } from "next";
import jwt from "jsonwebtoken";
import { getAccessToken } from "./getAccessToken";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  try {
    const { access_token } = await getAccessToken(req, res);

    if (!access_token) {
      return res.status(401).json({ error: "No token found" });
    }

    const decoded = jwt.verify(access_token, process.env.JWT_SECRET!) as {
      user_id: number;
    };
    return res.status(200).json({ user_id: decoded.user_id });
  } catch (error) {
    console.error("Error getting user ID:", error);
    return res.status(401).json({ error: "Unauthorized" });
  }
}
