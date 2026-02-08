from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import json
import os
from datetime import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from translation_validator import RobustTranslationWrapper, TranslationValidator

app = Flask(__name__)
app.secret_key = 'desi_translate_secret_key_2026'

# Database setup
DATABASE = 'users.db'

def init_db():
    """Initialize SQLite database for users"""
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
        conn.commit()
        conn.close()

def load_translation_rules():
    """Load translation rules from JSON files - using comprehensive versions"""
    rules_path = os.path.join(os.path.dirname(__file__), 'rules')
    
    # Try to load comprehensive files first, fall back to original files
    dict_file = os.path.join(rules_path, 'dictionaries_comprehensive.json')
    if not os.path.exists(dict_file):
        dict_file = os.path.join(rules_path, 'dictionaries.json')
    
    grammar_file = os.path.join(rules_path, 'grammar_rules_comprehensive.json')
    if not os.path.exists(grammar_file):
        grammar_file = os.path.join(rules_path, 'grammar_rules.json')
    
    idioms_file = os.path.join(rules_path, 'idioms_comprehensive.json')
    if not os.path.exists(idioms_file):
        idioms_file = os.path.join(rules_path, 'idioms.json')
    
    with open(dict_file, 'r', encoding='utf-8') as f:
        dictionaries = json.load(f)
    
    with open(grammar_file, 'r', encoding='utf-8') as f:
        grammar_rules = json.load(f)
    
    with open(idioms_file, 'r', encoding='utf-8') as f:
        idioms = json.load(f)
    
    return dictionaries, grammar_rules, idioms

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index_redirect():
    """Redirect to login or home"""
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and logic"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'message': 'Invalid request'}), 400
            
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'success': False, 'message': 'Username and password required'}), 400
            
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('SELECT id, password FROM users WHERE username = ?', (username,))
            user = c.fetchone()
            conn.close()
            
            if user and check_password_hash(user[1], password):
                session['user_id'] = user[0]
                session['username'] = username
                return jsonify({'success': True, 'message': 'Login successful'}), 200
            else:
                return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
        except Exception as e:
            return jsonify({'success': False, 'message': 'An error occurred'}), 500
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page and logic"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'message': 'Invalid request'}), 400
            
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            
            if not username or not email or not password:
                return jsonify({'success': False, 'message': 'All fields are required'}), 400
            
            if password != confirm_password:
                return jsonify({'success': False, 'message': 'Passwords do not match'}), 400
            
            if len(password) < 6:
                return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
            
            hashed_password = generate_password_hash(password)
            
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                     (username, email, hashed_password))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Registration successful'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'message': 'Username or email already exists'}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': 'An error occurred during registration'}), 500
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

# ==================== MAIN PAGES ====================

@app.route('/home')
@login_required
def home():
    """Home page with feature cards"""
    return render_template('index.html', username=session.get('username'))

@app.route('/text-translator')
@login_required
def text_translator():
    """Main text/voice translator page"""
    return render_template('translator.html', feature='text')

@app.route('/idiom-translator')
@login_required
def idiom_translator():
    """Idiom/Proverb translator page"""
    return render_template('idiom.html')

@app.route('/slang-normalizer')
@login_required
def slang_normalizer():
    """Chat/SMS Slang Normalizer page"""
    return render_template('slang.html')

@app.route('/historical-translator')
@login_required
def historical_translator():
    """Historical/Colonial Document Translator page"""
    return render_template('historical.html')

@app.route('/video-translator')
@login_required
def video_translator():
    """Video Subtitle Translator page"""
    return render_template('video.html')

# ==================== TRANSLATION API ROUTES ====================

