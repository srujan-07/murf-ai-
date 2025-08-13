// Day 12: Enhanced Chat Agent with Combined Recording Button
let chatMediaRecorder;
let chatAudioChunks = [];
let currentSessionId = '';
let isRecording = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Generate a random session ID on load
    generateSessionId();
    
    // Update status display
    updateStatusDisplay();
});

// Combined recording button functionality
function toggleRecording() {
    if (isRecording) {
        stopChatRecording();
    } else {
        startChatRecording();
    }
}

function startChatRecording() {
    const recordBtn = document.getElementById('record-btn');
    const recordText = document.getElementById('record-text');
    const statusDiv = document.getElementById('chat-status');
    
    // Update session if input changed
    updateSessionId();
    
    if (!currentSessionId) {
        statusDiv.textContent = '❌ Please enter a session ID';
        statusDiv.style.color = '#dc3545';
        return;
    }
    
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            chatMediaRecorder = new MediaRecorder(stream);
            chatAudioChunks = [];
            
            chatMediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    chatAudioChunks.push(event.data);
                }
            };
            
            chatMediaRecorder.onstop = async () => {
                const audioBlob = new Blob(chatAudioChunks, { type: 'audio/webm' });
                await processChatMessage(audioBlob);
            };
            
            chatMediaRecorder.start();
            
            // Update UI to recording state
            isRecording = true;
            recordBtn.classList.add('recording');
            recordText.textContent = 'Stop Recording';
            statusDiv.textContent = '🎙️ Recording... Click again to stop and send.';
            statusDiv.style.color = '#28a745';
            
        })
        .catch(error => {
            console.error('Microphone access error:', error);
            statusDiv.textContent = '❌ Microphone access denied. Please enable microphone.';
            statusDiv.style.color = '#dc3545';
        });
}

function stopChatRecording() {
    const recordBtn = document.getElementById('record-btn');
    const recordText = document.getElementById('record-text');
    const statusDiv = document.getElementById('chat-status');
    
    if (chatMediaRecorder && chatMediaRecorder.state !== 'inactive') {
        chatMediaRecorder.stop();
        chatMediaRecorder.stream.getTracks().forEach(track => track.stop());
        
        // Update UI to stopped state
        isRecording = false;
        recordBtn.classList.remove('recording');
        recordText.textContent = 'Start Conversation';
        statusDiv.textContent = '⏳ Processing your message...';
        statusDiv.style.color = '#667eea';
    }
}

