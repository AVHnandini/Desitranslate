"""
Voice Handler Module for Desi Translate
Handles speech-to-text and text-to-speech using SpeechRecognition and pyttsx3.
"""

import pyttsx3
import speech_recognition as sr
from typing import Optional, Tuple, List
import os
import threading


class VoiceHandler:
    """Handles voice input/output for translation"""
    
    def __init__(self):
        """Initialize voice handler with pyttsx3 engine"""
        try:
            self.tts_engine = pyttsx3.init()
            # Set default properties
            self.tts_engine.setProperty('rate', 150)  # Words per minute
            self.tts_engine.setProperty('volume', 0.9)  # Volume 0-1
        except Exception as e:
            print(f"Warning: Could not initialize text-to-speech: {e}")
            self.tts_engine = None
        
        try:
            self.recognizer = sr.Recognizer()
            # Optimize for recognizing Indian accents
            self.recognizer.energy_threshold = 4000  # Adjust for background noise
            self.recognizer.dynamic_energy_threshold = True
        except Exception as e:
            print(f"Warning: Could not initialize speech recognizer: {e}")
            self.recognizer = None
    
    # Language codes mapping for pyttsx3
    LANGUAGE_CODES = {
        'english': 'en',
        'en': 'en',
        'hindi': 'hi',
        'hi': 'hi',
        'telugu': 'te',
        'te': 'te',
        'tamil': 'ta',
        'ta': 'ta',
        'kannada': 'kn',
        'kn': 'kn',
        'malayalam': 'ml',
        'ml': 'ml'
    }
    
    def set_voice_properties(self, rate: int = 150, volume: float = 0.9):
        """
        Set voice properties for text-to-speech.
        
        Args:
            rate: Speech rate in words per minute (50-300)
            volume: Volume level (0.0-1.0)
        """
        if self.tts_engine:
            self.tts_engine.setProperty('rate', max(50, min(300, rate)))
            self.tts_engine.setProperty('volume', max(0.0, min(1.0, volume)))
    
    def set_voice_gender(self, gender: str = 'female'):
        """
        Set voice gender if available.
        
        Args:
            gender: 'male', 'female', or 'neutral'
        """
        if not self.tts_engine:
            return
        
        try:
            voices = self.tts_engine.getProperty('voices')
            for i, voice in enumerate(voices):
                if gender.lower() in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    return
        except Exception as e:
            print(f"Warning: Could not set voice gender: {e}")
    
    def text_to_speech(self,
                      text: str,
                      language: str = 'english',
                      save_to_file: Optional[str] = None,
                      block: bool = True) -> bool:
        """
        Convert text to speech and optionally save to file.
        
        Args:
            text: Text to convert
            language: Target language code
            save_to_file: Path to save audio file (optional)
            block: Whether to block until speech finishes
        
        Returns:
            True if successful, False otherwise
        """
        if not self.tts_engine:
            print("Text-to-speech engine not available")
            return False
        
        try:
            # Set language if supported by pyttsx3
            lang_code = self.LANGUAGE_CODES.get(language.lower(), 'en')
            
            if save_to_file:
                self.tts_engine.save_to_file(text, save_to_file)
            
            self.tts_engine.say(text)
            
            if block:
                self.tts_engine.runAndWait()
            
            return True
        
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            return False
    
    def text_to_speech_async(self,
                           text: str,
                           language: str = 'english',
                           callback: Optional[callable] = None):
        """
        Convert text to speech asynchronously.
        
        Args:
            text: Text to convert
            language: Target language code
            callback: Function to call when done
        """
        def speak_thread():
            self.text_to_speech(text, language, block=True)
            if callback:
                callback()
        
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()
    
    def speech_to_text(self,
                      duration: int = 5,
                      language: str = 'english',
                      microphone_index: Optional[int] = None) -> Tuple[str, float]:
        """
        Record speech and convert to text.
        
        Args:
            duration: Duration to record in seconds
            language: Expected language (for better recognition)
            microphone_index: Specific microphone to use
        
        Returns:
            Tuple of (recognized_text, confidence_score)
        """
        if not self.recognizer:
            print("Speech recognizer not available")
            return "", 0.0
        
        try:
            # Get microphone
            with sr.Microphone(device_index=microphone_index) as source:
                print(f"Listening for {duration} seconds...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Record audio
                audio_data = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            
            # Language mapping for Google Speech Recognition
            lang_map = {
                'english': 'en-US',
                'en': 'en-US',
                'hindi': 'hi-IN',
                'hi': 'hi-IN',
                'telugu': 'te-IN',
                'te': 'te-IN',
                'tamil': 'ta-IN',
                'ta': 'ta-IN',
                'kannada': 'kn-IN',
                'kn': 'kn-IN'
            }
            
            lang_code = lang_map.get(language.lower(), 'en-US')
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio_data, language=lang_code)
            confidence = 0.85  # Google doesn't directly provide confidence, estimate high
            
            print(f"Recognized: {text}")
            return text, confidence
        
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "", 0.0
        
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            return "", 0.0
        
        except Exception as e:
            print(f"Error in speech-to-text: {e}")
            return "", 0.0
    
    def list_microphones(self) -> List[Tuple[int, str]]:
        """
        List available microphones.
        
        Returns:
            List of (index, name) tuples
        """
        try:
            for i, microphone_name in enumerate(sr.Microphone.list_microphone_indexes()):
                print(f"Microphone {microphone_name}: {sr.Microphone.list_microphones()[i]}")
            
            return [(i, sr.Microphone.list_microphones()[i]) for i in range(len(sr.Microphone.list_microphones()))]
        
        except Exception as e:
            print(f"Error listing microphones: {e}")
            return []
    
    def save_audio_file(self,
                       text: str,
                       output_path: str,
                       language: str = 'english') -> bool:
        """
        Save text as audio file.
        
        Args:
            text: Text to convert
            output_path: Path to save audio file
            language: Target language
        
        Returns:
            True if successful, False otherwise
        """
        if not self.tts_engine:
            return False
        
        try:
            # Determine audio format based on file extension
            ext = output_path.split('.')[-1].lower()
            
            if ext not in ['wav', 'mp3', 'flac']:
                output_path = output_path + '.wav'
            
            self.tts_engine.save_to_file(text, output_path)
            self.tts_engine.runAndWait()
            
            return True
        
        except Exception as e:
            print(f"Error saving audio file: {e}")
            return False
    
    def recognize_from_file(self,
                          audio_file_path: str,
                          language: str = 'english') -> Tuple[str, float]:
        """
        Recognize speech from an audio file.
        
        Args:
            audio_file_path: Path to audio file
            language: Expected language
        
        Returns:
            Tuple of (recognized_text, confidence_score)
        """
        if not self.recognizer:
            return "", 0.0
        
        try:
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                audio_data = self.recognizer.record(source)
            
            # Language mapping
            lang_map = {
                'english': 'en-US',
                'en': 'en-US',
                'hindi': 'hi-IN',
                'hi': 'hi-IN',
                'telugu': 'te-IN',
                'te': 'te-IN',
                'tamil': 'ta-IN',
                'ta': 'ta-IN'
            }
            
            lang_code = lang_map.get(language.lower(), 'en-US')
            
            # Recognize
            text = self.recognizer.recognize_google(audio_data, language=lang_code)
            return text, 0.85
        
        except sr.UnknownValueError:
            return "", 0.0
        
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            return "", 0.0
        
        except Exception as e:
            print(f"Error recognizing audio file: {e}")
            return "", 0.0
    
    def close(self):
        """Cleanup resources"""
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass


