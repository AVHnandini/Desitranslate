# Integration Guide for Desi Translate Modules

This guide explains how to use the newly created modules in your application.

## 1. NLP Engine Integration

### Import and Initialize

```python
from nlp_engine import NLPEngine, get_pos_tag_simple
import json

# Load your grammar rules and dictionaries
with open('rules/grammar_rules_comprehensive.json', 'r', encoding='utf-8') as f:
    grammar_rules = json.load(f)

with open('rules/dictionaries_comprehensive.json', 'r', encoding='utf-8') as f:
    dictionaries = json.load(f)

# Initialize NLP Engine
nlp_engine = NLPEngine(grammar_rules=grammar_rules, dictionaries=dictionaries)
```

### Use for Text Analysis

```python
# Analyze English text
text = "I love to read books"
analysis = nlp_engine.analyze_text(text)

print(f"Tokens: {analysis['tokens']}")
print(f"POS Tags: {analysis['pos_tags']}")
print(f"Tense: {analysis['tense']}")  # 'present'
print(f"Mood: {analysis['mood']}")    # 'indicative'

# Get sentence structure
structure = analysis['sentence_structure']
print(f"Subject index: {structure['subject_idx']}")
print(f"Verb index: {structure['verb_idx']}")
print(f"Object index: {structure['object_idx']}")
```

### Calculate Confidence Scores

```python
# Get dictionary coverage for translation
dict_key = "en_hindi"
coverage = nlp_engine.estimate_dictionary_coverage(tokens, dict_key)

# Calculate weighted confidence
confidence = nlp_engine.calculate_confidence_score(
    dictionary_coverage=0.85,
    grammar_match=0.90,
    source_reliability=0.95
)
# Result: (0.4 * 0.85) + (0.4 * 0.90) + (0.2 * 0.95) = 0.89
```

### Get Word Details

```python
# Get detailed information about a specific word
word_info = nlp_engine.get_word_details(
    word="hello",
    source_lang="en",
    target_lang="hindi"
)

print(f"Original: {word_info['word']}")
print(f"Translation: {word_info['translated']}")
print(f"POS: {word_info['pos']}")
print(f"Meaning: {word_info['meaning']}")
print(f"Confidence: {word_info['confidence']}")
print(f"Found: {word_info['found']}")
```

### Transform Word Order for SOV Languages

```python
# Get the new word order for SOV transformation
tokens = ["I", "love", "books"]
pos_tags = [("I", "PRP"), ("love", "VB"), ("books", "NNS")]

new_order = nlp_engine.get_sov_transformation_order(
    subject_idx=0,      # "I"
    verb_idx=1,         # "love"
    object_idx=2,       # "books"
    total_words=3
)
# Result: [0, 2, 1] for SOV transformation
```

## 2. Subtitle Processor Integration

### Import and Use

```python
from subtitle_processor import SubtitleProcessor, SubtitleEntry

processor = SubtitleProcessor()
```

### Parse Subtitle Files

```python
# Auto-detect format (SRT or VTT)
entries, format_type = processor.parse_subtitle_file('input.srt')

print(f"Loaded {len(entries)} subtitle entries in {format_type} format")

# Or specify format explicitly
entries = processor.parse_srt_file('movie.srt')
entries = processor.parse_vtt_file('video.vtt')
```

### Translate Subtitles

```python
# Import your translation function
from app import translate_text

# Translate all entries
translated_entries = processor.translate_entries(
    entries=entries,
    translate_func=translate_text,
    source_lang='en',
    target_lang='hi',
    batch_size=10
)

# Check translations
for entry in translated_entries:
    print(f"[{entry.start_time}] {entry.text}")
    print(f"  → {entry.translated_text}")
    print(f"  Confidence: {entry.translation_confidence}")
```

### Optimize Subtitles

```python
# Merge very short subtitles (< 500ms)
optimized = processor.merge_short_subtitles(entries, min_duration_ms=500)

# Split long subtitles (> 60 characters)
optimized = processor.split_long_subtitles(entries, max_chars=60)
```

### Save Translated Subtitles

