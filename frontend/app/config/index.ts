export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  imageUrl: process.env.NEXT_PUBLIC_IMAGE_URL || "http//localhost:8000",
} as const;
