import { NextApiRequest, NextApiResponse } from "next";
import { parse } from "cookie";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  console.log("Cookie contents: ", req.cookies);
  console.log("Headers: ", req.headers);
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const cookies = parse(req.headers.cookie || "");
    const access_token = cookies.access_token;

    if (!access_token) {
      res.status(401).json({ error: "No Token" });
      return;
    }

    return res.status(200).json({ access_token });
  } catch (error) {
    console.error("Token retrieval error: ", error);
    res.status(500).json({ error: "Internal Server error" });
  }
}
