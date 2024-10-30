import asyncio
import websockets
import json
import httpx

class ChatTester:

    def __init__(self) -> None:
        # John's Credential
        self.john_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MzAzMjI0MDB9.5UkVGrZEGYC27Fxh600ypBKRzOmrKOnppKj4nZEG9Wk"

        # Jane's Credential
        self.jane_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3MzAzMjI0MTF9.p447-7PEObuQq_9FDm0HKUlQhWKZlSFIedYdhIB3o28"

        self.chatroom_id = None
        self.forum_service_url = "http://localhost:5004"



    async def create_chatroom(self):
        """Create a chatroom for John and Jane"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.forum_service_url}/chat/chatroom",
                json={"participants": [1, 2]},  # John's ID and Jane's ID
                headers={"Authorization": f"Bearer {self.john_token}"}
            )
            data = response.json()
            self.chatroom_id = data["chatroom_id"]
            print(f"Created chatroom: {self.chatroom_id}")

    # In test_chat.py, add error handling
    async def simulate_user(self, name: str, token: str, messages: list):
        try:
            ws_url = f"ws://localhost:5004/chat/ws/{self.chatroom_id}?token={token}"
            
            async with websockets.connect(ws_url) as websocket:
                print(f"{name} connected to chat")
                
                for msg in messages:
                    await asyncio.sleep(1)
                    message = {
                        "content": msg
                    }
                    print(f"Sending message: {message}")
                    await websocket.send(json.dumps(message))
                    
                    response = await websocket.recv()
                    response_data = json.loads(response)
                    print(f"{name} received: {response_data}")
                    
                    if "type" in response_data and response_data["type"] == "error":
                        print(f"Error received: {response_data['content']}")
                        
        except Exception as e:
            print(f"Error in {name}'s session: {str(e)}")

    async def run_test(self):
        """Run the complete chat test"""
        # First create the chatroom
        await self.create_chatroom()
        
        # Define messages for each user
        john_messages = [
            "Hi Jane! How are you?",
            "I'm doing great too! Have you tried any new perfumes lately?",
            "That sounds wonderful! We should go perfume shopping sometime."
        ]
        
        jane_messages = [
            "Hello John! I'm doing well, how about you?",
            "Yes! I just discovered this amazing floral scent!",
            "That would be fun! Let's plan for next week."
        ]
        
        # Run both users' chat simulations concurrently
        await asyncio.gather(
            self.simulate_user("John", self.john_token, john_messages),
            self.simulate_user("Jane", self.jane_token, jane_messages)
        )

async def main():
    tester = ChatTester()
    print("Starting chat test...")
    await tester.run_test()
    print("Chat test completed!")

if __name__ == "__main__":
    asyncio.run(main())


