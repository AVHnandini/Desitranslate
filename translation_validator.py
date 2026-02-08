"""
Translation Validator & Error Handler
Ensures Desi Translate never fails, even with unknown words
"""

import logging
from typing import Dict, List, Tuple, Any

# Setup logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class TranslationValidator:
    """Validates and ensures robust translation output"""
    
    @staticmethod
    def validate_translation_output(result: Dict) -> Dict:
        """
        Validates translation result and fills missing fields
        Ensures output always has required fields
        """
        try:
            # Ensure all required fields exist
            required_fields = {
                'translated_text': '',
                'confidence': 0,
                'explanations': [],
                'word_mappings': [],
                'source_language': 'unknown',
                'target_language': 'unknown',
                'error': None,
                'warnings': []
            }
            
            # Merge with actual result
            for field, default in required_fields.items():
                if field not in result:
                    result[field] = default
            
            # Validate translated_text is not empty
            if not result.get('translated_text'):
                result['error'] = 'Translation produced empty result'
                logger.warning('Empty translation output detected')
                return result
            
            # Validate confidence is numeric and 0-100
            try:
                conf = float(result['confidence'])
                if not (0 <= conf <= 100):
                    result['confidence'] = max(0, min(100, conf))
                    result['warnings'].append('Confidence adjusted to 0-100 range')
            except (TypeError, ValueError):
                result['confidence'] = 0
                result['warnings'].append('Invalid confidence value - set to 0')
            
            # Validate explanations list
            if not isinstance(result['explanations'], list):
                result['explanations'] = []
                result['warnings'].append('Explanations not a list')
            
            # Validate each explanation has required fields
            for exp in result['explanations']:
                if not isinstance(exp, dict):
                    continue
                exp.setdefault('original', '?')
                exp.setdefault('translated', '?')
                exp.setdefault('pos', 'unknown')
                exp.setdefault('confidence', 0.5)
                exp.setdefault('rule', 'unknown rule')
                exp.setdefault('meaning', '')
            
            # Ensure at least one explanation per word
            words_in_text = result['translated_text'].split()
            if len(result['explanations']) < len(words_in_text):
                # Add placeholder explanations for missing words
                while len(result['explanations']) < len(words_in_text):
                    result['explanations'].append({
                        'original': '?',
                        'translated': words_in_text[len(result['explanations'])],
                        'pos': 'unknown',
                        'confidence': 0.3,
                        'rule': 'No explanation available',
                        'meaning': ''
                    })
                result['warnings'].append('Added placeholder explanations for missing entries')
            
            return result
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return {
                'translated_text': result.get('translated_text', '[Translation failed]'),
                'confidence': 0,
                'explanations': [],
                'word_mappings': [],
                'error': str(e),
                'warnings': ['Critical validation error occurred']
            }
    
    @staticmethod
    def fallback_translation(text: str, target_lang: str = 'unknown') -> Dict:
        """
        Provides fallback translation when main translation fails
        Returns original text with confidence 0 and explanatory notes
        """
        words = text.split()
        explanations = [
            {
                'original': word.strip('.,!?;:'),
                'translated': word.strip('.,!?;:'),
                'pos': 'unknown',
                'confidence': 0.0,
                'rule': 'Fallback: Word kept as-is due to translation failure',
                'meaning': 'Translation unavailable'
            }
            for word in words
        ]
        
        return {
            'translated_text': text,
            'confidence': 0,
            'explanations': explanations,
            'word_mappings': [],
            'source_language': 'unknown',
            'target_language': target_lang,
            'error': 'Translation failed - returned original text',
            'warnings': ['System fallback mode activated']
        }
    
    @staticmethod
    def check_dictionary_coverage(words: List[str], word_dict: Dict) -> Tuple[float, List[str]]:
        """
        Calculates how many words are in the dictionary
        Returns: (coverage_percentage, missing_words)
        """
        if not words:
            return 100.0, []
        
        missing = []
        found_count = 0
        
        for word in words:
            clean_word = word.lower().strip('.,!?;:')
            if clean_word in word_dict:
                found_count += 1
            else:
                missing.append(clean_word)
        
        coverage = (found_count / len(words)) * 100 if words else 0
        return coverage, missing
    
    @staticmethod
    def calculate_safe_confidence(
        dictionary_coverage: float,
        grammar_match: float = 0.8,
        known_words: int = 0,
        total_words: int = 0
    ) -> float:
        """
        Calculates confidence score with multiple factors
        Falls back gracefully if any factor is missing
        """
        try:
            # Base confidence from dictionary coverage
            dict_conf = dictionary_coverage / 100.0
            
            # Grammar matching factor
            gram_conf = grammar_match if 0 <= grammar_match <= 1 else 0.5
            
            # Known words ratio
            if total_words > 0:
                word_ratio = (known_words / total_words)
            else:
                word_ratio = 0.5
            
            # Weighted average: 40% dict + 40% grammar + 20% word ratio
            confidence = (0.4 * dict_conf) + (0.4 * gram_conf) + (0.2 * word_ratio)
            
            # Clamp to 0-1 range
            confidence = max(0.0, min(1.0, confidence))
            
            return round(confidence * 100, 2)
            
        except Exception as e:
            logger.warning(f"Confidence calculation error: {e}")
            return 50.0  # Default middle confidence on error


class RobustTranslationWrapper:
    """
    Wraps translation function with error handling
    Ensures system never crashes on bad input
    """
    
    def __init__(self, translate_func):
        self.translate_func = translate_func
        self.validator = TranslationValidator()
    
    def safe_translate(
        self,
        text: str,
        source_lang: str = 'en',
        target_lang: str = 'hindi'
    ) -> Dict:
        """
        Safely translates text with comprehensive error handling
        """
        try:
            # Input validation
            if not text or not isinstance(text, str):
                return self.validator.fallback_translation(
                    text or '[Empty input]',
                    target_lang
                )
            
            # Attempt translation
            result = self.translate_func(text, source_lang, target_lang)
            
            # Validate and fix output
            validated_result = self.validator.validate_translation_output(result)
            
            return validated_result
            
        except KeyError as e:
            # Missing key in dictionary or rules
            logger.warning(f"Missing key error: {e}")
            return self.validator.fallback_translation(text, target_lang)
            
        except ValueError as e:
            # Invalid value in processing
            logger.warning(f"Value error: {e}")
            return self.validator.fallback_translation(text, target_lang)
            
        except Exception as e:
            # Any other unexpected error
            logger.error(f"Unexpected translation error: {e}", exc_info=True)
            return self.validator.fallback_translation(text, target_lang)


# Example usage in Flask app:
"""
from app import translate_text_detailed
from translation_validator import RobustTranslationWrapper

# Wrap the translation function
translator = RobustTranslationWrapper(translate_text_detailed)

# Use in API endpoint
result = translator.safe_translate(text, source_lang, target_lang)
return jsonify(result)
"""
