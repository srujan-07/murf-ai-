#!/usr/bin/env python3
"""
Test script for Day 16: Streaming Audio WebSocket functionality
"""

import asyncio
import websockets
import json
import time
import os

async def test_streaming_websocket():
    """Test the streaming WebSocket functionality"""
    
    uri = "ws://localhost:8000/ws/"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket server")
            
            # Wait for connection message
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📡 Connection message: {data}")
            
            # Send start recording message
            start_msg = {
                "type": "start_recording",
                "timestamp": time.time()
            }
            await websocket.send(json.dumps(start_msg))
            print("🎙️ Sent start recording message")
            
            # Wait for recording started confirmation
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📡 Recording started: {data}")
            
            # Simulate sending audio chunks (fake binary data)
            for i in range(5):
                # Send fake audio chunk (100 bytes)
                fake_audio = b"fake_audio_data_" * 6 + b"end"  # 100 bytes
                await websocket.send(fake_audio)
                print(f"📦 Sent audio chunk {i+1} ({len(fake_audio)} bytes)")
                
                # Wait for confirmation
                response = await websocket.recv()
                data = json.loads(response)
                print(f"📡 Chunk confirmed: {data}")
                
                time.sleep(0.2)  # Wait 200ms between chunks
            
            # Send stop recording message
            stop_msg = {
                "type": "stop_recording",
                "timestamp": time.time()
            }
            await websocket.send(json.dumps(stop_msg))
            print("⏹️ Sent stop recording message")
            
            # Wait for recording stopped confirmation
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📡 Recording stopped: {data}")
            
            # Check if file was created
            uploads_dir = "uploads"
            if os.path.exists(uploads_dir):
                files = [f for f in os.listdir(uploads_dir) if f.startswith("streaming_audio_")]
                if files:
                    print(f"✅ Audio file created: {files[-1]}")
                    file_path = os.path.join(uploads_dir, files[-1])
                    file_size = os.path.getsize(file_path)
                    print(f"📁 File size: {file_size} bytes")
                else:
                    print("❌ No audio files found")
            else:
                print("❌ Uploads directory not found")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Day 16: Streaming Audio WebSocket")
    print("=" * 50)
    
    asyncio.run(test_streaming_websocket())
    
    print("\n" + "=" * 50)
    print("�� Test completed!")
