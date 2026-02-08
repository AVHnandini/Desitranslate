"""
NLP Engine Module for Desi Translate
Provides advanced linguistic analysis, POS tagging, and confidence scoring.
"""

import json
import os
import re
from typing import Dict, List, Tuple, Optional
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet

# Download required NLTK data if not available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

# NLTK POS tag to simple POS mapping
POS_TAG_MAP = {
    'NN': 'noun',
    'NNS': 'noun',
    'NNP': 'noun',
    'NNPS': 'noun',
    'VB': 'verb',
    'VBD': 'verb',
    'VBG': 'verb',
    'VBN': 'verb',
    'VBP': 'verb',
    'VBZ': 'verb',
    'JJ': 'adjective',
    'JJR': 'adjective',
    'JJS': 'adjective',
    'RB': 'adverb',
    'RBR': 'adverb',
    'RBS': 'adverb',
    'PRP': 'pronoun',
    'PRP$': 'pronoun',
    'WP': 'pronoun',
    'WP$': 'pronoun',
    'IN': 'preposition',
    'CC': 'conjunction',
    'CD': 'number',
    'DT': 'determiner',
    'EX': 'determiner',
    'PDT': 'determiner',
    'WDT': 'determiner',
    'UH': 'interjection',
    'SYM': 'symbol',
    'FW': 'foreign_word',
    'MD': 'modal',
    'RP': 'particle',
    'TO': 'particle'
}

# Common English auxiliaries
AUXILIARIES = {
    'is', 'am', 'are', 'was', 'were',
    'be', 'been', 'being',
    'have', 'has', 'had',
    'do', 'does', 'did',
    'will', 'would', 'shall', 'should',
    'can', 'could', 'may', 'might', 'must',
    'ought', 'dare', 'need'
}

# Common English pronouns
PRONOUNS = {
    'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'me', 'him', 'her', 'us', 'them',
    'my', 'your', 'his', 'her', 'its', 'our', 'their',
    'mine', 'yours', 'hers', 'ours', 'theirs',
    'myself', 'yourself', 'himself', 'herself', 'itself',
    'ourselves', 'yourselves', 'themselves',
    'this', 'that', 'these', 'those',
    'who', 'whom', 'whose', 'which', 'what'
}

# Tense markers
PAST_MARKERS = {
    'was', 'were', 'did', 'had', 'have been',
    'had been', 'was going', 'were going'
}

PRESENT_MARKERS = {
    'is', 'am', 'are', 'have', 'has', 'do', 'does'
}

FUTURE_MARKERS = {
    'will', 'shall', 'going to', 'about to',
    'would', 'should'
}