```python
# Save as SRT
processor.save_to_srt(translated_entries, 'output.srt')

# Save as VTT
processor.save_to_vtt(translated_entries, 'output.vtt')

# Export as JSON for web storage
json_output = processor.to_json(translated_entries)
with open('subtitles.json', 'w', encoding='utf-8') as f:
    f.write(json_output)
```

## 3. Voice Handler Integration

### Import and Initialize

```python
from voice_handler import VoiceHandler, AudioProcessor

voice = VoiceHandler()
```

### Text-to-Speech

```python
# Simple text-to-speech
voice.text_to_speech(
    text="नमस्ते! यह देसी ट्रांसलेट है।",
    language='hindi',
    block=True  # Wait for speech to finish
)

# Async (non-blocking)
def on_complete():
    print("Speech complete!")

voice.text_to_speech_async(
    text="Hello, this is Desi Translate!",
    language='english',
    callback=on_complete
)

# Save to file
voice.save_audio_file(
    text="This is a test",
    output_path='output/audio.wav',
    language='english'
)
```

### Speech-to-Text

```python
# Record from microphone (5 seconds)
text, confidence = voice.speech_to_text(
    duration=5,
    language='hindi',
    microphone_index=0  # Optional: specific microphone
)

print(f"Recognized: {text}")
print(f"Confidence: {confidence}")

# Recognize from file
text, confidence = voice.recognize_from_file(
    audio_file_path='input/audio.wav',
    language='english'
)
```

### Voice Properties

```python
# Adjust speech rate and volume
voice.set_voice_properties(
    rate=150,        # Words per minute (50-300)
    volume=0.9       # Volume level (0.0-1.0)
)

# Set voice gender if available
voice.set_voice_gender('female')  # 'male', 'female', 'neutral'
```

### List Available Microphones

```python
microphones = voice.list_microphones()
for index, name in microphones:
    print(f"Microphone {index}: {name}")
```

### Audio Processing Utilities

```python
from voice_handler import AudioProcessor

# Normalize audio level to -20dB
AudioProcessor.normalize_audio_level(
    audio_path='input.wav',
    target_path='normalized.wav',
    target_db=-20.0
)

# Trim silence from audio
AudioProcessor.trim_silence(
    audio_path='input.wav',
    target_path='trimmed.wav',
    threshold_db=-40.0
)
```

## 4. Using All Modules Together

### Complete Translation Pipeline Example

```python
from nlp_engine import NLPEngine
from subtitle_processor import SubtitleProcessor
from voice_handler import VoiceHandler
from app import load_translation_rules
import json

# 1. Load resources
dictionaries, grammar_rules, idioms = load_translation_rules()
nlp_engine = NLPEngine(grammar_rules, dictionaries)
subtitle_processor = SubtitleProcessor()
voice = VoiceHandler()

# 2. Record speech
print("Recording your speech (5 seconds)...")
source_text, _ = voice.speech_to_text(duration=5, language='english')
print(f"You said: {source_text}")

# 3. Analyze text
analysis = nlp_engine.analyze_text(source_text)
print(f"Detected tense: {analysis['tense']}")
print(f"Detected mood: {analysis['mood']}")

# 4. Translate
from app import translate_text
translation = translate_text(source_text, 'en', 'hindi')

# 5. Speak result
voice.text_to_speech(
    text=translation,
    language='hindi',
    block=True
)

print(f"Translation: {translation}")
```

### Subtitle Translation Pipeline Example

```python
# 1. Load subtitle file
entries, format_type = subtitle_processor.parse_subtitle_file('movie.srt')

# 2. Analyze first subtitle for structure
analysis = nlp_engine.analyze_text(entries[0].text)
print(f"Analysis: {analysis['sentence_structure']}")

# 3. Translate all subtitles
from app import translate_text_detailed
translated = subtitle_processor.translate_entries(
    entries=entries,
    translate_func=translate_text_detailed,
    source_lang='en',
    target_lang='hindi'
)

# 4. Optimize
optimized = subtitle_processor.merge_short_subtitles(translated)

# 5. Save
subtitle_processor.save_to_srt(optimized, 'movie_hindi.srt')

# 6. Optionally speak first subtitle
voice.text_to_speech(
    text=optimized[0].translated_text,
    language='hindi'
)
```