def translate_text(text, source_lang='en', target_lang='hindi'):
    """Advanced sentence-level translation with grammar transformation and word-to-word mapping"""
    import re
    
    # Map language codes to full names
    lang_map = {
        'en': 'en',
        'hi': 'hindi',
        'te': 'telugu',
        'ta': 'tamil',
        'hindi': 'hindi',
        'telugu': 'telugu',
        'tamil': 'tamil'
    }
    
    source_lang = lang_map.get(source_lang.lower(), source_lang)
    target_lang = lang_map.get(target_lang.lower(), target_lang)
    
    dictionaries, grammar_rules, _ = load_translation_rules()
    
    # Get dictionary and rules for the language pair
    # Try: source_target, then target_source, then english_target if source is not english
    dict_key = f"{source_lang}_{target_lang}"
    word_dict = dictionaries.get(dict_key, {})
    
    # If no direct translation available, try reverse dictionary
    if not word_dict:
        reverse_key = f"{target_lang}_{source_lang}"
        word_dict = dictionaries.get(reverse_key, {})
    
    # If still no dictionary and source is not English, try English as intermediate
    if not word_dict and source_lang != 'en':
        en_target_key = f"en_{target_lang}"
        word_dict = dictionaries.get(en_target_key, {})
    
    # Step 1: Tokenize and extract punctuation
    words = text.lower().split()
    clean_words = []
    punctuation_map = {}
    
    for i, word in enumerate(words):
        leading_punct = ''
        trailing_punct = ''
        clean_word = word
        
        # Extract trailing punctuation
        while clean_word and clean_word[-1] in '.,!?;:\'"':
            trailing_punct = clean_word[-1] + trailing_punct
            clean_word = clean_word[:-1]
        
        # Extract leading punctuation
        while clean_word and clean_word[0] in '\'"(':
            leading_punct = leading_punct + clean_word[0]
            clean_word = clean_word[1:]
        
        clean_words.append(clean_word)
        punctuation_map[i] = {'leading': leading_punct, 'trailing': trailing_punct}
    
    # Step 2: Identify sentence structure (SVO parsing)
    subject_idx = -1
    verb_idx = -1
    object_idx = -1
    auxiliary_indices = []
    
    pos_tags = []
    for i, word in enumerate(clean_words):
        if word in word_dict:
            pos = word_dict[word].get('pos', 'noun')
        else:
            pos = get_pos_tag(word, grammar_rules)
        pos_tags.append(pos)
        
        # Simple heuristic SVO detection
        if pos == 'pronoun' and subject_idx == -1:
            subject_idx = i
        elif pos == 'verb':
            if verb_idx == -1:
                verb_idx = i
            elif word in ['is', 'are', 'was', 'were', 'do', 'does', 'did', 'will', 'can', 'could', 'may', 'might', 'must', 'should', 'would', 'shall']:
                auxiliary_indices.append(i)
        elif pos in ['noun', 'pronoun'] and verb_idx != -1 and object_idx == -1:
            object_idx = i
    
    # Step 3: Translate each word with detailed mapping
    word_translations = []  # Keep all translation info
    tense_info = 'present'
    
    for i, word in enumerate(clean_words):
        if word in word_dict:
            translated = word_dict[word]['word']
            rule = word_dict[word].get('rule', 'Direct translation')
            pos = word_dict[word].get('pos', 'noun')
            confidence = word_dict[word].get('confidence', 0.8)
            meaning = word_dict[word].get('meaning', '')
        else:
            translated = word
            rule = 'Word not found in dictionary'
            pos = get_pos_tag(word, grammar_rules)
            confidence = 0.5
            meaning = ''
        
        word_translations.append({
            'source_word': word,
            'target_word': translated,
            'source_pos': pos,
            'target_pos': pos,
            'rule': rule,
            'meaning': meaning,
            'confidence': confidence,
            'original_index': i
        })
    
    # Build translated_words list
    translated_words = [wt['target_word'] for wt in word_translations]
    word_mappings = word_translations
    
    # Step 4: Apply grammar transformations based on target language
    target_lang_lower = target_lang.lower()
    
    # Check if target language uses SOV word order (Indian languages)
    uses_sov = target_lang_lower in ['hindi', 'telugu', 'tamil', 'kannada', 'malayalam', 'marathi', 'punjabi']
    
    reordering_info = None
    if uses_sov and subject_idx != -1 and verb_idx != -1:
        # Reorder from SVO to SOV
        # SVO: Subject Verb Object → SOV: Subject Object Verb
        new_order = []
        
        # Add subject
        if subject_idx != -1:
            new_order.append(subject_idx)
        
        # Add objects and other words (except verb and auxiliaries)
        for i in range(len(clean_words)):
            if i not in [subject_idx, verb_idx] and i not in auxiliary_indices:
                new_order.append(i)
        
        # Add verb last (with auxiliaries merged)
        if verb_idx != -1:
            new_order.append(verb_idx)
        
        # Reorder translated words
        reordered = []
        for idx in new_order:
            if idx < len(translated_words):
                reordered.append(translated_words[idx])
        
        # Only use reordered if we have valid positions
        if len(reordered) == len(translated_words):
            translated_words = reordered
            reordering_info = {
                'original_order': list(range(len(clean_words))),
                'new_order': new_order,
                'rule': 'SVO to SOV word order transformation',
                'source_order': 'SVO (Subject-Verb-Object)',
                'target_order': 'SOV (Subject-Object-Verb)'
            }
    
    # Step 5: Handle auxiliary verb merging for target language
    # For Indian languages, merge auxiliary verbs into main verb
    if uses_sov and auxiliary_indices:
        # Remove auxiliaries from translated words if they shouldn't appear separately
        filtered_words = []
        for i, word in enumerate(translated_words):
            # Check if this was an auxiliary (rough estimate based on position)
            if i not in auxiliary_indices:
                filtered_words.append(word)
        
        if filtered_words and len(filtered_words) < len(translated_words):
            translated_words = filtered_words
    
    # Step 6: Build explanations for each word (in original order, not reordered)
    explanations = []
    for i, word in enumerate(clean_words):
        wt = word_translations[i] if i < len(word_translations) else {'target_word': word, 'confidence': 0, 'rule': 'Unknown'}
        
        if word in word_dict:
            explanations.append({
                'original': word,
                'translated': wt['target_word'],
                'pos': word_dict[word].get('pos', 'noun'),
                'rule': word_dict[word].get('rule', 'Direct translation'),
                'confidence': word_dict[word].get('confidence', 0.8),
                'meaning': word_dict[word].get('meaning', '')
            })
        else:
            explanations.append({
                'original': word,
                'translated': wt['target_word'],
                'pos': get_pos_tag(word, grammar_rules),
                'rule': 'Word not found - approximate translation',
                'confidence': 0.5,
                'meaning': ''
            })
    
    # Step 7: Reconstruct sentence with punctuation (use reordered translated_words)
    final_words = []
    for i, word in enumerate(translated_words):
        # Map back to get punctuation from original position
        original_idx = i if i < len(clean_words) else len(clean_words) - 1
        punct_info = punctuation_map.get(original_idx, {'leading': '', 'trailing': ''})
        final_words.append(punct_info['leading'] + word + punct_info['trailing'])
    
    translated_text = ' '.join(final_words)
    avg_confidence = sum(e['confidence'] for e in explanations) / len(explanations) if explanations else 0
    
    return {
        'translated_text': translated_text,
        'explanations': explanations,
        'confidence': round(avg_confidence * 100, 2),
        'word_mappings': word_mappings,
        'source_language': source_lang,
        'target_language': target_lang,
        'reordering_info': reordering_info
    }

