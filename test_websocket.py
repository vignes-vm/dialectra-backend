import asyncio
import json
import websockets
import requests
import sys
import time
from websockets.exceptions import ConnectionClosed

# Server URL
BASE_URL = "http://127.0.0.1:8000"
WS_BASE_URL = "ws://127.0.0.1:8000"

# Timeout for WebSocket operations (in seconds)
TIMEOUT = 10

async def test_websocket_connection(session_id):
    """
    Test basic WebSocket connection and initial state reception
    """
    print("\n=== Testing WebSocket Connection ===")
    try:
        async with websockets.connect(f"{WS_BASE_URL}/debate/{session_id}/ws") as websocket:
            print("✅ Successfully connected to WebSocket")

            # Receive initial debate state
            initial_state = await asyncio.wait_for(websocket.recv(), TIMEOUT)
            initial_data = json.loads(initial_state)
            print(f"✅ Received initial state: {initial_state}")

            if initial_data.get("type") == "debate_state":
                print("✅ Initial state has correct format")
            else:
                print("❌ Initial state has unexpected format")

            return True
    except ConnectionClosed as e:
        print(f"❌ WebSocket connection closed unexpectedly: {e}")
        return False
    except asyncio.TimeoutError:
        print(f"❌ Timed out waiting for initial state")
        return False
    except Exception as e:
        print(f"❌ Error during connection test: {e}")
        return False

async def test_speech_submission(session_id):
    """
    Test submitting a speech and receiving a response
    """
    print("\n=== Testing Speech Submission ===")
    try:
        async with websockets.connect(f"{WS_BASE_URL}/debate/{session_id}/ws") as websocket:
            # Skip initial state
            await websocket.recv()

            # Send a speech message
            speech_message = {
                "type": "speech",
                "speaker": "Test Speaker",
                "content": "This is a test speech about AI regulation."
            }
            print(f"Sending speech message: {json.dumps(speech_message)}")
            await websocket.send(json.dumps(speech_message))

            # Receive response
            response = await asyncio.wait_for(websocket.recv(), TIMEOUT)
            response_data = json.loads(response)
            print(f"Received response: {response}")

            if response_data.get("type") in ["speech", "error"]:
                print("✅ Speech response received with correct format")
                return True
            else:
                print("❌ Speech response has unexpected format")
                return False
    except Exception as e:
        print(f"❌ Error during speech test: {e}")
        return False

async def test_ai_response(session_id):
    """
    Test requesting an AI response
    """
    print("\n=== Testing AI Response Generation ===")
    try:
        async with websockets.connect(f"{WS_BASE_URL}/debate/{session_id}/ws") as websocket:
            # Skip initial state
            await websocket.recv()

            # Request AI response
            ai_request = {
                "type": "ai_response",
                "motion": "AI should be regulated",
                "speaker_role": "Prime Minister"
            }
            print(f"Requesting AI response: {json.dumps(ai_request)}")
            await websocket.send(json.dumps(ai_request))

            # Receive AI response (this might take longer)
            ai_response = await asyncio.wait_for(websocket.recv(), TIMEOUT * 3)
            ai_data = json.loads(ai_response)
            print(f"Received AI response: {ai_response}")

            if ai_data.get("type") == "ai_response" and "speech" in ai_data:
                print("✅ AI response received with correct format")
                return True
            else:
                print("❌ AI response has unexpected format")
                return False
    except asyncio.TimeoutError:
        print("❌ Timed out waiting for AI response (this might be normal if AI generation is slow)")
        return False
    except Exception as e:
        print(f"❌ Error during AI response test: {e}")
        return False

async def test_invalid_message(session_id):
    """
    Test sending an invalid message format
    """
    print("\n=== Testing Invalid Message Handling ===")
    try:
        async with websockets.connect(f"{WS_BASE_URL}/debate/{session_id}/ws") as websocket:
            # Skip initial state
            await websocket.recv()

            # Send invalid message
            invalid_message = {
                "type": "invalid_type",
                "data": "This should not be processed"
            }
            print(f"Sending invalid message: {json.dumps(invalid_message)}")
            await websocket.send(json.dumps(invalid_message))

            # Try to receive a response (may not get one)
            try:
                response = await asyncio.wait_for(websocket.recv(), 5)  # Short timeout
                print(f"Received response to invalid message: {response}")
                return True
            except asyncio.TimeoutError:
                print("No response received for invalid message (this might be expected)")
                return True
    except Exception as e:
        print(f"❌ Error during invalid message test: {e}")
        return False

async def run_all_tests():
    """
    Run all WebSocket tests
    """
    print("Starting WebSocket tests...")

    # Step 1: Create a debate session using the REST API
    print("\n=== Creating a debate session ===")
    try:
        response = requests.post(f"{BASE_URL}/create_session", json={"topic": "AI should be regulated"})
        if response.status_code != 200:
            print(f"❌ Failed to create session: {response.text}")
            return

        session_data = response.json()
        session_id = session_data["id"]
        print(f"✅ Session created with ID: {session_id}")

        # Run all tests
        tests = [
            test_websocket_connection(session_id),
            test_speech_submission(session_id),
            test_ai_response(session_id),
            test_invalid_message(session_id)
        ]

        results = await asyncio.gather(*tests, return_exceptions=True)

        # Print summary
        print("\n=== Test Summary ===")
        success_count = sum(1 for r in results if r is True)
        print(f"Passed: {success_count}/{len(tests)} tests")

        if success_count == len(tests):
            print("\n✅ All WebSocket tests completed successfully!")
        else:
            print("\n❌ Some tests failed. Check the logs above for details.")

    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect to the server. Make sure the server is running.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# Run the tests
if __name__ == "__main__":
    print("WebSocket Test Script")
    print("=====================")
    print("This script tests the WebSocket functionality of the debate application.")
    print("Make sure the server is running at", BASE_URL)

    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
        sys.exit(1)
