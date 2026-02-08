// ===========================
// IDIOM TRANSLATOR JAVASCRIPT
// ===========================

// Store current idiom data for voice playback
let currentIdiomData = null;
let currentTargetLang = 'hindi';

// Speech synthesis object
const synth = window.speechSynthesis;

document.addEventListener('DOMContentLoaded', function() {
    setupIdiomTranslator();
});

function setupIdiomTranslator() {
    const idiomInput = document.getElementById('idiomInput');
    const targetLang = document.getElementById('targetLang');
    const clearBtn = document.getElementById('clearBtn');
    const translateBtn = document.getElementById('translateBtn');
    const copyBtn = document.getElementById('copyBtn');
    const speakInputBtn = document.getElementById('speakInputBtn');
    const speakTranslationBtn = document.getElementById('speakTranslationBtn');
    
    // Panel toggle buttons
    const toggleExplanationBtn = document.getElementById('toggleExplanationPanel');
    const toggleExampleBtn = document.getElementById('toggleExamplePanel');
    const toggleReferenceBtn = document.getElementById('toggleReferencePanel');
    const togglePronunciationBtn = document.getElementById('togglePronunciationPanel');
    
    // Clear button
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            idiomInput.value = '';
            idiomInput.focus();
        });
    }
    
    // Speak input button
    if (speakInputBtn) {
        speakInputBtn.addEventListener('click', function() {
            const text = idiomInput.value;
            if (text.trim()) {
                speakText(text, 'en-US');
            } else {
                alert('Please enter an idiom to speak');
            }
        });
    }
    
    // Speak translation button
    if (speakTranslationBtn) {
        speakTranslationBtn.addEventListener('click', function() {
            if (currentIdiomData) {
                const translation = currentIdiomData.translation || '';
                if (translation) {
                    const langCode = getLangCode(currentTargetLang);
                    speakText(translation, langCode);
                }
            }
        });
    }
    
    // Translate button
    if (translateBtn) {
        translateBtn.addEventListener('click', function() {
            translateIdiom();
        });
    }
    
    // Copy button
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const result = document.getElementById('idiomResult').textContent;
            copyToClipboard(result);
        });
    }
    
    // Panel toggles
    if (toggleExplanationBtn) {
        toggleExplanationBtn.addEventListener('click', function() {
            togglePanel('.explanation-panel .panel-content', toggleExplanationBtn);
        });
    }
    
    if (toggleExampleBtn) {
        toggleExampleBtn.addEventListener('click', function() {
            togglePanel('.example-panel .panel-content', toggleExampleBtn);
        });
    }
    
    if (toggleReferenceBtn) {
        toggleReferenceBtn.addEventListener('click', function() {
            togglePanel('.reference-panel .panel-content', toggleReferenceBtn);
        });
    }
    
    if (togglePronunciationBtn) {
        togglePronunciationBtn.addEventListener('click', function() {
            togglePanel('.pronunciation-panel .panel-content', togglePronunciationBtn);
        });
    }
    
    // Store target language
    if (targetLang) {
        targetLang.addEventListener('change', function() {
            currentTargetLang = this.value;
        });
    }
    
    // Allow Enter key to translate
    idiomInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            translateIdiom();
        }
    });
}

function togglePanel(selector, button) {
    const panel = document.querySelector(selector);
    if (panel) {
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        button.textContent = panel.style.display === 'none' ? '▼' : '▲';
    }
}

function speakText(text, lang = 'en-US') {
    // Cancel any ongoing speech
    synth.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 0.9;
    utterance.pitch = 1;
    
    synth.speak(utterance);
}

function getLangCode(lang) {
    const langMap = {
        'hindi': 'hi-IN',
        'telugu': 'te-IN',
        'tamil': 'ta-IN'
    };
    return langMap[lang] || 'en-US';
}