# ==================== ADVANCED LINGUISTIC ANALYSIS ====================

def get_pos_tag(word, grammar_rules):
    """Get part of speech tag for a word using rule-based approach"""
    pos_tags = grammar_rules.get('pos_tags', {})
    
    # Simple rule-based POS detection
    verb_endings = ['ate', 'ing', 'ed', 'en']
    noun_indicators = ['tion', 'ment', 'ness', 'ity']
    adjective_indicators = ['ful', 'less', 'able', 'ible', 'ous', 'ious']
    adverb_indicators = ['ly']
    
    word_lower = word.lower()
    
    # Check for specific POS patterns
    if any(word_lower.endswith(ending) for ending in verb_endings):
        return 'verb'
    elif any(word_lower.endswith(ending) for ending in noun_indicators):
        return 'noun'
    elif any(word_lower.endswith(ending) for ending in adjective_indicators):
        return 'adjective'
    elif any(word_lower.endswith(ending) for ending in adverb_indicators):
        return 'adverb'
    elif word_lower in ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them']:
        return 'pronoun'
    elif word_lower in ['and', 'but', 'or', 'nor', 'yet']:
        return 'conjunction'
    elif word_lower in ['in', 'on', 'at', 'by', 'to', 'from', 'with', 'for']:
        return 'preposition'
    elif word_lower in ['hello', 'hi', 'bye', 'wow', 'oh', 'ah']:
        return 'interjection'
    else:
        return 'noun'  # Default to noun

