#!/usr/bin/env python3
"""
Test script for WebSocket functionality
Run this after starting the server to test the WebSocket connection
"""

import asyncio
import websockets
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_websocket():
    """Test WebSocket connection and message exchange"""
    uri = "ws://localhost:8000/ws/"
    
    try:
        logger.info("Connecting to WebSocket server...")
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to WebSocket server!")
            
            # Wait for welcome message
            welcome_msg = await websocket.recv()
            logger.info(f"Received welcome: {welcome_msg}")
            
            # Send test messages
            test_messages = [
                "Hello, WebSocket server!",
                "This is a test message",
                "How are you doing?",
                "Testing real-time communication"
            ]
            
            for i, message in enumerate(test_messages, 1):
                logger.info(f"Sending message {i}: {message}")
                await websocket.send(message)
                
                # Wait for echo response
                response = await websocket.recv()
                logger.info(f"Received response {i}: {response}")
                
                # Small delay between messages
                await asyncio.sleep(1)
            
            logger.info("All messages sent and received successfully!")
            
    except websockets.exceptions.ConnectionRefused:
        logger.error("Failed to connect to WebSocket server. Make sure the server is running on localhost:8000")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

if __name__ == "__main__":
    print("WebSocket Test Client")
    print("=" * 30)
    print("Make sure your server is running on localhost:8000")
    print("This script will connect and send test messages")
    print()
    
    asyncio.run(test_websocket())
