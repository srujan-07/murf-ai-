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
            document.getElementById('status').textContent = 'Connected ✅';
            document.getElementById('status').style.color = '#28a745';
        } catch (error) {
            document.getElementById('status').textContent = 'Disconnected ❌';
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

// Global functions for button clicks
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

function testTTS() {
    const ttsInput = document.getElementById('tts-input');
    const isVisible = ttsInput.style.display !== 'none';
    
    if (isVisible) {
        ttsInput.style.display = 'none';
        document.getElementById('audio-player').style.display = 'none';
    } else {
        ttsInput.style.display = 'block';
        // Set default text
        document.getElementById('tts-text').value = 'Hello! This is Day 2 of my 30 Days of Voice Agents challenge. I have successfully integrated Murf AI for text-to-speech conversion!';
    }
}

async function generateTTS() {
    const text = document.getElementById('tts-text').value.trim();
    const voiceId = document.getElementById('voice-select').value;
    
    if (!text) {
        alert('Please enter some text to convert to speech!');
        return;
    }
    
    try {
        // Show loading
        const responseDiv = document.getElementById('response');
        responseDiv.innerHTML = '<div style="color: #667eea;"><strong>🎤 Generating audio...</strong> Please wait while Murf creates your speech.</div>';
        
        const response = await app.makeApiCall('/api/tts/generate', 'POST', {
            text: text,
            voice_id: voiceId
        });
        
        if (response.success && response.audio_url) {
            // Show success message
            app.displayResponse({
                ...response,
                message: `✅ Audio generated successfully! Duration: ~${Math.ceil(text.length / 10)} seconds`
            });
            
            // Show audio player
            const audioPlayer = document.getElementById('audio-player');
            const audioElement = document.getElementById('audio-element');
            const audioLink = document.getElementById('audio-link');
            
            audioElement.src = response.audio_url;
            audioLink.href = response.audio_url;
            audioLink.textContent = response.audio_url;
            
            audioPlayer.style.display = 'block';
            
            // Auto-play the audio (if browser allows)
            try {
                await audioElement.play();
            } catch (playError) {
                console.log('Auto-play prevented by browser. User needs to click play.');
            }
            
        } else {
            app.displayError(new Error('TTS generation failed: ' + response.message));
        }
        
    } catch (error) {
        app.displayError(error);
    }
}

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