def analyze_word_detailed(word, clean_word, target_lang, dictionaries, grammar_rules):
    """Generate detailed word-level explanation with linguistic analysis"""
    dict_key = f"en_{target_lang}"
    word_dict = dictionaries.get(dict_key, {})
    pos_tags = grammar_rules.get('pos_tags', {})
    
    # Get source language info
    source_pos = get_pos_tag(clean_word, grammar_rules)
    source_meaning = "word or phrase" if clean_word.lower() not in ['hello', 'good', 'morning', 'water', 'food', 'love'] else clean_word
    
    # Get target language info
    if clean_word in word_dict:
        word_data = word_dict[clean_word]
        translated_word = word_data.get('word', clean_word)
        target_pos = word_data.get('pos', source_pos)
        source_meaning = word_data.get('meaning', source_meaning)
        rule = word_data.get('rule', 'Direct translation')
        confidence = word_data.get('confidence', 0.8)
        
        # Get target language meaning if available
        target_meaning = word_data.get('meaning', '')
    else:
        translated_word = clean_word
        target_pos = 'unknown'
        rule = 'Word not found in dictionary'
        confidence = 0.5
        target_meaning = ''
    
    return {
        'original_word': clean_word,
        'original_with_punct': word,
        'source_pos': source_pos,
        'source_pos_full': pos_tags.get(source_pos, {}).get('description', source_pos),
        'source_meaning': source_meaning,
        'translated_word': translated_word,
        'target_pos': target_pos,
        'target_pos_full': pos_tags.get(target_pos, {}).get('description', target_pos) if target_pos != 'unknown' else 'Unknown',
        'target_meaning': target_meaning,
        'rule': rule,
        'confidence': confidence
    }

def generate_linguistic_explanation(text, target_lang, dictionaries, grammar_rules):
    """Generate comprehensive explanation of linguistic transformations"""
    word_order = grammar_rules.get('word_order', {})
    english_order = word_order.get('english', {}).get('order', 'SVO')
    target_order = word_order.get(target_lang, {}).get('order', 'SVO')
    
    explanations = []
    target_lang_lower = target_lang.lower()
    
    # 1. WORD ORDER EXPLANATION
    if english_order != target_order:
        if target_lang_lower in ['hindi', 'telugu', 'tamil']:
            explanations.append(f"📍 Word Order: English uses SVO (Subject-Verb-Object), but {target_lang} uses SOV (Subject-Object-Verb). Words are reordered: Object comes before Verb.")
        else:
            explanations.append(f"📍 Word Order: English uses {english_order} order, {target_lang} uses {target_order} order.")
    
    # 2. AUXILIARY VERB EXPLANATION  
    auxiliaries = grammar_rules.get('auxiliary_verb_rules', {}).get('english_auxiliaries', [])
    aux_in_text = [word.rstrip('.,!?;:') for word in text.lower().split() if word.rstrip('.,!?;:') in auxiliaries]
    
    if aux_in_text:
        unique_aux = list(set(aux_in_text))
        explanations.append(f"🔧 Auxiliary Verbs: The auxiliary verb(s) '{', '.join(unique_aux)}' {'is' if len(unique_aux) == 1 else 'are'} merged into the main verb. In {target_lang}, there's typically no separate auxiliary—the tense is shown in the main verb conjugation.")
    
    # 3. TENSE DETECTION & PRESERVATION
    text_lower = text.lower()
    tense_detected = 'present'
    tense_markers = []
    
    if 'was' in text_lower or 'were' in text_lower:
        tense_detected = 'past'
        tense_markers = ['was', 'were']
        explanations.append(f"⏰ Tense: PAST TENSE detected (marked by '{tense_markers[0]}'). Verbs conjugated to show past action in {target_lang}.")
    elif 'will' in text_lower or 'shall' in text_lower:
        tense_detected = 'future'
        tense_markers = ['will', 'shall']
        explanations.append(f"⏰ Tense: FUTURE TENSE detected (marked by '{tense_markers[0]}'). Verbs conjugated to show future action in {target_lang}.")
    elif any(word in text_lower for word in ['have', 'has']):
        tense_detected = 'present_perfect'
        explanations.append(f"⏰ Tense: PRESENT PERFECT detected. Shows completed action with present relevance in {target_lang}.")
    else:
        explanations.append(f"⏰ Tense: PRESENT TENSE detected. Verbs use present form in {target_lang}.")
    
    # 4. SUBJECT-OBJECT IDENTIFICATION
    pronouns = {'i': 'first person singular', 'you': 'second person', 'he': 'third person masculine', 'she': 'third person feminine', 'it': 'third person neuter', 'we': 'first person plural', 'they': 'third person plural'}
    text_pronouns = [word.rstrip('.,!?;:') for word in text.lower().split() if word.rstrip('.,!?;:') in pronouns]
    
    if text_pronouns:
        unique_pronouns = list(set(text_pronouns))
        explanations.append(f"👤 Subject: '{', '.join(unique_pronouns)}' ({', '.join([pronouns.get(p, 'unknown') for p in unique_pronouns])}). Affects verb conjugation and gender agreement in {target_lang}.")
    
    # 5. LANGUAGE-SPECIFIC NOTES
    if target_lang_lower == 'hindi':
        explanations.append("🇮🇳 Hindi: Verb conjugation changes based on subject gender (masculine/feminine), number (singular/plural), and tense. Postpositions may be used instead of prepositions.")
    elif target_lang_lower == 'telugu':
        explanations.append("🇮🇳 Telugu: Agglutinative language where suffixes are added for tense, mood, and person. Word order is strictly SOV.")
    elif target_lang_lower == 'tamil':
        explanations.append("🇮🇳 Tamil: Highly inflected language with rich verb conjugations. Feminine/masculine distinction less prominent in verbs than in nouns.")
    elif target_lang_lower == 'spanish':
        explanations.append("🇪🇸 Spanish: Verb conjugation crucial for marking person, number, tense. Pronouns often omitted as verb form indicates subject.")
    elif target_lang_lower == 'french':
        explanations.append("🇫🇷 French: Complex verb conjugation system. Many irregular verbs. Gender affects adjectives and some nouns.")
    
    return " | ".join(explanations) if explanations else "✓ Standard translation. Minimal grammatical transformation required."

