// Day 16: Streaming Audio Recording with WebSockets
let websocket = null;
let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;
let isConnected = false;
let connectionId = null;
let recordingStartTime = null;
let chunkCount = 0;
let totalBytesSent = 0;

// DOM elements
const recordBtn = document.getElementById('record-btn');
const recordText = document.getElementById('record-text');
const statusDiv = document.getElementById('chat-status');
const conversationDiv = document.getElementById('conversation-messages');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Update status display
    updateStatusDisplay();
    
    // Initialize WebSocket connection
    initializeWebSocket();
});

function initializeWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/`;
    
    try {
        websocket = new WebSocket(wsUrl);
        
        websocket.onopen = function(event) {
            console.log('WebSocket connected');
            isConnected = true;
            updateStatusDisplay();
        };
        
        websocket.onmessage = function(event) {
            try {
                const data = JSON.parse(event.data);
                handleWebSocketMessage(data);
            } catch (e) {
                console.log('Received non-JSON message:', event.data);
            }
        };
        
        websocket.onclose = function(event) {
            console.log('WebSocket disconnected');
            isConnected = false;
            updateStatusDisplay();
            
            // Try to reconnect after 3 seconds
            setTimeout(initializeWebSocket, 3000);
        };
        
        websocket.onerror = function(error) {
            console.error('WebSocket error:', error);
            isConnected = false;
            updateStatusDisplay();
        };
        
    } catch (error) {
        console.error('Failed to create WebSocket:', error);
        isConnected = false;
        updateStatusDisplay();
    }
}

function handleWebSocketMessage(data) {
    console.log('WebSocket message received:', data);
    
    switch (data.type) {
        case 'connection':
            connectionId = data.connection_id;
            addMessageToConversation('🔌 System', `Connected to server (ID: ${connectionId})`, 'system');
            break;
            
        case 'recording_started':
            addMessageToConversation('🎙️ System', 'Recording started - sending audio chunks...', 'system');
            break;
            
        case 'recording_stopped':
            addMessageToConversation('⏹️ System', 'Recording stopped - file saved successfully', 'system');
            break;
            
        case 'audio_stream_started':
            addMessageToConversation('📁 System', `Audio file created: ${data.filename}`, 'system');
            break;
            
        case 'audio_chunk_received':
            addMessageToConversation('📊 System', `Received ${data.chunk_count} audio chunks`, 'system');
            break;
            
        case 'audio_chunk_confirmed':
            chunkCount++;
            totalBytesSent += data.bytes_received;
            updateStatusDisplay();
            
            // Update statistics display
            document.getElementById('chunk-count-display').textContent = chunkCount;
            document.getElementById('bytes-display').textContent = `${(totalBytesSent / 1024).toFixed(1)} KB`;
            break;
            
        case 'error':
            addMessageToConversation('❌ Error', data.message, 'error');
            break;
            
        default:
            addMessageToConversation('📡 Server', data.message, 'system');
    }
}

// Combined recording button functionality
function toggleRecording() {
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
}

function startRecording() {
    if (!isConnected) {
        addMessageToConversation('❌ Error', 'WebSocket not connected. Please wait...', 'error');
        return;
    }
    
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });
            
            audioChunks = [];
            chunkCount = 0;
            totalBytesSent = 0;
            recordingStartTime = Date.now();
            
            // Send start recording message to server
            websocket.send(JSON.stringify({
                type: 'start_recording',
                timestamp: new Date().toISOString()
            }));
            
            // Handle audio data
            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    // Send audio chunk directly to server via WebSocket
                    if (websocket && websocket.readyState === WebSocket.OPEN) {
                        websocket.send(event.data);
                    }
                }
            };
            
            mediaRecorder.onstop = () => {
                // Send stop recording message
                websocket.send(JSON.stringify({
                    type: 'stop_recording',
                    timestamp: new Date().toISOString()
                }));
                
                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
            };
            
            // Start recording with small timeslice for streaming
            mediaRecorder.start(100); // Send chunks every 100ms
            
            // Update UI to recording state
            isRecording = true;
            recordBtn.classList.add('recording');
            recordText.textContent = 'Stop Recording';
            updateStatusDisplay();
            
            addMessageToConversation('🎙️ User', 'Started recording...', 'user');
            
        })
        .catch(error => {
            console.error('Microphone access error:', error);
            addMessageToConversation('❌ Error', 'Microphone access denied. Please enable microphone.', 'error');
        });
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        
        // Update UI to stopped state
        isRecording = false;
        recordBtn.classList.remove('recording');
        recordText.textContent = 'Start Recording';
        
        const recordingDuration = ((Date.now() - recordingStartTime) / 1000).toFixed(2);
        addMessageToConversation('⏹️ User', `Stopped recording after ${recordingDuration}s`, 'user');
        
        updateStatusDisplay();
    }
}

function addMessageToConversation(sender, message, type) {
    const time = new Date().toLocaleTimeString();
    let messageClass = 'message-item';
    
    switch (type) {
        case 'user':
            messageClass += ' user-message';
            break;
        case 'system':
            messageClass += ' system-message';
            break;
        case 'error':
            messageClass += ' error-message';
            break;
    }
    
    const messageHtml = `
        <div class="${messageClass}">
            <div class="message-header">
                ${sender} <span class="message-time">${time}</span>
            </div>
            <div class="message-content">${message}</div>
        </div>
    `;
    
    conversationDiv.insertAdjacentHTML('beforeend', messageHtml);
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}

function updateStatusDisplay() {
    const statusSpan = document.getElementById('status');
    
    if (isRecording) {
        const duration = recordingStartTime ? ((Date.now() - recordingStartTime) / 1000).toFixed(1) : '0';
        statusSpan.textContent = `Recording... ${duration}s | Chunks: ${chunkCount} | Bytes: ${(totalBytesSent / 1024).toFixed(1)}KB`;
    } else if (isConnected) {
        statusSpan.textContent = `Connected to WebSocket | Ready to record | Total chunks: ${chunkCount} | Total bytes: ${(totalBytesSent / 1024).toFixed(1)}KB`;
    } else {
        statusSpan.textContent = `Connecting to WebSocket...`;
    }
}

// Session management functions (simplified for Day 16)
function generateSessionId() {
    const sessionInput = document.getElementById('session-id-input');
    const randomId = 'session_' + Math.random().toString(36).substr(2, 9);
    sessionInput.value = randomId;
    updateSessionId();
}

function updateSessionId() {
    const sessionInput = document.getElementById('session-id-input');
    const newSessionId = sessionInput.value.trim();
    
    if (newSessionId) {
        document.getElementById('current-session-display').textContent = newSessionId;
        
        // Clear conversation display when session changes
        conversationDiv.innerHTML = '<div style="color: #6c757d; font-style: italic; text-align: center; padding: 20px;">New session started. Begin recording...</div>';
        document.getElementById('message-count-display').textContent = '0';
    }
}

function clearSession() {
    document.getElementById('session-id-input').value = '';
    document.getElementById('current-session-display').textContent = 'Not set';
    document.getElementById('message-count-display').textContent = '0';
    conversationDiv.innerHTML = '<div style="color: #6c757d; font-style: italic; text-align: center; padding: 20px;">Session cleared. Start recording...</div>';
    
    // Reset recording state
    if (isRecording) {
        stopRecording();
    }
}
