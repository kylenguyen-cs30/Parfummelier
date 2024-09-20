#!/bin/bash

# base url for user-service API
BASE_URL="http://localhost:5001"

# Function to check the response status
check_status() {
  if [ "$1" -eq "$2" ]; then
    echo "✅ $3 - passed"
  else
    echo "❌ $3 - Failed (status: $1)"
  fi
}

# 1. Test Home route
echo "Testing Home Route..."
home_response=$(http GET $BASE_URL/ | jq -r '.')
check_status $? 200 "Home Route"
# 2. Register user
echo "Registering new user..."
user_data=$(http POST $BASE_URL/register firstName="John" lastName="Doe" email="john.doe@example.com" password="password123" userName="johndoe" dob="1990-01-01" | jq -r '.')
user_id=$(echo $user_data | jq -r '.user_id')
scent_id=$(echo $user_data | jq -r '.scentID')
check_status $? 202 "User Registration"

# 3. List Users

# 4. Update ScentBank for the user

# 5. Get ScentBank Details for a user

# 6. Delete User

# 7. Reset Database

# 8. Test PUT method