def translate_text_detailed(text, source_lang='en', target_lang='hindi'):
    """Advanced translation with detailed linguistic analysis"""
    # Map language codes to full names
    lang_map = {
        'en': 'en',
        'hi': 'hindi',
        'te': 'telugu',
        'ta': 'tamil',
        'hindi': 'hindi',
        'telugu': 'telugu',
        'tamil': 'tamil'
    }
    
    source_lang = lang_map.get(source_lang.lower(), source_lang)
    target_lang = lang_map.get(target_lang.lower(), target_lang)
    
    dictionaries, grammar_rules, _ = load_translation_rules()
    
    # Get basic translation
    basic_translation = translate_text(text, source_lang, target_lang)
    
    # Perform detailed word analysis
    words = text.lower().split()
    detailed_explanations = []
    
    for word in words:
        # Separate punctuation
        punctuation = ''
        clean_word = word
        
        while clean_word and clean_word[-1] in '.,!?;:\'"':
            punctuation = clean_word[-1] + punctuation
            clean_word = clean_word[:-1]
        
        leading_punct = ''
        while clean_word and clean_word[0] in '\'"(':
            leading_punct = leading_punct + clean_word[0]
            clean_word = clean_word[1:]
        
        # Analyze word in detail
        word_analysis = analyze_word_detailed(word, clean_word, target_lang, dictionaries, grammar_rules)
        detailed_explanations.append(word_analysis)
    
    # Generate linguistic explanation
    linguistic_explanation = generate_linguistic_explanation(text, target_lang, dictionaries, grammar_rules)
    
    return {
        'translated_text': basic_translation['translated_text'],
        'original_text': text,
        'confidence': basic_translation['confidence'],
        'word_explanations': detailed_explanations,
        'word_mappings': basic_translation.get('word_mappings', []),
        'linguistic_explanation': linguistic_explanation,
        'basic_explanations': basic_translation['explanations'],
        'source_language': source_lang,
        'target_language': target_lang
    }

