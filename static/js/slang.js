// ===========================
// SLANG NORMALIZER JAVASCRIPT
// ===========================

const synth = window.speechSynthesis;

document.addEventListener('DOMContentLoaded', function() {
    setupSlangNormalizer();
});

function setupSlangNormalizer() {
    const slangText = document.getElementById('slangText');
    const charCount = document.querySelector('.char-count');
    const clearBtn = document.getElementById('clearBtn');
    const normalizeBtn = document.getElementById('normalizeBtn');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const speakInputBtn = document.getElementById('speakInputBtn');
    const speakOutputBtn = document.getElementById('speakOutputBtn');
    
    // Panel toggles
    const toggleSlangBtn = document.getElementById('toggleSlangPanel');
    const toggleAbbrevBtn = document.getElementById('toggleAbbreviationPanel');
    const toggleLangBtn = document.getElementById('toggleLanguagePanel');
    
    // Character counter
    if (slangText) {
        slangText.addEventListener('input', function() {
            charCount.textContent = `${this.value.length}/500`;
        });
    }
    
    // Clear button
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            slangText.value = '';
            charCount.textContent = '0/500';
            slangText.focus();
        });
    }
    
    // Speak input
    if (speakInputBtn) {
        speakInputBtn.addEventListener('click', function() {
            const text = slangText.value;
            if (text.trim()) {
                speakText(text, 'en-US');
            } else {
                alert('Please enter text to speak');
            }
        });
    }
    
    // Speak output
    if (speakOutputBtn) {
        speakOutputBtn.addEventListener('click', function() {
            const text = document.getElementById('normalizedText').textContent;
            if (text && !text.includes('Click Normalize')) {
                speakText(text, 'en-US');
            }
        });
    }
    
    // Normalize button
    if (normalizeBtn) {
        normalizeBtn.addEventListener('click', function() {
            normalizeSlang();
        });
    }
    
    // Copy button
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            copyToClipboard(document.getElementById('normalizedText').textContent);
        });
    }
    
    // Download button
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            downloadNormalized();
        });
    }
    
    // Panel toggles
    if (toggleSlangBtn) {
        toggleSlangBtn.addEventListener('click', function() {
            togglePanel('.slang-panel .panel-content', toggleSlangBtn);
        });
    }
    
    if (toggleAbbrevBtn) {
        toggleAbbrevBtn.addEventListener('click', function() {
            togglePanel('.abbreviation-panel .panel-content', toggleAbbrevBtn);
        });
    }
    
    if (toggleLangBtn) {
        toggleLangBtn.addEventListener('click', function() {
            togglePanel('.language-panel .panel-content', toggleLangBtn);
        });
    }
}

function togglePanel(selector, button) {
    const panel = document.querySelector(selector);
    if (panel) {
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        button.textContent = panel.style.display === 'none' ? '▼' : '▲';
    }
}

function speakText(text, lang = 'en-US') {
    synth.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 0.9;
    synth.speak(utterance);
}

async function normalizeSlang() {
    const text = document.getElementById('slangText').value;
    
    if (!text.trim()) {
        alert('Please enter text to normalize');
        return;
    }
    
    const normalizedText = document.getElementById('normalizedText');
    normalizedText.textContent = 'Normalizing...';
    
    try {
        const response = await fetch('/api/normalize-slang', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            normalizedText.textContent = data.normalized_text;
            normalizedText.classList.remove('placeholder');
            
            // Display confidence
            const confidenceScore = document.getElementById('confidenceScore');
            confidenceScore.textContent = `${Math.round(data.confidence * 100)}%`;
            
            // Show buttons
            document.getElementById('copyBtn').style.display = 'inline-block';
            document.getElementById('speakOutputBtn').style.display = 'inline-block';
            document.getElementById('downloadBtn').style.display = 'inline-block';
            
            // Display word-to-word mappings
            displaySlangWordMappings(data.explanations);
            
            // Display explanations
            displaySlangExplanation(data.explanations);
            displayAbbreviations(data.explanations);
            displayLanguageInfo(data);
        } else {
            normalizedText.textContent = 'Normalization failed';
        }
    } catch (error) {
        console.error('Error:', error);
        normalizedText.textContent = 'Error during normalization';
    }
}