async function translateIdiom() {
    const idiom = document.getElementById('idiomInput').value;
    const targetLang = document.getElementById('targetLang').value;
    currentTargetLang = targetLang;
    
    if (!idiom.trim()) {
        alert('Please enter an idiom to translate');
        return;
    }
    
    const idiomResult = document.getElementById('idiomResult');
    idiomResult.textContent = 'Translating...';
    
    try {
        const response = await fetch('/api/translate-idiom', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                idiom: idiom,
                target_lang: targetLang
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store current idiom data
            currentIdiomData = data;
            
            // Display result
            idiomResult.classList.remove('placeholder');
            idiomResult.innerHTML = '';
            
            const resultDiv = document.createElement('div');
            resultDiv.innerHTML = `
                <div class="idiom-meaning">
                    <div class="idiom-meaning-title">Original Idiom:</div>
                    <div class="idiom-meaning-text">"${data.original}"</div>
                </div>
                <div class="idiom-meaning">
                    <div class="idiom-meaning-title">English Meaning:</div>
                    <div class="idiom-meaning-text">${data.meaning}</div>
                </div>
                <div class="idiom-meaning">
                    <div class="idiom-meaning-title">Translation in ${targetLang.charAt(0).toUpperCase() + targetLang.slice(1)}:</div>
                    <div class="idiom-meaning-text">${data.translation || 'N/A'}</div>
                </div>
            `;
            
            idiomResult.appendChild(resultDiv);
            
            // Display confidence
            const confidenceScore = document.getElementById('confidenceScore');
            confidenceScore.textContent = `${Math.round(data.confidence * 100)}%`;
            
            // Show copy and speak buttons
            document.getElementById('copyBtn').style.display = 'inline-block';
            document.getElementById('speakTranslationBtn').style.display = 'inline-block';
            
            // Display word-by-word breakdown
            displayIdiomWordBreakdown(data);
            
            // Display explanation
            displayIdiomExplanation(data);
            
            // Display example
            displayIdiomExample(data);
            
            // Display quick reference
            displayQuickReference(data, targetLang);
            
            // Display pronunciation
            displayPronunciationGuide(data, targetLang);
        } else {
            idiomResult.classList.add('placeholder');
            idiomResult.textContent = 'Idiom not found in database';
        }
    } catch (error) {
        console.error('Error:', error);
        idiomResult.classList.add('placeholder');
        idiomResult.textContent = 'Error during translation';
    }
}

function displayIdiomWordBreakdown(data) {
    // Create word breakdown display if it doesn't exist
    let wordBreakDisplay = document.getElementById('wordBreakDisplay');
    if (!wordBreakDisplay) {
        wordBreakDisplay = document.createElement('div');
        wordBreakDisplay.id = 'wordBreakDisplay';
        wordBreakDisplay.className = 'panel';
        wordBreakDisplay.innerHTML = '<div class="panel-header">Word-by-Word Breakdown</div><div id="wordBreakContent" class="panel-content"></div>';
        const idiomResult = document.getElementById('idiomResult');
        idiomResult.parentElement.insertBefore(wordBreakDisplay, idiomResult.nextSibling);
    }
    
    const wordBreakContent = document.getElementById('wordBreakContent');
    wordBreakContent.innerHTML = '';
    
    // Get words from idiom
    const words = data.original.split(/\s+/);
    let html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;">';
    
    words.forEach((word, idx) => {
        html += `<div style="padding: 10px; background: #f0f9ff; border: 1px solid #3b82f6; border-radius: 6px;">`;
        html += `<div style="font-weight: 600; color: #1e40af; margin-bottom: 4px;">${word}</div>`;
        html += `<div style="font-size: 0.9em; color: #6b7280;">Word ${idx + 1}</div>`;
        html += '</div>';
    });
    html += '</div>';
    html += `<div style="margin-top: 15px; padding: 10px; background: #f3f4f6; border-radius: 6px; font-size: 0.95em;">`;
    html += `<strong>Full Translation:</strong> ${data.translation || 'N/A'}`;
    html += '</div>';
    
    wordBreakContent.innerHTML = html;
}