@app.route('/api/translate', methods=['POST'])
def api_translate():
    """Translate text API endpoint with error handling"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'hindi')
        
        if not text:
            return jsonify({
                'error': 'No text provided',
                'translated_text': '',
                'confidence': 0,
                'explanations': []
            }), 400
        
        # Use validator wrapper for safe translation
        validator = TranslationValidator()
        result = translate_text(text, source_lang, target_lang)
        validated_result = validator.validate_translation_output(result)
        
        return jsonify(validated_result), 200
        
    except Exception as e:
        # Fallback response on critical error
        return jsonify({
            'error': 'Translation service error',
            'translated_text': text,
            'confidence': 0,
            'explanations': [],
            'warnings': ['System fallback mode']
        }), 500

@app.route('/api/translate-detailed', methods=['POST'])
def api_translate_detailed():
    """Advanced translation with detailed linguistic analysis and error handling"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'hindi')
        
        if not text:
            return jsonify({
                'error': 'No text provided',
                'translated_text': '',
                'confidence': 0,
                'word_explanations': [],
                'linguistic_explanation': ''
            }), 400
        
        # Use validator wrapper for safe translation
        validator = TranslationValidator()
        result = translate_text_detailed(text, source_lang, target_lang)
        validated_result = validator.validate_translation_output(result)
        
        return jsonify(validated_result), 200
        
    except Exception as e:
        # Fallback response on critical error
        return jsonify({
            'error': 'Translation service error',
            'translated_text': text,
            'confidence': 0,
            'word_explanations': [],
            'linguistic_explanation': '',
            'warnings': ['System fallback mode']
        }), 500

def translate_idiom(idiom, target_lang='hindi'):
    """Translate idiom to target language"""
    _, _, idioms_dict = load_translation_rules()
    
    idiom_lower = idiom.lower().strip()
    
    # Try exact match first (with underscore format)
    idiom_with_underscore = idiom_lower.replace(' ', '_')
    if idiom_with_underscore in idioms_dict.get('idioms', {}):
        idiom_entry = idioms_dict['idioms'][idiom_with_underscore]
    else:
        # Try to find by matching English field
        idiom_entry = None
        for key, value in idioms_dict.get('idioms', {}).items():
            english_phrase = value.get('english', '').lower().strip()
            if english_phrase == idiom_lower or idiom_lower in english_phrase:
                idiom_entry = value
                break
    
    if idiom_entry:
        # Map language names to field names
        lang_map = {
            'hindi': 'hindi',
            'telugu': 'telugu',
            'tamil': 'tamil',
            'hi': 'hindi',
            'te': 'telugu',
            'ta': 'tamil'
        }
        target_field = lang_map.get(target_lang.lower(), target_lang.lower())
        
        return {
            'original': idiom_entry.get('english', idiom),
            'meaning': idiom_entry.get('meaning', idiom_entry.get('english_meaning', '')),
            'translation': idiom_entry.get(target_field, idiom_entry.get(f'{target_field}_meaning', '')),
            'explanation': idiom_entry.get('explanation', ''),
            'example': idiom_entry.get('example', ''),
            'cultural_note': idiom_entry.get('cultural_note', ''),
            'confidence': idiom_entry.get('confidence', 0.9)
        }
    else:
        return {
            'original': idiom,
            'meaning': 'Idiom not found',
            'translation': '',
            'explanation': 'This idiom is not in our database',
            'example': '',
            'cultural_note': '',
            'confidence': 0.0
        }

@app.route('/api/translate-idiom', methods=['POST'])
def api_translate_idiom():
    """Translate idiom API endpoint"""
    data = request.get_json()
    idiom = data.get('idiom')
    target_lang = data.get('target_lang', 'hindi')
    
    if not idiom:
        return jsonify({'error': 'No idiom provided'}), 400
    
    result = translate_idiom(idiom, target_lang)
    return jsonify(result), 200

def normalize_slang(text):
    """Normalize chat/SMS slang to proper English"""
    slang_dict = {
        'ur': 'your',
        'u': 'you',
        'r': 'are',
        'wud': 'would',
        'cd': 'could',
        'shud': 'should',
        'btw': 'by the way',
        'lol': 'laughing out loud',
        'omg': 'oh my god',
        'brb': 'be right back',
        'nvm': 'never mind',
        'thx': 'thanks',
        'pls': 'please',
        'msg': 'message',
        'str8': 'straight',
        'gr8': 'great',
        'l8r': 'later',
        'b4': 'before',
        '2': 'to',
        '4': 'for',
        '2day': 'today',
        '2morrow': 'tomorrow',
        'nite': 'night',
        'gud': 'good',
        'cuz': 'because',
        'c': 'see',
        'luv': 'love',
        'hbu': 'how about you',
        'ttyl': 'talk to you later'
    }
    
    words = text.lower().split()
    normalized_words = []
    explanations = []
    
    for word in words:
        clean_word = word.rstrip('.,!?;:')
        punctuation = word[len(clean_word):]
        
        if clean_word in slang_dict:
            normalized = slang_dict[clean_word]
            normalized_words.append(normalized + punctuation)
            explanations.append({
                'original': word,
                'normalized': normalized + punctuation,
                'type': 'slang',
                'explanation': f"Internet slang abbreviated form"
            })
        else:
            normalized_words.append(word)
            explanations.append({
                'original': word,
                'normalized': word,
                'type': 'normal',
                'explanation': 'Proper English'
            })
    
    normalized_text = ' '.join(normalized_words)
    return {
        'normalized_text': normalized_text,
        'explanations': explanations,
        'confidence': 0.85
    }

