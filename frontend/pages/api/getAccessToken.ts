import { NextApiRequest, NextApiResponse } from 'next';
import { parse } from 'cookie';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const cookies = parse(req.headers.cookie || '');
  const access_token = cookies.access_token;

  if (!access_token) {
    return res.status(401).json({ error: 'No access token found' });
  }

  return res.status(200).json({ access_token });
}