## 5. API Integration in Flask

### Update app.py to use new modules

```python
from flask import Flask
from nlp_engine import NLPEngine
from subtitle_processor import SubtitleProcessor
from voice_handler import VoiceHandler
import json

app = Flask(__name__)

# Initialize modules at startup
def init_modules():
    global nlp_engine, subtitle_processor, voice_handler
    
    with open('rules/grammar_rules_comprehensive.json', 'r', encoding='utf-8') as f:
        grammar_rules = json.load(f)
    
    with open('rules/dictionaries_comprehensive.json', 'r', encoding='utf-8') as f:
        dictionaries = json.load(f)
    
    nlp_engine = NLPEngine(grammar_rules, dictionaries)
    subtitle_processor = SubtitleProcessor()
    voice_handler = VoiceHandler()

@app.before_first_request
def initialize():
    init_modules()

# API endpoint using NLP engine
@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get('text')
    
    analysis = nlp_engine.analyze_text(text)
    return jsonify({
        'tokens': analysis['tokens'],
        'pos_tags': analysis['pos_tags'],
        'tense': analysis['tense'],
        'mood': analysis['mood'],
        'structure': analysis['sentence_structure']
    })

# API endpoint for subtitle translation
@app.route('/api/translate-subtitles', methods=['POST'])
def translate_subtitles():
    # Handle file upload
    file = request.files['file']
    entries, format_type = subtitle_processor.parse_subtitle_file(file.filename)
    
    # Translate
    translated = subtitle_processor.translate_entries(
        entries=entries,
        translate_func=translate_text,
        source_lang=request.json['source_lang'],
        target_lang=request.json['target_lang']
    )
    
    # Return as JSON
    return jsonify({
        'subtitles': [e.to_dict() for e in translated],
        'format': format_type
    })

# API endpoint for voice
@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text_api():
    # Assuming audio file is uploaded
    audio_file = request.files['audio']
    language = request.json.get('language', 'english')
    
    text, confidence = voice_handler.recognize_from_file(
        audio_file_path=audio_file.filename,
        language=language
    )
    
    return jsonify({
        'text': text,
        'confidence': confidence
    })
```

## 6. Configuration and Setup

### Required Dependencies

```bash
pip install nltk==3.8.1
pip install pyttsx3==2.90
pip install SpeechRecognition==3.10.0
pip install pydub  # Optional, for audio processing
```

### Environment Setup

```python
# In your main app or config file
import nltk
import os

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

# Set encoding for Indian language support
os.environ['PYTHONIOENCODING'] = 'utf-8'
```

## 7. Error Handling

```python
# NLP Engine
try:
    analysis = nlp_engine.analyze_text(text)
except Exception as e:
    print(f"Error analyzing text: {e}")
    analysis = {"error": str(e)}

# Subtitle Processor
try:
    entries, format_type = subtitle_processor.parse_subtitle_file(path)
except FileNotFoundError:
    print(f"File not found: {path}")
except Exception as e:
    print(f"Error parsing subtitles: {e}")

# Voice Handler
try:
    text, confidence = voice.speech_to_text(duration=5)
    if confidence < 0.5:
        print("Low confidence recognition. Please repeat.")
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print(f"Speech recognition service error: {e}")
```

---

## 8. Performance Tips

1. **NLP Engine:** Cache analysis results for same text
2. **Subtitle Processor:** Use batch translation for multiple files
3. **Voice Handler:** Use async for non-blocking operations
4. **All Modules:** Initialize once at app startup

```python
# Good practice
nlp_engine = None

def get_nlp_engine():
    global nlp_engine
    if nlp_engine is None:
        nlp_engine = NLPEngine(grammar_rules, dictionaries)
    return nlp_engine

# Use throughout app
engine = get_nlp_engine()
```

---

**Last Updated:** January 27, 2026