@app.route('/api/normalize-slang', methods=['POST'])
@login_required
def api_normalize_slang():
    """Normalize slang API endpoint"""
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = normalize_slang(text)
    return jsonify(result), 200

def translate_historical(text):
    """Convert old/historical English to modern English"""
    historical_dict = {
        'thee': 'you',
        'thou': 'you',
        'thy': 'your',
        'thine': 'yours',
        'hath': 'has',
        'doth': 'does',
        'art': 'are',
        'ere': 'before',
        'prithee': 'please',
        'forsooth': 'truly',
        'verily': 'indeed',
        'methinks': 'it seems to me',
        'betwixt': 'between',
        'wherefore': 'why',
        'whence': 'where',
        'thither': 'there',
        'hither': 'here',
        'naught': 'nothing',
        'aught': 'anything',
        'oft': 'often',
        'ne\'er': 'never',
        'o\'er': 'over',
        'mayhap': 'perhaps',
        'prune': 'trim',
        'withal': 'with',
        'shall': 'will',
        'hast': 'have',
        'am': 'am',
        'wast': 'was',
        'wert': 'were',
        'hadst': 'had',
        'canst': 'can',
        'dost': 'do',
        'shalt': 'will',
        'didst': 'did',
        'shouldst': 'should',
        'wouldst': 'would',
        'mightst': 'might',
        'mustst': 'must',
        'sayest': 'say',
        'goest': 'go',
        'comest': 'come',
        'givest': 'give',
        'takest': 'take',
        'knowest': 'know',
        'lovest': 'love',
        'seest': 'see',
        'believest': 'believe',
        'doest': 'do',
        'makest': 'make',
        'findest': 'find',
        'keepest': 'keep',
        'tellest': 'tell',
        'speakest': 'speak',
        'heareth': 'hears',
        'seeth': 'sees',
        'knoweth': 'knows',
        'loveth': 'loves',
        'speaketh': 'speaks',
        'goeth': 'goes',
        'cometh': 'comes',
        'giveth': 'gives',
        'taketh': 'takes',
        'maketh': 'makes',
        'saith': 'says',
        'doeth': 'does',
        'keepeth': 'keeps',
        'findeth': 'finds',
        'believeth': 'believes',
        'thinketh': 'thinks',
        'showeth': 'shows',
        'telleth': 'tells',
        'calleth': 'calls',
        'beareth': 'bears',
        'forbear': 'refrain from',
        'beseeched': 'begged',
        'beseech': 'beg',
        'prithee': 'please',
        'marry': 'indeed',
        'forsooth': 'truly',
        'nay': 'no',
        'yea': 'yes',
        'aye': 'yes',
        'good-bye': 'goodbye',
        'adieu': 'goodbye',
        'begone': 'go away',
        'hence': 'from here',
        'thence': 'from there',
        'henceforth': 'from now on',
        'thereafter': 'afterwards',
        'therein': 'in that',
        'thereupon': 'on that',
        'thereof': 'of that',
        'therewith': 'with that',
        'aforetime': 'previously',
        'anon': 'soon',
        'by and by': 'soon',
        'befall': 'happen to',
        'befallen': 'happened to',
        'become': 'suit',
        'becoming': 'suitable',
        'behoof': 'benefit',
        'demeanor': 'behavior',
        'countenance': 'face',
        'visage': 'face',
        'discourse': 'conversation',
        'converse': 'talk',
        'partake': 'share',
        'repast': 'meal',
        'supper': 'dinner',
        'breakfast': 'breakfast',
        'dinner': 'lunch',
        'promenade': 'walk',
        'carriage': 'car',
        'horse': 'horse',
        'mistress': 'woman',
        'lord': 'man',
        'lady': 'woman',
        'gentleman': 'man',
        'knave': 'fool',
        'varlet': 'rogue',
        'scoundrel': 'villain',
        'rogue': 'villain',
        'villain': 'villain',
        'miscreant': 'villain',
        'knight': 'knight',
        'squire': 'servant',
        'yeoman': 'farmer',
        'merchant': 'merchant',
        'peasant': 'farmer',
        'serf': 'slave',
        'vassal': 'servant',
        'apprentice': 'trainee',
        'journeyman': 'worker',
        'craftsman': 'worker',
        'blacksmith': 'metalworker',
        'miller': 'grain processor',
        'baker': 'baker',
        'butcher': 'butcher',
        'cobbler': 'shoemaker',
        'tailor': 'tailor',
        'weaver': 'weaver',
        'tanner': 'leather worker',
        'cordwainer': 'shoemaker'
    }
    
    words = text.lower().split()
    translated_words = []
    explanations = []
    
    for word in words:
        clean_word = word.rstrip('.,!?;:')
        punctuation = word[len(clean_word):]
        
        if clean_word in historical_dict:
            modern = historical_dict[clean_word]
            translated_words.append(modern + punctuation)
            explanations.append({
                'original': word,
                'modern': modern + punctuation,
                'era': 'Middle/Early Modern English',
                'explanation': f"Old English term meaning '{modern}'"
            })
        else:
            translated_words.append(word)
            explanations.append({
                'original': word,
                'modern': word,
                'era': 'Modern English',
                'explanation': 'Already in modern form'
            })
    
    modern_text = ' '.join(translated_words)
    return {
        'modern_text': modern_text,
        'explanations': explanations,
        'confidence': 0.88
    }