function displayIdiomExplanation(data) {
    const explanationContent = document.getElementById('explanationContent');
    explanationContent.classList.remove('placeholder');
    explanationContent.innerHTML = '';
    
    const explanationDiv = document.createElement('div');
    explanationDiv.className = 'explanation-item';
    explanationDiv.innerHTML = `
        <div class="explanation-item-title">📚 What does it mean?</div>
        <div class="explanation-item-detail">
            <strong>Explanation:</strong> ${data.explanation}<br><br>
            <strong>Cultural Note:</strong> ${data.cultural_note || 'This idiom reflects common cultural expressions and communication styles.'}<br><br>
            <strong>Confidence Level:</strong> ${Math.round(data.confidence * 100)}%
        </div>
    `;
    
    explanationContent.appendChild(explanationDiv);
}

function displayIdiomExample(data) {
    const exampleContent = document.getElementById('exampleContent');
    exampleContent.classList.remove('placeholder');
    exampleContent.innerHTML = '';
    
    const exampleDiv = document.createElement('div');
    exampleDiv.className = 'example-item';
    exampleDiv.innerHTML = `
        <div class="example-item-title">📝 How to use it?</div>
        <div class="example-item-detail">
            <strong>Example Sentence:</strong><br>
            <em>"${data.example}"</em><br><br>
            <div style="background: #f0f0f0; padding: 10px; border-radius: 4px; margin-top: 10px;">
                <strong>🎯 Usage Tip:</strong> Use this idiom in casual conversations or when describing situations that match the idiom's meaning.
            </div>
        </div>
    `;
    
    exampleContent.appendChild(exampleDiv);
}

function displayQuickReference(data, targetLang) {
    const referenceContent = document.getElementById('referenceContent');
    referenceContent.classList.remove('placeholder');
    referenceContent.innerHTML = '';
    
    const referenceDiv = document.createElement('div');
    referenceDiv.className = 'reference-item';
    referenceDiv.innerHTML = `
        <div style="background: #e6f2ff; padding: 15px; border-radius: 6px; border-left: 4px solid #1e40af;">
            <div style="margin-bottom: 10px; color: #1e40af;">
                <strong>English:</strong> ${data.original}
                <button class="voice-btn-small" onclick="speakText('${data.original}', 'en-US')">🔊</button>
            </div>
            <div style="margin-bottom: 10px; color: #1e40af;">
                <strong>${targetLang.charAt(0).toUpperCase() + targetLang.slice(1)}:</strong> ${data.translation}
                <button class="voice-btn-small" onclick="speakText('${data.translation}', '${getLangCode(targetLang)}')">🔊</button>
            </div>
            <div style="background: #cce5ff; padding: 10px; border-radius: 4px; margin-top: 10px; border-left: 3px solid #1e40af; color: #1e40af;">
                <strong>Quick Meaning:</strong> ${data.meaning}
            </div>
        </div>
    `;
    
    referenceContent.appendChild(referenceDiv);
}

function displayPronunciationGuide(data, targetLang) {
    const pronunciationContent = document.getElementById('pronunciationContent');
    pronunciationContent.classList.remove('placeholder');
    pronunciationContent.innerHTML = '';
    
    const pronDiv = document.createElement('div');
    pronDiv.innerHTML = `
        <div class="pronunciation-item">
            <div class="pronunciation-item-lang">English Idiom</div>
            <div class="pronunciation-item-text">${data.original}</div>
            <button class="voice-btn-small" onclick="speakText('${data.original}', 'en-US')">🔊 Listen</button>
        </div>
        <div class="pronunciation-item">
            <div class="pronunciation-item-lang">${targetLang.charAt(0).toUpperCase() + targetLang.slice(1)} Translation</div>
            <div class="pronunciation-item-text">${data.translation}</div>
            <button class="voice-btn-small" onclick="speakText('${data.translation}', '${getLangCode(targetLang)}')">🔊 Listen</button>
        </div>
    `;
    
    pronunciationContent.appendChild(pronDiv);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        const copyBtn = document.getElementById('copyBtn');
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        copyBtn.style.background = '#10b981';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Copy failed:', err);
        alert('Failed to copy text');
    });
}
