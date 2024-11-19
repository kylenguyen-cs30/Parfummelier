export interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
  user_id: number;
  topic: string;
  image_urls: string[];
}
