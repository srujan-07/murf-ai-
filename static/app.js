// Voice Agents Frontend JavaScript - Day 1
class VoiceAgentsApp {
    constructor() {
        this.baseUrl = window.location.origin;
        this.init();
    }

    init() {
        console.log('Voice Agents App initialized');
        this.checkHealthOnLoad();
    }

    async checkHealthOnLoad() {
        try {
            const response = await this.makeApiCall('/api/health');
            document.getElementById('status').textContent = 'API Ready ✅';
            document.getElementById('status').style.color = '#28a745';
        } catch (error) {
            document.getElementById('status').textContent = 'API Disconnected ❌';
            document.getElementById('status').style.color = '#dc3545';
        }
    }

    async makeApiCall(endpoint, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${this.baseUrl}${endpoint}`, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    displayResponse(data) {
        const responseDiv = document.getElementById('response');
        responseDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    }

    displayError(error) {
        const responseDiv = document.getElementById('response');
        responseDiv.innerHTML = `<div style="color: #dc3545;"><strong>Error:</strong> ${error.message}</div>`;
    }
}

// Day 3: Main TTS function - Generate and Play Audio
async function generateAndPlayAudio() {
    const textInput = document.getElementById('text-input');
    const voiceSelector = document.getElementById('voice-selector');
    const submitBtn = document.getElementById('submit-btn');
    const audioSection = document.getElementById('audio-section');
    const audioPlayer = document.getElementById('audio-player');
    const urlDisplay = document.getElementById('audio-url-display');
    const responseDiv = document.getElementById('response');
    
    const text = textInput.value.trim();
    const voiceId = voiceSelector.value;
    
    // Validation
    if (!text) {
        alert('Please enter some text to convert to speech!');
        textInput.focus();
        return;
    }
    
    if (text.length > 3000) {
        alert('Text is too long! Please keep it under 3000 characters.');
        return;
    }
    
    try {
        // Update UI - Loading state
        submitBtn.disabled = true;
        submitBtn.textContent = '🔄 Generating Audio...';
        urlDisplay.textContent = 'Generating audio, please wait...';
        audioSection.style.display = 'block';
        
        // Show progress in response area
        responseDiv.innerHTML = `
            <div style="color: #667eea;">
                <strong>🎤 Processing your request...</strong><br>
                Text: "${text.substring(0, 100)}${text.length > 100 ? '...' : ''}"<br>
                Voice: ${voiceSelector.options[voiceSelector.selectedIndex].text}<br>
                Status: Calling Murf API...
            </div>
        `;
        
        // Call the TTS API
        const response = await app.makeApiCall('/api/tts/generate', 'POST', {
            text: text,
            voice_id: voiceId
        });
        
        if (response.success && response.audio_url) {
            // Success! Update the audio player
            audioPlayer.src = response.audio_url;
            urlDisplay.textContent = response.audio_url;
            
            // Update response area with success info
            responseDiv.innerHTML = `
                <div style="color: #28a745;">
                    <strong>✅ Audio Generated Successfully!</strong><br>
                    ${response.message}<br>
                    Audio ID: ${response.audio_id || 'N/A'}<br>
                    Ready to play!
                </div>
            `;
            
            // Attempt to auto-play (browsers may prevent this)
            try {
                await audioPlayer.play();
                console.log('Audio started playing automatically');
            } catch (playError) {
                console.log('Auto-play prevented by browser - user must click play');
                responseDiv.innerHTML += `<br><small style="color: #ffc107;">Click the play button to start audio ▶️</small>`;
            }
            
        } else {
            throw new Error(response.message || 'TTS generation failed');
        }
        
    } catch (error) {
        console.error('TTS Error:', error);
        
        // Show error in UI
        responseDiv.innerHTML = `
            <div style="color: #dc3545;">
                <strong>❌ Error generating audio:</strong><br>
                ${error.message}<br>
                Please try again or check your connection.
            </div>
        `;
        
        urlDisplay.textContent = 'Error occurred during generation';
        audioSection.style.display = 'none';
        
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        submitBtn.textContent = '🔊 Generate & Play Audio';
    }
}

// Legacy functions for additional controls
async function checkHealth() {
    try {
        const response = await app.makeApiCall('/api/health');
        app.displayResponse(response);
    } catch (error) {
        app.displayError(error);
    }
}

async function getVoiceAgents() {
    try {
        const response = await app.makeApiCall('/api/voice-agents');
        app.displayResponse(response);
    } catch (error) {
        app.displayError(error);
    }
}

// Keyboard shortcut: Enter to submit (Ctrl+Enter for new line)
document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('text-input');
    if (textInput) {
        textInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.ctrlKey && !e.shiftKey) {
                e.preventDefault();
                generateAndPlayAudio();
            }
        });
        
        // Set default text for demo
        textInput.value = 'Hello! Welcome to Day 3 of the 30 Days of Voice Agents challenge. Today we are implementing audio playback functionality using HTML audio elements.';
    }
});

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new VoiceAgentsApp();
});

// Add some voice-related utilities for future days
class VoiceUtils {
    static async requestMicrophonePermission() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach(track => track.stop());
            return true;
        } catch (error) {
            console.error('Microphone permission denied:', error);
            return false;
        }
    }

    static checkBrowserSupport() {
        const support = {
            mediaDevices: !!navigator.mediaDevices,
            getUserMedia: !!navigator.mediaDevices?.getUserMedia,
            speechRecognition: 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window,
            speechSynthesis: 'speechSynthesis' in window
        };
        console.log('Browser voice support:', support);
        return support;
    }
}

// Check browser support on load
VoiceUtils.checkBrowserSupport();
