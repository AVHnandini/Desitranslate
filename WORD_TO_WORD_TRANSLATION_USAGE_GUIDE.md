# How to Use Word-to-Word Translation Feature

## Quick Start

### Basic Translation with Word-to-Word Mapping

1. **Open the Translator Page**
   - Navigate to `http://localhost:5000/translator`
   - You'll see the enhanced translator interface

2. **Choose Languages**
   - **From Language**: Select any supported source language (English, Hindi, Telugu, Tamil, Spanish, French)
   - **To Language**: Select any supported target language

3. **Enter Text**
   - Type or paste text in the "Source Text" box (up to 500 characters)
   - Example: "I am learning machine translation"

4. **Click Translate**
   - Click the blue "Translate" button
   - The system processes your translation

5. **View Results**
   - **Translated Text**: Shows the translated output
   - **Confidence Score**: Shows overall translation confidence (0-100%)
   - **Word-to-Word Mapping**: Visual breakdown of each word translation

## Understanding Word-to-Word Mapping

The mapping displays two rows:

**Top Row (Source Language):**
- Shows each word from your input
- Displays part-of-speech tag (noun, verb, pronoun, etc.)

**Bottom Row (Target Language):**
- Shows each translated word
- Displays confidence percentage

Example:
```
Input:  I         am          learning      machine        translation
        pronoun → verb    →    verb      →    noun      →     noun
        ↓         ↓           ↓          ↓          ↓
Output: నేను      am         learning     machine       translation
        94%       50%         50%         50%           50%
```

## Interpreting Confidence Scores

- **90-100%**: High confidence - Dictionary match with good rule
- **70-89%**: Medium confidence - Known word with some uncertainty
- **50-69%**: Lower confidence - Word not found or approximated
- **Below 50%**: Very low - Word not translated

## Supported Language Pairs

### Direct Translations (Most Complete)
- English → Hindi, Telugu, Tamil, Spanish, French
- Hindi ↔ English
- Telugu ↔ English
- Hindi ↔ Telugu

### Expanding Coverage
More language pairs coming soon!

## Tips for Better Translations

1. **Use Complete Sentences**
   - "The cat is sleeping" (works well)
   - "cat sleeping" (less accurate)

2. **Avoid Slang/Abbreviations**
   - Full words translate better than abbreviations
   - "cannot" works better than "can't"

3. **Check Word Mappings**
   - Red/low confidence words may need review
   - Click on words to see confidence details (coming soon)

4. **Use Common Words**
   - Dictionary covers 150+ common English words
   - More extensive coverage for frequently used terms

## Examples

### Example 1: Simple English to Telugu
- **Input**: "Hello good morning"
- **Output**: "హలో good morning"
- **Confidence**: 95%
- Shows exact matches for "hello" and "morning"

### Example 2: Hindi to English
- **Input**: "नमस्ते मैं खुश हूं"
- **Output**: "hello i happy am"
- **Confidence**: 90%
- Shows native translation for all words

### Example 3: Mixed Language Pair
- **Input**: "I love water"
- **Output**: "నేను love నీరు"
- **Confidence**: 85%
- Shows partial translation (dictionary can be expanded)

## Features in the Word Mapping Display

### Interactive Hover
- Hover over any word to see:
  - Meaning in English
  - Translation rule applied
  - Part-of-speech details

### Confidence Color Coding
- **Green**: High confidence (80%+)
- **Orange**: Medium confidence (50-80%)
- **Red**: Low confidence (<50%)

### Responsive Layout
- On mobile: Words stack vertically
- On desktop: Words display in rows
- Automatically adapts to text length

## Troubleshooting

### "Word not found" Messages
- **Cause**: Word isn't in the dictionary yet
- **Solution**: Use a different but similar word, or help expand the dictionary

### Low Confidence Scores
- **Cause**: Word combination not in training data
- **Solution**: Try simpler sentences with more common words

### Translation Looks Wrong
- **Cause**: Word order rules differ between languages
- **Solution**: Review the word mapping to understand transformations

## Advanced Usage

### Batch Translation
(Coming soon) - Translate multiple sentences at once

### Custom Dictionary
(Coming soon) - Add your own word translations

### Export Results
- Click "Download" to save translation as .txt file
- Includes source text, translation, and mapping

## API Usage

For developers wanting to use word mappings programmatically:

```javascript
// JavaScript example
const response = await fetch('/api/translate-detailed', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        text: "I love India",
        source_lang: "en",
        target_lang: "hindi"
    })
});

const data = await response.json();

// Access word mappings
data.word_mappings.forEach(mapping => {
    console.log(`${mapping.source_word} → ${mapping.target_word}`);
    console.log(`Confidence: ${(mapping.confidence * 100).toFixed(0)}%`);
});
```

## Getting Help

1. **Check Dictionary Status**: Try translating with simpler words first
2. **Review Confidence**: Low confidence scores indicate uncertain translations
3. **Expand Dictionary**: More words and phrases coming in future updates

## Feedback

Help improve the feature:
- Report incorrect translations
- Suggest new words to add
- Recommend new language pairs
- Share use cases and examples

Your feedback helps us expand dictionary coverage and improve accuracy!
