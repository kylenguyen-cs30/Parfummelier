#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Function to check if service is running
check_service() {
    for i in {1..5}; do
        echo "Attempting to curl http://localhost:5004/chat/"
        curl -v http://localhost:5004/chat/
        if [ $? -eq 0 ]; then
            return 0
        fi
        echo "Waiting for service to be ready... (attempt $i)"
        # Show docker container status
        echo "Docker container status:"
        docker ps | grep forum-service
        echo "Docker logs:"
        docker-compose logs --tail=20 forum-service
        sleep 2
    done
    return 1
}

# Wait for service to be ready
echo -e "${BLUE}Checking if service is ready...${NC}"
if ! check_service; then
    echo -e "${RED}Service is not responding. Please check if it's running.${NC}"
    exit 1
fi
# Create chatroom
echo -e "${BLUE}Creating test chatroom...${NC}"
RESPONSE=$(curl -s -X POST http://localhost:5004/chat/chatroom \
    -H "Content-Type: application/json" \
    -d '{"participants": [1, 2, 3]}')

CHATROOM_ID=$(echo $RESPONSE | jq -r '.chatroom_id')

if [ -z "$CHATROOM_ID" ] || [ "$CHATROOM_ID" == "null" ]; then
    echo -e "${RED}Failed to create chatroom${NC}"
    exit 1
fi

echo -e "${GREEN}Chatroom created with ID: $CHATROOM_ID${NC}"

# Create expect script for WebSocket testing
cat > ws_test.exp << EOF
#!/usr/bin/expect -f
set timeout 10
set user_id [lindex \$argv 0]
set chatroom_id [lindex \$argv 1]

spawn wscat -c ws://localhost:5004/chat/ws/\$chatroom_id

expect "Connected" {
    send "{\\"userId\\": \$user_id, \\"content\\": \\"Hello from User \$user_id!\\"}\r"
    expect "message" {
        send "{\\"userId\\": \$user_id, \\"content\\": \\"How is everyone?\\"}\r"
        expect "message"
    }
}

sleep 2
EOF

chmod +x ws_test.exp

# Function to run a single user test
test_user() {
    local USER_ID=$1
    local CHATROOM_ID=$2
    echo -e "${BLUE}Testing User $USER_ID${NC}"
    ./ws_test.exp $USER_ID $CHATROOM_ID
}

# Run tests sequentially (more reliable than parallel for testing)
echo -e "${BLUE}Starting user simulations...${NC}"
test_user 1 $CHATROOM_ID
test_user 2 $CHATROOM_ID
test_user 3 $CHATROOM_ID

# Clean up expect script
rm ws_test.exp

# Get final messages
echo -e "\n${BLUE}Final messages in chatroom:${NC}"
curl -s http://localhost:5004/chat/chatroom/$CHATROOM_ID/messages | jq '.'
