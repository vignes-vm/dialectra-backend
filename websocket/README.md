# WebSocket Configuration for Debate Sessions

This module provides WebSocket functionality for debate sessions, allowing real-time communication between clients participating in the same debate.

## Overview

Each debate session has its own WebSocket connection, identified by the session ID. Clients can connect to a specific debate session and exchange messages with other clients in the same session.

## Usage

### Connecting to a Debate Session

To connect to a debate session, use the following WebSocket URL:

```
ws://your-server-address/debate/{session_id}/ws
```

Replace `{session_id}` with the ID of the debate session you want to connect to. You can get the session ID when creating a new debate session using the `/create_session` endpoint.

### Message Format

Messages are exchanged in JSON format. Each message should have a `type` field that indicates the type of message.

#### Sending a Speech

To submit a speech, send a message with the following format:

```json
{
  "type": "speech",
  "speaker": "Speaker Name",
  "content": "Speech content goes here"
}
```

#### Requesting an AI Response

To request an AI-generated response, send a message with the following format:

```json
{
  "type": "ai_response",
  "motion": "Debate motion",
  "speaker_role": "Speaker role",
  "draft": "Optional draft text"
}
```

### Receiving Messages

You will receive messages in JSON format. The `type` field indicates the type of message:

#### Speech Message

```json
{
  "type": "speech",
  "speaker": "Speaker Name",
  "content": "Speech content"
}
```

#### AI Response Message

```json
{
  "type": "ai_response",
  "speech": "AI-generated speech content"
}
```

#### System Message

```json
{
  "type": "system",
  "message": "System message (e.g., 'A client has disconnected')"
}
```

## Example Client Code

Here's an example of how to connect to a debate session using JavaScript:

```javascript
// Connect to a debate session
const sessionId = "your-session-id";
const socket = new WebSocket(`ws://your-server-address/debate/${sessionId}/ws`);

// Handle connection open
socket.onopen = function(event) {
  console.log("Connected to debate session:", sessionId);
};

// Handle incoming messages
socket.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log("Received message:", data);
  
  // Handle different message types
  if (data.type === "speech") {
    console.log(`${data.speaker} says: ${data.content}`);
  } else if (data.type === "ai_response") {
    console.log(`AI response: ${data.speech}`);
  } else if (data.type === "system") {
    console.log(`System message: ${data.message}`);
  }
};

// Handle errors
socket.onerror = function(error) {
  console.error("WebSocket error:", error);
};

// Handle connection close
socket.onclose = function(event) {
  console.log("Disconnected from debate session");
};

// Send a speech
function sendSpeech(speaker, content) {
  socket.send(JSON.stringify({
    type: "speech",
    speaker: speaker,
    content: content
  }));
}

// Request an AI response
function requestAIResponse(motion, speakerRole, draft = "") {
  socket.send(JSON.stringify({
    type: "ai_response",
    motion: motion,
    speaker_role: speakerRole,
    draft: draft
  }));
}
```