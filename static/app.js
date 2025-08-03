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

    async makeApiCall(endpoint) {
        const response = await fetch(`${this.baseUrl}${endpoint}`);
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
