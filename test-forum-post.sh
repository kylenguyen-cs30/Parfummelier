# Store token in a variable for easier use
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MzE2MzIyNzl9.mSFavjW1_KkdAn_9EU8w9h76E92-oyG2y5N3TWYXxOU"

# 1. Test health endpoint
http GET http://localhost:5004/health

# 2. Create a post with authentication
http POST http://localhost:5004/posts/ \
  "Authorization: Bearer $TOKEN" \
  title="My First Post" \
  content="This is a test post with authentication" \
  topic="General" \
  image_urls:='[]'

# 3. Get all posts
http GET http://localhost:5004/posts/ \
  "Authorization: Bearer $TOKEN"

# 4. Get specific post (replace {id} with actual post ID)
http GET http://localhost:5004/posts/1 \
  "Authorization: Bearer $TOKEN"

# 5. Filter posts by topic
http GET http://localhost:5004/posts/ \
  "Authorization: Bearer $TOKEN" \
  topic=="General"

# 6. Upload image for a post (if you have test.jpg)
http -f POST http://localhost:5004/posts/upload-images \
  "Authorization: Bearer $TOKEN" \
  files@./test.jpg

# 7. Create a comment on a post
http POST http://localhost:5004/comments/1 \
  "Authorization: Bearer $TOKEN" \
  content="This is a test comment" \
  parent_id=null

# 8. Get comments for a post
http GET http://localhost:5004/comments/post/1 \
  "Authorization: Bearer $TOKEN"

# Advanced Usage:
# Pagination
http GET http://localhost:5004/posts/ \
  "Authorization: Bearer $TOKEN" \
  skip==0 \
  limit==10

# Create post with image URLs
http POST http://localhost:5004/posts/ \
  "Authorization: Bearer $TOKEN" \
  title="Post with Images" \
  content="This post has some images" \
  topic="Photography" \
  image_urls:='["image1.jpg", "image2.jpg"]'
