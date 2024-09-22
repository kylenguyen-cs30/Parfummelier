#!/bin/bash

# Base URL for user-service API
BASE_URL="http://localhost:5001"

# Function to check the response status
check_status() {
  if [ "$1" -eq "0" ]; then
    echo "✅ $3 - passed. Response: $4"
  else
    echo "❌ $3 - Failed (status: $1). Response: $4"
  fi
}

# 1. Test Home route
echo "Testing Home Route..."
home_response=$(http GET "$BASE_URL/" 2>&1)
check_status $? 200 "Home Route" "$home_response"

# 2. Register user
echo "Registering new user..."
user_data=$(http POST "$BASE_URL/register" firstName="John" lastName="Doe" email="john.doe123@example.com" password="password123" userName="johndoe123" dob="1990-01-01" 2>&1)
check_status $? 202 "User Registration" "$user_data"

user_id=$(echo "$user_data" | jq -r '.user_id')
scent_id=$(echo "$user_data" | jq -r '.scentID')

# 3. List Users
echo "Listing all users..."
list_users_response=$(http GET "$BASE_URL/users" 2>&1)
check_status $? 200 "List Users" "$list_users_response"

# 4. Update ScentBank for the user
echo "Updating ScentBank for user with ID: $user_id..."

UPDATED_DATA='{
  "favorite_notes": ["Citrus", "Floral"],
  "favorite_accords": ["Fresh", "Woody"],
  "favorite_scents": ["Strong", "Long-Lasting"],
  "favorite_seasons": ["Summer", "Spring"]
}'

update_response=$(echo "$UPDATED_DATA" | http PUT "$BASE_URL/user/$user_id/scentbank" 2>&1)
check_status $? 201 "Update ScentBank" "$update_response"

# 5. Get ScentBank Details for a user
echo "Getting ScentBank Details for user with ID: $user_id..."
scentbank_response=$(http GET "$BASE_URL/user/$user_id/scentbank/details" 2>&1)
check_status $? 200 "Get ScentBank Details" "$scentbank_response"

# 6. Delete User
echo "Deleting user with ID: $user_id..."
delete_response=$(http DELETE "$BASE_URL/user/$user_id/delete" 2>&1)
check_status $? 200 "Delete User" "$delete_response"

# 7. Reset Database
echo "Resetting the database..."
reset_db_response=$(http POST "$BASE_URL/reset-db" 2>&1)
check_status $? 200 "Reset Database" "$reset_db_response"


# 8. Test PUT method
