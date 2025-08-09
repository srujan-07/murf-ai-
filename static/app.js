// Day 5: Echo Bot - MediaRecorder API with Upload
let mediaRecorder;
let recordedChunks = [];

const startBtn = document.getElementById('start-record-btn');
const stopBtn = document.getElementById('stop-record-btn');
const echoAudioSection = document.getElementById('echo-audio-section');
const echoAudioPlayer = document.getElementById('echo-audio-player');
const echoStatus = document.getElementById('echo-status');

function startRecording() {
    recordedChunks = [];
    echoStatus.textContent = 'Requesting microphone access...';
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = e => {
                if (e.data.size > 0) recordedChunks.push(e.data);
            };
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(recordedChunks, { type: 'audio/webm' });
                
                // Show local playback first
                echoAudioPlayer.src = URL.createObjectURL(audioBlob);
                echoAudioSection.style.display = 'block';
                echoStatus.textContent = 'Recording complete. Processing with Echo Bot v2...';
                
                // Day 7: Use new Echo Bot v2 with TTS
                await echoWithTTS(audioBlob);
            };
            mediaRecorder.start();
            startBtn.disabled = true;
            stopBtn.disabled = false;
            echoStatus.textContent = 'Recording... Speak now!';
        })
        .catch(err => {
            echoStatus.textContent = 'Microphone access denied: ' + err.message;
        });
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        startBtn.disabled = false;
        stopBtn.disabled = true;
        echoStatus.textContent = 'Processing audio...';
    }
}

// Day 6: Upload and transcribe recorded audio
async function uploadAudioToServer(audioBlob) {
    try {
        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'echo_recording.webm');
        
        echoStatus.textContent = '📤 Uploading audio to server...';
        
        const response = await fetch('/api/audio/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            echoStatus.innerHTML = `
                ✅ Upload successful!<br>
                📁 File: ${result.filename}<br>
                📊 Size: ${(result.size_bytes / 1024).toFixed(2)} KB<br>
                🎵 Type: ${result.content_type}<br>
                🎯 Now transcribing...
            `;
            
            // Day 6: Also transcribe the audio
            await transcribeAudio(audioBlob);
            
        } else {
            echoStatus.textContent = '❌ Upload failed: ' + result.message;
        }
        
    } catch (error) {
        console.error('Upload error:', error);
        echoStatus.textContent = '❌ Upload error: ' + error.message;
    }
}

// Day 6: Transcribe audio using AssemblyAI
async function transcribeAudio(audioBlob) {
    try {
        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'recording_to_transcribe.webm');
        
        echoStatus.textContent = '🎙️ Transcribing audio with AssemblyAI...';
        
        const response = await fetch('/api/transcribe/file', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Display transcription result
            const duration = result.audio_duration ? ` (${result.audio_duration.toFixed(1)}s)` : '';
            const confidence = result.confidence ? ` • Confidence: ${(result.confidence * 100).toFixed(1)}%` : '';
            
            echoStatus.innerHTML = `
                ✅ Transcription complete!${duration}${confidence}<br>
                📝 <strong>Transcript:</strong><br>
                <div style="background: white; border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px 0; font-style: italic; text-align: left;">
                    "${result.transcript}"
                </div>
            `;
        } else {
            echoStatus.innerHTML += '<br>❌ Transcription failed: ' + result.message;
        }
        
    } catch (error) {
        console.error('Transcription error:', error);
        echoStatus.innerHTML += '<br>❌ Transcription error: ' + error.message;
    }
}

// Day 7: Echo Bot v2 - Transcribe and replay with Murf TTS
async function echoWithTTS(audioBlob) {
    try {
        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'echo_recording.webm');
        formData.append('voice_id', 'en-US-natalie'); // You can make this configurable
        
        echoStatus.textContent = '🎙️ Step 1: Transcribing your voice...';
        
        const response = await fetch('/api/tts/echo', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Update status with transcription
            echoStatus.textContent = '🔊 Step 2: Generating Murf voice...';
            
            // Update the audio player with the new Murf TTS audio
            echoAudioPlayer.src = result.audio_url;
            echoAudioPlayer.load(); // Ensure the new audio loads
            
            // Display final result with transcript and confidence
            const confidence = result.confidence ? ` • Confidence: ${(result.confidence * 100).toFixed(1)}%` : '';
            
            echoStatus.innerHTML = `
                ✅ Echo Bot v2 Complete!${confidence}<br>
                🎤 <strong>What you said:</strong><br>
                <div style="background: #e3f2fd; border: 1px solid #1976d2; border-radius: 5px; padding: 10px; margin: 10px 0; font-style: italic; color: #1565c0;">
                    "${result.transcript}"
                </div>
                🔊 <strong>Now playing in ${result.voice_used} voice!</strong><br>
                <small>Click the play button below to hear your voice as ${result.voice_used}</small>
            `;
            
            // Auto-play the new TTS audio (if browser allows)
            try {
                await echoAudioPlayer.play();
            } catch (playError) {
                console.log('Auto-play prevented by browser:', playError);
            }
            
        } else {
            echoStatus.textContent = '❌ Echo Bot v2 failed: ' + result.message;
        }
        
    } catch (error) {
        console.error('Echo Bot v2 error:', error);
        echoStatus.textContent = '❌ Echo Bot v2 error: ' + error.message;
    }
}
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

// Day 8: Simple test function
function testLLM() {
    alert('Button clicked! Function is working.');
    const statusDiv = document.getElementById('llm-status');
    if (statusDiv) {
        statusDiv.textContent = '🧪 Button clicked - function is working!';
        statusDiv.style.color = '#28a745';
    }
    // Now call the actual function
    setTimeout(() => queryLLM(), 100);
}

// Day 8: LLM Query Function with Google Gemini
async function queryLLM() {
    console.log('🧪 queryLLM function called');
    
    const inputText = document.getElementById('llm-input').value.trim();
    const statusDiv = document.getElementById('llm-status');
    const responseDiv = document.getElementById('llm-response');
    const responseTextDiv = document.getElementById('llm-response-text');

    // Basic validation
    if (!inputText) {
        if (statusDiv) {
            statusDiv.textContent = '❌ Please enter your question or prompt';
            statusDiv.style.color = '#dc3545';
        }
        return;
    }

    // Show loading state
    if (statusDiv) {
        statusDiv.textContent = '🚀 Querying Gemini... Please wait.';
        statusDiv.style.color = '#667eea';
    }

    try {
        const response = await fetch('/api/llm/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: inputText,
                model: 'gemini-1.5-flash',
                temperature: 0.7,
                max_tokens: 500
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        // Display response
        if (responseTextDiv) {
            responseTextDiv.textContent = data.response;
        }
        
        if (responseDiv) {
            responseDiv.style.display = 'block';
        }
        
        if (statusDiv) {
            statusDiv.textContent = '✅ Response generated successfully!';
            statusDiv.style.color = '#28a745';
        }

        console.log('LLM Response:', data);

    } catch (error) {
        console.error('LLM Query Error:', error);
        if (statusDiv) {
            statusDiv.textContent = `❌ Error: ${error.message}`;
            statusDiv.style.color = '#dc3545';
        }
        if (responseDiv) {
            responseDiv.style.display = 'none';
        }
    }
}

// Add Enter key support for LLM input
document.addEventListener('DOMContentLoaded', () => {
    const llmInput = document.getElementById('llm-input');
    if (llmInput) {
        llmInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                e.preventDefault();
                queryLLM();
            }
        });
    }
});
