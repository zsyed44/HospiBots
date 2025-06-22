# speech_recognizer.py

import pyaudio
import wave
import tempfile
import os

# Optional Google Cloud import with fallback
try:
    from google.cloud import speech
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("Warning: Google Cloud Speech library not found. Speech-to-text will be disabled.")

class SimpleVoiceRecorder:
    """Lightweight voice recorder for command capture"""
    
    def __init__(self):
        self.rate = 16000
        self.channels = 1
        self.format = pyaudio.paInt16
        self.chunk = 1024
        self.max_duration = 5 # Maximum recording duration
        
        self.speech_enabled = False # Assume false until verified
        if SPEECH_AVAILABLE:
            try:
                # If not using a service account key file, make sure gcloud is authenticated
                self.speech_client = speech.SpeechClient()
                self.speech_enabled = True
                print("Google Cloud Speech-to-Text client initialized.")
            except Exception as e:
                print(f"Error initializing Google Cloud Speech client: {e}")
                print("Speech-to-text will be disabled. Please ensure authentication is correctly configured.")
                self.speech_enabled = False
        else:
            print("Google Cloud Speech library not available. Speech-to-text will be disabled.")


    def record_command(self) -> str:
        """Record voice command and return text"""
        if not self.speech_enabled:
            print("Speech-to-text is not enabled or failed to initialize.")
            return ""
            
        try:
            audio = pyaudio.PyAudio()
            print("🎤 Listening... (speak now)")
            
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            frames = []
            # Parameters for silence detection
            silence_threshold = 500  # Adjust based on your microphone and environment (avg amplitude)
            max_silence_chunks = int(1.5 * self.rate / self.chunk) # 1.5 seconds of silence to stop
            silence_count = 0
            
            print(f"Recording for max {self.max_duration} seconds or until silence detected...")

            for _ in range(0, int(self.rate / self.chunk * self.max_duration) + max_silence_chunks):
                data = stream.read(self.chunk, exception_on_overflow=False)
                frames.append(data)
                
                # Simple silence detection
                # Convert bytes to short integers for amplitude check
                audio_data = wave.struct.unpack(f"{self.chunk}h", data)
                max_amplitude = max(abs(sample) for sample in audio_data)
                
                if max_amplitude < silence_threshold:
                    silence_count += 1
                    if silence_count > max_silence_chunks:
                        print("Silence detected. Stopping recording.")
                        break
                else:
                    silence_count = 0 # Reset silence counter if sound is detected
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            return self._audio_to_text(frames)
            
        except Exception as e:
            print(f"Error during audio recording: {e}")
            return ""

    def _audio_to_text(self, frames) -> str:
        """Convert audio to text using Google Cloud Speech-to-Text"""
        if not self.speech_enabled:
            return "" # Should not be called if speech is not enabled
            
        try:
            # Use tempfile.NamedTemporaryFile to handle file creation and cleanup securely
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_file_name = temp_file.name
                with wave.open(temp_file_name, 'wb') as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.format))
                    wf.setframerate(self.rate)
                    wf.writeframes(b''.join(frames))
            
            with open(temp_file_name, 'rb') as f:
                audio_content = f.read()
            
            audio = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.rate,
                language_code='en-US',
                model='command_and_search', # Optimized for short commands and search queries
                # You can add hints for better recognition if you have specific commands
                # speech_contexts=[{"phrases": ["move to room 100", "shutdown", "service room"]}]
            )
            
            print("Transcribing audio...")
            response = self.speech_client.recognize(config=config, audio=audio)
            
            os.unlink(temp_file_name) # Clean up the temporary file

            if response.results:
                text = response.results[0].alternatives[0].transcript
                print(f"Heard: '{text}'")
                return text.lower().strip()
            print("No speech recognized.")
            return ""
                
        except Exception as e:
            print(f"Error during audio transcription: {e}")
            # Ensure temp file is cleaned up even if an error occurs
            if 'temp_file_name' in locals() and os.path.exists(temp_file_name):
                os.unlink(temp_file_name)
            return ""