class NLPEngine:
    """Advanced NLP engine for Indian language translation"""
    
    def __init__(self, grammar_rules: Dict = None, dictionaries: Dict = None):
        """
        Initialize NLP engine with grammar rules and dictionaries.
        
        Args:
            grammar_rules: Grammar rules JSON loaded from file
            dictionaries: Comprehensive dictionaries loaded from file
        """
        self.grammar_rules = grammar_rules or {}
        self.dictionaries = dictionaries or {}
    
    def tokenize_text(self, text: str) -> List[str]:
        """Tokenize text into words"""
        return word_tokenize(text.lower())
    
    def get_pos_tags(self, tokens: List[str]) -> List[Tuple[str, str]]:
        """
        Get POS tags for tokens using NLTK.
        
        Returns:
            List of (word, pos_tag) tuples
        """
        try:
            return pos_tag(tokens)
        except Exception as e:
            print(f"Error in POS tagging: {e}")
            return [(token, 'NN') for token in tokens]  # Fallback
    
    def simplify_pos(self, nltk_pos: str) -> str:
        """Convert NLTK POS tag to simple category"""
        return POS_TAG_MAP.get(nltk_pos, 'unknown')
    
    def analyze_sentence_structure(self, tokens: List[str], pos_tags: List[Tuple[str, str]]) -> Dict:
        """
        Analyze sentence structure to identify SVO/SOV pattern.
        
        Returns:
            Dict with subject_idx, verb_idx, object_idx, auxiliary_indices, analysis_type
        """
        analysis = {
            'subject_idx': -1,
            'verb_idx': -1,
            'object_idx': -1,
            'auxiliary_indices': [],
            'analysis_type': 'SVO',
            'structure': []
        }
        
        # Tag identification
        for i, (word, tag) in enumerate(pos_tags):
            simple_pos = self.simplify_pos(tag)
            
            # Store structure
            analysis['structure'].append({
                'word': word,
                'pos': simple_pos,
                'nltk_tag': tag,
                'index': i
            })
            
            # Identify subject (first pronoun or noun)
            if analysis['subject_idx'] == -1 and simple_pos in ['pronoun', 'noun']:
                analysis['subject_idx'] = i
            
            # Identify auxiliaries
            if word in AUXILIARIES:
                analysis['auxiliary_indices'].append(i)
            
            # Identify main verb (not auxiliary)
            elif simple_pos == 'verb' and word not in AUXILIARIES:
                if analysis['verb_idx'] == -1:
                    analysis['verb_idx'] = i
            
            # Identify object (noun/pronoun after verb)
            elif analysis['verb_idx'] != -1 and analysis['object_idx'] == -1:
                if simple_pos in ['noun', 'pronoun']:
                    analysis['object_idx'] = i
        
        # Determine if sentence is SVO (English) or needs SOV conversion (Indian languages)
        if analysis['subject_idx'] != -1 and analysis['verb_idx'] != -1:
            if analysis['subject_idx'] < analysis['verb_idx']:
                analysis['analysis_type'] = 'SVO'
            else:
                analysis['analysis_type'] = 'VSO or other'
        
        return analysis
    
    def detect_tense(self, tokens: List[str]) -> str:
        """
        Detect tense from auxiliary verbs and word patterns.
        
        Returns:
            'past', 'present', 'future', or 'present' (default)
        """
        text_lower = ' '.join(tokens).lower()
        
        # Check for future tense
        for marker in FUTURE_MARKERS:
            if marker in text_lower:
                return 'future'
        
        # Check for past tense
        for marker in PAST_MARKERS:
            if marker in text_lower:
                return 'past'
        
        # Check for present tense (default)
        for marker in PRESENT_MARKERS:
            if marker in text_lower:
                return 'present'
        
        return 'present'
    
    def detect_aspect(self, tokens: List[str]) -> str:
        """
        Detect grammatical aspect (simple, continuous, perfect, perfect continuous).
        
        Returns:
            Aspect type string
        """
        text_lower = ' '.join(tokens).lower()
        
        # Perfect continuous
        if ('have' in text_lower or 'has' in text_lower) and ('been' in text_lower and any(t.endswith('ing') for t in tokens)):
            return 'perfect_continuous'
        
        # Perfect
        if 'have' in text_lower or 'has' in text_lower or 'had' in text_lower:
            return 'perfect'
        
        # Continuous (progressive)
        if 'be' in text_lower or 'being' in text_lower or any(t.endswith('ing') for t in tokens):
            return 'continuous'
        
        # Simple
        return 'simple'
    
    def detect_mood(self, tokens: List[str]) -> str:
        """
        Detect grammatical mood (indicative, conditional, imperative, subjunctive).
        
        Returns:
            Mood type string
        """
        text_lower = ' '.join(tokens).lower()
        
        # Imperative: sentence starts with verb (no subject)
        if tokens and self.simplify_pos(pos_tag([tokens[0]])[0][1]) == 'verb':
            if tokens[0] not in AUXILIARIES and tokens[0] not in PRONOUNS:
                return 'imperative'
        
        # Conditional
        if 'would' in text_lower or 'could' in text_lower or 'should' in text_lower:
            return 'conditional'
        
        # Subjunctive (rare in modern English, look for "if" or specific constructions)
        if text_lower.startswith('if ') or ' if ' in text_lower:
            return 'subjunctive'
        
        # Default: indicative
        return 'indicative'
    
    def calculate_confidence_score(self,
                                   dictionary_coverage: float,
                                   grammar_match: float,
                                   source_reliability: float) -> float:
        """
        Calculate confidence score using weighted formula.
        
        Formula: (0.4 * dict_coverage) + (0.4 * grammar_match) + (0.2 * source_reliability)
        
        Args:
            dictionary_coverage: Percentage of words found in dictionary (0-1)
            grammar_match: Confidence in grammar rule application (0-1)
            source_reliability: Reliability of data source (0-1)
        
        Returns:
            Combined confidence score (0-1)
        """
        score = (0.4 * dictionary_coverage) + (0.4 * grammar_match) + (0.2 * source_reliability)
        return min(1.0, max(0.0, score))
    
    def analyze_text(self, text: str) -> Dict:
        """
        Comprehensive text analysis.
        
        Returns:
            Dict with tokens, pos_tags, sentence_structure, tense, aspect, mood, analysis
        """
        # Tokenize
        tokens = self.tokenize_text(text)
        
        # Get POS tags
        pos_tags = self.get_pos_tags(tokens)
        
        # Analyze structure
        structure_analysis = self.analyze_sentence_structure(tokens, pos_tags)
        
        # Detect linguistic features
        tense = self.detect_tense(tokens)
        aspect = self.detect_aspect(tokens)
        mood = self.detect_mood(tokens)
        
        return {
            'tokens': tokens,
            'pos_tags': [(word, self.simplify_pos(tag)) for word, tag in pos_tags],
            'nltk_pos_tags': pos_tags,
            'sentence_structure': structure_analysis,
            'tense': tense,
            'aspect': aspect,
            'mood': mood,
            'analysis': {
                'text': text,
                'token_count': len(tokens),
                'subject_index': structure_analysis['subject_idx'],
                'verb_index': structure_analysis['verb_idx'],
                'object_index': structure_analysis['object_idx'],
                'has_auxiliaries': len(structure_analysis['auxiliary_indices']) > 0,
                'auxiliary_count': len(structure_analysis['auxiliary_indices'])
            }
        }
    
    def get_word_details(self, word: str, source_lang: str = 'en', target_lang: str = 'hindi') -> Dict:
        """
        Get detailed information about a word from dictionaries.
        
        Returns:
            Dict with word, pos, meaning, confidence, source
        """
        dict_key = f"{source_lang}_{target_lang}"
        
        # Get word from dictionary
        word_dict = self.dictionaries.get(dict_key, {})
        
        # Skip metadata
        word_dict = {k: v for k, v in word_dict.items() if k != 'metadata'}
        
        if word in word_dict:
            entry = word_dict[word]
            return {
                'word': word,
                'translated': entry.get('word', word),
                'pos': entry.get('pos', 'unknown'),
                'meaning': entry.get('meaning', ''),
                'rule': entry.get('rule', ''),
                'confidence': entry.get('confidence', 0.5),
                'source': entry.get('source', 'dictionary'),
                'found': True
            }
        else:
            return {
                'word': word,
                'translated': word,
                'pos': 'unknown',
                'meaning': '',
                'rule': 'Word not found in dictionary',
                'confidence': 0.3,
                'source': 'approximate',
                'found': False
            }
    
    def get_sov_transformation_order(self,
                                    subject_idx: int,
                                    verb_idx: int,
                                    object_idx: int,
                                    total_words: int,
                                    auxiliary_indices: List[int] = None) -> List[int]:
        """
        Calculate word reordering for SVO to SOV transformation.
        
        Args:
            subject_idx: Index of subject
            verb_idx: Index of main verb
            object_idx: Index of object
            total_words: Total number of words
            auxiliary_indices: List of auxiliary verb indices
        
        Returns:
            List of indices in new order for SOV
        """
        auxiliary_indices = auxiliary_indices or []
        new_order = []
        
        # Add subject first
        if subject_idx != -1:
            new_order.append(subject_idx)
        
        # Add all other words except main verb and auxiliaries
        for i in range(total_words):
            if i not in [subject_idx, verb_idx] and i not in auxiliary_indices:
                new_order.append(i)
        
        # Add main verb last (with merged auxiliaries)
        if verb_idx != -1:
            new_order.append(verb_idx)
        
        # Handle missing indices by filling gaps
        if len(new_order) != total_words:
            all_indices = set(range(total_words))
            used = set(new_order)
            missing = sorted(all_indices - used)
            new_order.extend(missing)
        
        return new_order[:total_words]
    
    def estimate_dictionary_coverage(self, tokens: List[str], dict_key: str) -> float:
        """
        Estimate what percentage of tokens are in the dictionary.
        
        Returns:
            Coverage ratio (0-1)
        """
        if not tokens:
            return 0.0
        
        word_dict = self.dictionaries.get(dict_key, {})
        word_dict = {k: v for k, v in word_dict.items() if k != 'metadata'}
        
        found_count = sum(1 for token in tokens if token in word_dict)
        return found_count / len(tokens)


# Utility functions for backward compatibility

def get_pos_tag_simple(word: str, grammar_rules: Dict = None) -> str:
    """
    Simple POS tagging fallback function.
    Used for backward compatibility with existing code.
    """
    word_lower = word.lower()
    
    # Check grammar rules if available
    if grammar_rules:
        for pos_category, rules in grammar_rules.get('pos_tags', {}).items():
            if isinstance(rules, dict):
                indicators = rules.get('english_indicators', [])
                if word_lower in indicators:
                    return pos_category.lower()
    
    # Heuristic fallback
    if word_lower in PRONOUNS:
        return 'pronoun'
    elif word_lower in AUXILIARIES:
        return 'auxiliary'
    elif word_lower.endswith('ing'):
        return 'verb'
    elif word_lower.endswith('ly'):
        return 'adverb'
    elif word_lower in {'the', 'a', 'an'}:
        return 'determiner'
    else:
        return 'noun'  # Default