@app.route('/api/translate-historical', methods=['POST'])
@login_required
def api_translate_historical():
    """Translate historical English API endpoint"""
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = translate_historical(text)
    return jsonify(result), 200

@app.route('/api/translate-video', methods=['POST'])
@login_required
def api_translate_video():
    """Video subtitle translation API endpoint - translates EVERY word"""
    data = request.get_json()
    subtitles = data.get('subtitles', [])
    target_lang = data.get('target_lang', 'hindi')
    
    dictionaries, _, _ = load_translation_rules()
    
    # Get the dictionary for this language pair
    dict_key = f"en_{target_lang}"
    word_dict = dictionaries.get(dict_key, {})
    
    translated_subtitles = []
    
    for subtitle in subtitles:
        # Translate every word
        words = subtitle.lower().split()
        translated_words = []
        word_explanations = []
        
        for word in words:
            # Extract punctuation
            leading_punct = ''
            trailing_punct = ''
            clean_word = word
            
            while clean_word and clean_word[-1] in '.,!?;:\'"':
                trailing_punct = clean_word[-1] + trailing_punct
                clean_word = clean_word[:-1]
            
            while clean_word and clean_word[0] in '\'"(':
                leading_punct = leading_punct + clean_word[0]
                clean_word = clean_word[1:]
            
            # Translate the word
            if clean_word in word_dict:
                translated_word = word_dict[clean_word].get('word', clean_word)
                word_explanations.append({
                    'original': clean_word,
                    'translated': translated_word,
                    'meaning': word_dict[clean_word].get('meaning', ''),
                    'pos': word_dict[clean_word].get('pos', 'word')
                })
                translated_words.append(leading_punct + translated_word + trailing_punct)
            else:
                # If word not in dictionary, keep it as is (proper nouns, numbers, etc)
                translated_words.append(word)
                word_explanations.append({
                    'original': clean_word,
                    'translated': clean_word,
                    'meaning': 'Proper noun or special word',
                    'pos': 'proper_noun'
                })
        
        translated_text = ' '.join(translated_words)
        
        translated_subtitles.append({
            'original': subtitle,
            'translated': translated_text,
            'word_explanations': word_explanations,
            'words_translated': len([w for w in word_explanations if w['original'] != w['translated']]),
            'total_words': len(word_explanations)
        })
    
    return jsonify({
        'translated_subtitles': translated_subtitles,
        'total': len(translated_subtitles),
        'target_language': target_lang
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)
