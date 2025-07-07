from typing import Dict, List, Optional
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

class ConnectionManager:
    """
    A class to manage WebSocket connections for different debate sessions.
    Each debate session has its own set of connected clients.
    """
    def __init__(self):
        # Dictionary to store active connections for each debate session
        # Key: session_id, Value: list of WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """
        Connect a client to a specific debate session.
        
        Args:
            websocket: The WebSocket connection
            session_id: The ID of the debate session
        """
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        """
        Disconnect a client from a specific debate session.
        
        Args:
            websocket: The WebSocket connection
            session_id: The ID of the debate session
        """
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)
            # Clean up empty session lists
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
    
    async def send_message(self, message: dict, session_id: str, websocket: Optional[WebSocket] = None):
        """
        Send a message to all clients in a specific debate session or to a specific client.
        
        Args:
            message: The message to send
            session_id: The ID of the debate session
            websocket: Optional specific WebSocket to send to (if None, send to all in session)
        """
        if session_id in self.active_connections:
            if websocket:
                # Send to specific client
                await websocket.send_json(message)
            else:
                # Send to all clients in the session
                for connection in self.active_connections[session_id]:
                    await connection.send_json(message)
    
    def get_connections(self, session_id: str) -> List[WebSocket]:
        """
        Get all connections for a specific debate session.
        
        Args:
            session_id: The ID of the debate session
            
        Returns:
            List of WebSocket connections for the session
        """
        return self.active_connections.get(session_id, [])

# Create a global instance of the connection manager
manager = ConnectionManager()