async function processChatMessage(audioBlob) {
    const statusDiv = document.getElementById('chat-status');
    const responseSection = document.getElementById('chat-response-section');
    const audioPlayer = document.getElementById('chat-audio-player');
    const processingTime = document.getElementById('chat-processing-time');
    const messageCount = document.getElementById('session-message-count');
    const voiceSelector = document.getElementById('chat-voice-selector');
    const modelSelector = document.getElementById('chat-model-selector');
    const autoContinue = document.getElementById('auto-continue-chat');
    
    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'chat_message.webm');
        formData.append('voice', voiceSelector.value);
        formData.append('model', modelSelector.value);
        formData.append('temperature', '0.7');
        
        statusDiv.textContent = '🚀 Chat Pipeline: Transcribe → Context → Think → Speak...';
        statusDiv.style.color = '#667eea';
        
        const startTime = Date.now();
        
        // Send to chat agent endpoint
        const response = await fetch(`/api/agent/chat/${currentSessionId}`, {
            method: 'POST',
            body: formData
        });
        
        const endTime = Date.now();
        const totalTime = ((endTime - startTime) / 1000).toFixed(2);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        // Check if the response indicates service failures
        const hasErrors = !data.success;
        const isAudioAvailable = data.audio_url && data.audio_url !== null;
        
        // Update UI with results
        processingTime.textContent = `${totalTime}s (Server: ${data.processing_time}s)`;
        messageCount.textContent = `${data.message_count} messages`;
        document.getElementById('message-count-display').textContent = data.message_count;
        
        // Add messages to conversation display
        const conversationDiv = document.getElementById('conversation-messages');
        const userTime = new Date().toLocaleTimeString();
        
        // Add user message with error indication if needed
        const userMsg = `
            <div class="message-item user-message">
                <div class="message-header">
                    🗣️ You <span class="message-time">${userTime}</span>
                </div>
                <div class="message-content">${data.transcribed_text}</div>
            </div>
        `;
        
        conversationDiv.insertAdjacentHTML('beforeend', userMsg);
        
        // Add AI response message
        if (data.ai_response) {
            const aiTime = new Date().toLocaleTimeString();
            const aiMsg = `
                <div class="message-item ai-message">
                    <div class="message-header">
                        🤖 AI Assistant <span class="message-time">${aiTime}</span>
                    </div>
                    <div class="message-content">${data.ai_response}</div>
                </div>
            `;
            conversationDiv.insertAdjacentHTML('beforeend', aiMsg);
        }
        
        // Scroll to bottom
        conversationDiv.scrollTop = conversationDiv.scrollHeight;
        
        // Show response section and play audio if available
        if (isAudioAvailable) {
            responseSection.style.display = 'block';
            
            // Set audio source and auto-play
            audioPlayer.src = data.audio_url;
            audioPlayer.load();
            
            // Auto-play when audio is loaded
            audioPlayer.oncanplay = function() {
                audioPlayer.play().catch(e => {
                    console.log('Auto-play prevented:', e);
                    // Show play button if auto-play fails
                    statusDiv.textContent = '🔊 Audio ready! Click to play.';
                });
            };
            
            statusDiv.textContent = '✅ Response ready! Audio playing automatically.';
            statusDiv.style.color = '#28a745';
            
            // Auto-continue if enabled
            if (autoContinue.checked && !hasErrors) {
                setTimeout(() => {
                    statusDiv.textContent = '🎙️ Ready for next message...';
                    statusDiv.style.color = '#495057';
                }, 3000);
            }
        } else {
            // Handle errors or no audio
            if (hasErrors) {
                statusDiv.textContent = '⚠️ Response generated but audio failed. Check console for details.';
                statusDiv.style.color = '#ffc107';
            } else {
                statusDiv.textContent = '✅ Response generated successfully!';
                statusDiv.style.color = '#28a745';
            }
        }
        
    } catch (error) {
        console.error('Chat processing error:', error);
        statusDiv.textContent = '❌ Error processing message: ' + error.message;
        statusDiv.style.color = '#dc3545';
        
        // Add error message to conversation
        const conversationDiv = document.getElementById('conversation-messages');
        const errorTime = new Date().toLocaleTimeString();
        const errorMsg = `
            <div class="message-item" style="background: #ffe6e6; border-left: 4px solid #dc3545;">
                <div class="message-header">
                    ❌ Error <span class="message-time">${errorTime}</span>
                </div>
                <div class="message-content">Failed to process message: ${error.message}</div>
            </div>
        `;
        conversationDiv.insertAdjacentHTML('beforeend', errorMsg);
        conversationDiv.scrollTop = conversationDiv.scrollHeight;
    }
}

// Session management functions
function generateSessionId() {
    const sessionInput = document.getElementById('session-id-input');
    const randomId = 'session_' + Math.random().toString(36).substr(2, 9);
    sessionInput.value = randomId;
    updateSessionId();
}

function updateSessionId() {
    const sessionInput = document.getElementById('session-id-input');
    const newSessionId = sessionInput.value.trim();
    
    if (newSessionId !== currentSessionId) {
        currentSessionId = newSessionId;
        document.getElementById('current-session-display').textContent = currentSessionId || 'Not set';
        
        // Clear conversation display when session changes
        if (currentSessionId) {
            document.getElementById('conversation-messages').innerHTML = 
                '<div style="color: #6c757d; font-style: italic; text-align: center; padding: 20px;">New session started. Begin your conversation...</div>';
            document.getElementById('message-count-display').textContent = '0';
        }
    }
}

function clearSession() {
    currentSessionId = '';
    document.getElementById('session-id-input').value = '';
    document.getElementById('current-session-display').textContent = 'Not set';
    document.getElementById('message-count-display').textContent = '0';
    document.getElementById('conversation-messages').innerHTML = 
        '<div style="color: #6c757d; font-style: italic; text-align: center; padding: 20px;">Session cleared. Start a new conversation...</div>';
    document.getElementById('chat-response-section').style.display = 'none';
    
    // Reset recording state
    if (isRecording) {
        stopChatRecording();
    }
}

function updateStatusDisplay() {
    const statusSpan = document.getElementById('status');
    if (currentSessionId) {
        statusSpan.textContent = `Ready for conversation (Session: ${currentSessionId})`;
    } else {
        statusSpan.textContent = 'Ready for conversation';
    }
}

// Utility functions for health checks (kept for debugging)
async function checkHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        console.log('Health check:', data);
    } catch (error) {
        console.error('Health check failed:', error);
    }
}

async function getVoiceAgents() {
    try {
        const response = await fetch('/api/voice-agents');
        const data = await response.json();
        console.log('Voice agents:', data);
    } catch (error) {
        console.error('Failed to get voice agents:', error);
    }
}
