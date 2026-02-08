#!/usr/bin/env python3
"""
Desi Translate - Translation Manager Utility
Utility script to manage dictionaries, rules, and translations
"""

import json
import os
from pathlib import Path

RULES_DIR = Path(__file__).parent / 'rules'

def load_json(filename):
    """Load JSON file from rules directory"""
    filepath = RULES_DIR / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    """Save JSON file to rules directory"""
    filepath = RULES_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_word(word, translation, language_pair, pos='noun', rule='Direct translation', confidence=0.8):
    """Add a new word to dictionary"""
    dictionaries = load_json('dictionaries.json')
    
    if language_pair not in dictionaries:
        dictionaries[language_pair] = {}
    
    dictionaries[language_pair][word.lower()] = {
        'word': translation,
        'pos': pos,
        'rule': rule,
        'confidence': confidence
    }
    
    save_json('dictionaries.json', dictionaries)
    print(f"✓ Added: {word} → {translation} ({language_pair})")

def add_idiom(idiom, meaning, translations, explanation, example, origin=''):
    """Add a new idiom to database"""
    idioms = load_json('idioms.json')
    
    idioms[idiom.lower()] = {
        'meaning': meaning,
        'translations': translations,
        'explanation': explanation,
        'example': example,
        'origin': origin
    }
    
    save_json('idioms.json', idioms)
    print(f"✓ Added idiom: {idiom}")

def list_words(language_pair):
    """List all words in a language pair"""
    dictionaries = load_json('dictionaries.json')
    
    if language_pair not in dictionaries:
        print(f"Language pair {language_pair} not found")
        return
    
    words = dictionaries[language_pair]
    print(f"\n{language_pair} Dictionary ({len(words)} words):")
    print("-" * 50)
    
    for word, data in sorted(words.items()):
        print(f"  {word:20} → {data['word']:20} ({data['pos']})")

def list_idioms():
    """List all idioms in database"""
    idioms = load_json('idioms.json')
    
    print(f"\nIdiom Database ({len(idioms)} idioms):")
    print("-" * 50)
    
    for idiom in sorted(idioms.keys()):
        meaning = idioms[idiom]['meaning']
        print(f"  {idiom:30} - {meaning}")

def get_statistics():
    """Print translation database statistics"""
    dictionaries = load_json('dictionaries.json')
    grammar_rules = load_json('grammar_rules.json')
    idioms = load_json('idioms.json')
    
    print("\n" + "="*50)
    print("DESI TRANSLATE - DATABASE STATISTICS")
    print("="*50)
    
    # Dictionary stats
    print("\n📚 DICTIONARIES:")
    total_words = 0
    for lang_pair, words in dictionaries.items():
        count = len(words)
        total_words += count
        print(f"  {lang_pair:20} : {count:4} words")
    print(f"  {'Total':20} : {total_words:4} words")
    
    # Grammar rules stats
    print("\n📖 GRAMMAR RULES:")
    for rule_type, rules in grammar_rules.items():
        count = len(rules)
        print(f"  {rule_type:20} : {count:4} rules")
    
    # Idioms stats
    print("\n💡 IDIOMS:")
    print(f"  Total idioms        : {len(idioms):4}")
    
    # Language coverage
    languages = set()
    for lang_pair in dictionaries.keys():
        lang = lang_pair.split('_')[1]
        languages.add(lang)
    
    print("\n🌍 SUPPORTED LANGUAGES:")
    for lang in sorted(languages):
        print(f"  - {lang.capitalize()}")
    
    print("\n" + "="*50)

def export_for_backup(filename='translation_backup.json'):
    """Export all translation data for backup"""
    data = {
        'dictionaries': load_json('dictionaries.json'),
        'grammar_rules': load_json('grammar_rules.json'),
        'idioms': load_json('idioms.json')
    }
    
    backup_path = Path(__file__).parent / filename
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Backup created: {filename}")

def import_from_backup(filename='translation_backup.json'):
    """Import translation data from backup"""
    backup_path = Path(__file__).parent / filename
    
    if not backup_path.exists():
        print(f"Backup file not found: {filename}")
        return
    
    with open(backup_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    save_json('dictionaries.json', data['dictionaries'])
    save_json('grammar_rules.json', data['grammar_rules'])
    save_json('idioms.json', data['idioms'])
    
    print(f"✓ Backup restored from: {filename}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Desi Translate - Translation Manager")
        print("\nUsage:")
        print("  python manage_translations.py stats")
        print("  python manage_translations.py list-words en_hindi")
        print("  python manage_translations.py list-idioms")
        print("  python manage_translations.py backup")
        print("  python manage_translations.py restore")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'stats':
        get_statistics()
    elif command == 'list-words':
        if len(sys.argv) < 3:
            print("Usage: python manage_translations.py list-words <language_pair>")
            print("Example: python manage_translations.py list-words en_hindi")
        else:
            list_words(sys.argv[2])
    elif command == 'list-idioms':
        list_idioms()
    elif command == 'backup':
        export_for_backup()
    elif command == 'restore':
        import_from_backup()
    else:
        print(f"Unknown command: {command}")
