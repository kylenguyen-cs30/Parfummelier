import { NextApiRequest, NextApiResponse } from "next";
import jwt from "jsonwebtoken";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  try {
    const { access_token } = req.body;
    const decoded = jwt.verify(access_token, process.env.JWT_SECRET!);
    return res.status(200).json({ valid: true, decoded });
  } catch (error) {
    console.error("Error in Token Verification: ", error);
    return res.status(401).json({ valid: false });
  }
}