function displaySlangWordMappings(explanations) {
    // Create word mapping display if it doesn't exist
    let wordMappingDisplay = document.getElementById('wordMappingDisplay');
    if (!wordMappingDisplay) {
        wordMappingDisplay = document.createElement('div');
        wordMappingDisplay.id = 'wordMappingDisplay';
        wordMappingDisplay.className = 'panel';
        wordMappingDisplay.innerHTML = '<div class="panel-header">Word-by-Word Mapping</div><div id="wordMappingContent" class="panel-content"></div>';
        const normalizedText = document.getElementById('normalizedText');
        normalizedText.parentElement.insertBefore(wordMappingDisplay, normalizedText.nextSibling);
    }
    
    const wordMappingContent = document.getElementById('wordMappingContent');
    wordMappingContent.innerHTML = '';
    
    if (explanations && explanations.length > 0) {
        let html = '<table style="width: 100%; border-collapse: collapse;">';
        html += '<tr style="background: #e0e7ff; border-bottom: 2px solid #3b82f6;"><th style="padding: 8px; text-align: left;">Slang</th><th style="padding: 8px; text-align: left;">Normalized</th><th style="padding: 8px; text-align: left;">Category</th></tr>';
        
        explanations.forEach((item, idx) => {
            const bgColor = idx % 2 === 0 ? '#f9fafb' : '#ffffff';
            html += `<tr style="background: ${bgColor}; border-bottom: 1px solid #e5e7eb;">`;
            html += `<td style="padding: 8px;"><strong>${item.original}</strong></td>`;
            html += `<td style="padding: 8px;">${item.normalized}</td>`;
            html += `<td style="padding: 8px; font-size: 0.85em; color: #6b7280;">${item.explanation.substring(0, 40)}...</td>`;
            html += '</tr>';
        });
        html += '</table>';
        wordMappingContent.innerHTML = html;
    }
}

function displaySlangExplanation(explanations) {
    const slangContent = document.getElementById('slangContent');
    slangContent.innerHTML = '';
    slangContent.classList.remove('placeholder');
    
    explanations.slice(0, 5).forEach(item => {
        const slangItem = document.createElement('div');
        slangItem.className = 'slang-item';
        
        slangItem.innerHTML = `
            <div class="slang-item-original">"${item.original}" → "${item.normalized}"</div>
            <div class="slang-item-meaning">${item.explanation}</div>
        `;
        
        slangContent.appendChild(slangItem);
    });
}

function displayAbbreviations(explanations) {
    const abbrevContent = document.getElementById('abbreviationContent');
    abbrevContent.innerHTML = '';
    abbrevContent.classList.remove('placeholder');
    
    const abbrevDiv = document.createElement('div');
    abbrevDiv.style.color = '#3b82f6';
    abbrevDiv.style.lineHeight = '1.8';
    
    let abbrevText = '<strong>Common Abbreviations Found:</strong><br>';
    const uniqueItems = new Map();
    
    explanations.forEach(item => {
        if (!uniqueItems.has(item.original)) {
            uniqueItems.set(item.original, item);
        }
    });
    
    uniqueItems.forEach((item, key) => {
        abbrevText += `<strong>${key}</strong> = ${item.normalized}<br>`;
    });
    
    abbrevDiv.innerHTML = abbrevText || 'Common abbreviations will appear here';
    abbrevContent.appendChild(abbrevDiv);
}

function displayLanguageInfo(data) {
    const languageContent = document.getElementById('languageContent');
    languageContent.innerHTML = '';
    languageContent.classList.remove('placeholder');
    
    const langDiv = document.createElement('div');
    langDiv.style.color = '#3b82f6';
    langDiv.style.lineHeight = '1.6';
    
    langDiv.innerHTML = `
        <strong>Internet Language Analysis:</strong><br><br>
        <strong>Confidence Level:</strong> ${Math.round(data.confidence * 100)}%<br><br>
        <strong>About Modern Slang:</strong> Internet slang and text abbreviations have become an integral part of digital communication. This tool helps convert casual online language into formal, standardized English suitable for professional and academic contexts. Understanding both forms is essential in today's multilingual communication landscape.
    `;
    
    languageContent.appendChild(langDiv);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        const copyBtn = document.getElementById('copyBtn');
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        copyBtn.style.background = '#60a5fa';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Copy failed:', err);
        alert('Failed to copy text');
    });
}

function downloadNormalized() {
    const sourceText = document.getElementById('slangText').value;
    const normalizedText = document.getElementById('normalizedText').textContent;
    
    const content = `ORIGINAL SLANG TEXT:\n${sourceText}\n\nNORMALIZED TEXT:\n${normalizedText}`;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `normalized_text_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}
