# WebSocket Testing

This directory contains a script for testing the WebSocket functionality of the debate application.

## Prerequisites

Before running the test script, make sure you have the following dependencies installed:

```bash
pip install websockets requests
```

## Running the Test

1. Make sure the debate application server is running:

```bash
python app.py
```

2. In a separate terminal, run the WebSocket test script:

```bash
python test_websocket.py
```

## What the Test Does

The test script performs the following operations:

1. Creates a new debate session using the REST API
2. Connects to the WebSocket for that session
3. Tests basic WebSocket connection and initial state reception
4. Tests submitting a speech message
5. Tests requesting an AI-generated response
6. Tests handling of invalid message formats

## Expected Output

If all tests pass, you should see output similar to:

```
WebSocket Test Script
=====================
This script tests the WebSocket functionality of the debate application.
Make sure the server is running at http://127.0.0.1:8000

Starting WebSocket tests...

=== Creating a debate session ===
✅ Session created with ID: [session_id]

=== Testing WebSocket Connection ===
✅ Successfully connected to WebSocket
✅ Received initial state: [state_json]
✅ Initial state has correct format

=== Testing Speech Submission ===
Sending speech message: {"type":"speech","speaker":"Test Speaker","content":"This is a test speech about AI regulation."}
Received response: [response_json]
✅ Speech response received with correct format

=== Testing AI Response Generation ===
Requesting AI response: {"type":"ai_response","motion":"AI should be regulated","speaker_role":"Prime Minister"}
Received AI response: [ai_response_json]
✅ AI response received with correct format

=== Testing Invalid Message Handling ===
Sending invalid message: {"type":"invalid_type","data":"This should not be processed"}
No response received for invalid message (this might be expected)

=== Test Summary ===
Passed: 4/4 tests

✅ All WebSocket tests completed successfully!
```

If any test fails, the script will indicate which test failed and provide error details.

## Troubleshooting

- If you see connection errors, make sure the server is running at http://127.0.0.1:8000
- If tests time out, you may need to increase the TIMEOUT value in the script
- If the AI response test fails, it might be due to slow AI generation - try increasing the timeout for that specific test