class AudioProcessor:
    """Additional utilities for audio processing"""
    
    @staticmethod
    def normalize_audio_level(audio_path: str, target_path: str, target_db: float = -20.0) -> bool:
        """
        Normalize audio level (requires external tools).
        
        Args:
            audio_path: Input audio file
            target_path: Output audio file
            target_db: Target decibel level
        
        Returns:
            True if successful
        """
        try:
            from pydub import AudioSegment
            
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            
            # Calculate current loudness and adjust
            current_db = audio.dBFS
            diff = target_db - current_db
            
            # Apply gain
            normalized = audio.apply_gain(diff)
            
            # Export
            ext = target_path.split('.')[-1].lower()
            normalized.export(target_path, format=ext)
            
            return True
        
        except ImportError:
            print("pydub not installed. Install it with: pip install pydub")
            return False
        except Exception as e:
            print(f"Error normalizing audio: {e}")
            return False
    
    @staticmethod
    def trim_silence(audio_path: str, target_path: str, threshold_db: float = -40.0) -> bool:
        """
        Trim silence from beginning and end of audio.
        
        Args:
            audio_path: Input audio file
            target_path: Output audio file
            threshold_db: Threshold for silence detection
        
        Returns:
            True if successful
        """
        try:
            from pydub import AudioSegment
            from pydub.silence import detect_leading_silence, detect_trailing_silence
            
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            
            # Trim leading silence
            leading_silence = detect_leading_silence(audio, threshold=threshold_db)
            trimmed = audio[leading_silence:]
            
            # Trim trailing silence
            trailing_silence = detect_trailing_silence(trimmed, threshold=threshold_db)
            if trailing_silence > 0:
                trimmed = trimmed[:-trailing_silence]
            
            # Export
            ext = target_path.split('.')[-1].lower()
            trimmed.export(target_path, format=ext)
            
            return True
        
        except ImportError:
            print("pydub not installed. Install it with: pip install pydub")
            return False
        except Exception as e:
            print(f"Error trimming silence: {e}")
            return False
