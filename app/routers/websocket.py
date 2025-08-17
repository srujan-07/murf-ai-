from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import logging
import os
import uuid
from datetime import datetime
import asyncio

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["websocket"])

# Store active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.audio_streams = {}  # Track audio streams per connection

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # Generate unique connection ID
        connection_id = str(uuid.uuid4())
        self.audio_streams[connection_id] = {
            'websocket': websocket,
            'file_path': None,
            'file_handle': None,
            'chunk_count': 0
        }
        
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
        
        # Send welcome message with connection ID
        await websocket.send_text(json.dumps({
            "type": "connection",
            "message": "Connected to WebSocket server",
            "connection_id": connection_id,
            "timestamp": datetime.now().isoformat()
        }))

    def disconnect(self, websocket: WebSocket):
        # Find and cleanup audio stream
        connection_id = None
        for conn_id, stream_info in self.audio_streams.items():
            if stream_info['websocket'] == websocket:
                connection_id = conn_id
                break
        
        if connection_id:
            # Close file handle if open
            if self.audio_streams[connection_id]['file_handle']:
                try:
                    self.audio_streams[connection_id]['file_handle'].close()
                except:
                    pass
            
            # Remove from tracking
            del self.audio_streams[connection_id]
        
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                # Remove broken connections
                self.active_connections.remove(connection)

    async def handle_audio_chunk(self, websocket: WebSocket, audio_data: bytes):
        """Handle incoming audio chunk and save to file"""
        # Find connection info
        connection_id = None
        for conn_id, stream_info in self.audio_streams.items():
            if stream_info['websocket'] == websocket:
                connection_id = conn_id
                break
        
        if not connection_id:
            logger.error("Connection not found for audio data")
            return
        
        stream_info = self.audio_streams[connection_id]
        
        try:
            # Create uploads directory if it doesn't exist
            uploads_dir = "uploads"
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            
            # Create filename for this audio stream if not exists
            if not stream_info['file_path']:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"streaming_audio_{timestamp}_{connection_id[:8]}.webm"
                stream_info['file_path'] = os.path.join(uploads_dir, filename)
                
                # Open file for writing
                stream_info['file_handle'] = open(stream_info['file_path'], 'wb')
                logger.info(f"Started new audio stream: {stream_info['file_path']}")
                
                # Send confirmation to client
                await websocket.send_text(json.dumps({
                    "type": "audio_stream_started",
                    "filename": filename,
                    "timestamp": datetime.now().isoformat()
                }))
            
            # Write audio chunk to file
            if stream_info['file_handle']:
                stream_info['file_handle'].write(audio_data)
                stream_info['chunk_count'] += 1
                
                # Flush to ensure data is written
                stream_info['file_handle'].flush()
                
                # Send confirmation every 10 chunks
                if stream_info['chunk_count'] % 10 == 0:
                    await websocket.send_text(json.dumps({
                        "type": "audio_chunk_received",
                        "chunk_count": stream_info['chunk_count'],
                        "timestamp": datetime.now().isoformat()
                    }))
                
                logger.debug(f"Audio chunk {stream_info['chunk_count']} saved to {stream_info['file_path']}")
        
        except Exception as e:
            logger.error(f"Error handling audio chunk: {e}")
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": f"Failed to save audio chunk: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }))

manager = ConnectionManager()

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication and audio streaming"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Check message type
            message = await websocket.receive()
            
            if message["type"] == "websocket.receive":
                # Handle text messages
                if "text" in message:
                    data = message["text"]
                    logger.info(f"Received text message: {data}")
                    
                    try:
                        parsed_data = json.loads(data)
                        if parsed_data.get("type") == "start_recording":
                            # Client wants to start recording
                            await websocket.send_text(json.dumps({
                                "type": "recording_started",
                                "message": "Ready to receive audio chunks",
                                "timestamp": datetime.now().isoformat()
                            }))
                        elif parsed_data.get("type") == "stop_recording":
                            # Client wants to stop recording
                            await websocket.send_text(json.dumps({
                                "type": "recording_stopped",
                                "message": "Recording stopped, file saved",
                                "timestamp": datetime.now().isoformat()
                            }))
                        else:
                            # Echo back other text messages
                            response = {
                                "type": "echo",
                                "message": f"Server received: {data}",
                                "original_message": data,
                                "timestamp": datetime.now().isoformat()
                            }
                            await manager.send_personal_message(json.dumps(response), websocket)
                    
                    except json.JSONDecodeError:
                        # Handle plain text
                        response = {
                            "type": "echo",
                            "message": f"Server received: {data}",
                            "original_message": data,
                            "timestamp": datetime.now().isoformat()
                        }
                        await manager.send_personal_message(json.dumps(response), websocket)
                
                elif "bytes" in message:
                    # Handle binary audio data
                    audio_data = message["bytes"]
                    logger.info(f"Received audio chunk: {len(audio_data)} bytes")
                    
                    # Save audio chunk to file
                    await manager.handle_audio_chunk(websocket, audio_data)
                    
                    # Send confirmation
                    await websocket.send_text(json.dumps({
                        "type": "audio_chunk_confirmed",
                        "bytes_received": len(audio_data),
                        "timestamp": datetime.now().isoformat()
                    }))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
