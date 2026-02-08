// ===========================
// HISTORICAL TRANSLATOR JAVASCRIPT
// ===========================

const synth = window.speechSynthesis;

document.addEventListener('DOMContentLoaded', function() {
    setupHistoricalTranslator();
});

function setupHistoricalTranslator() {
    const historicalText = document.getElementById('historicalText');
    const charCount = document.querySelector('.char-count');
    const clearBtn = document.getElementById('clearBtn');
    const translateBtn = document.getElementById('translateBtn');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const speakInputBtn = document.getElementById('speakInputBtn');
    const speakOutputBtn = document.getElementById('speakOutputBtn');
    
    // Panel toggles
    const toggleExplanationBtn = document.getElementById('toggleExplanationPanel');
    const toggleEtymologyBtn = document.getElementById('toggleEtymologyPanel');
    const toggleContextBtn = document.getElementById('toggleContextPanel');
    
    // Character counter
    if (historicalText) {
        historicalText.addEventListener('input', function() {
            charCount.textContent = `${this.value.length}/500`;
        });
    }
    
    // Clear button
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            historicalText.value = '';
            charCount.textContent = '0/500';
            historicalText.focus();
        });
    }
    
    // Speak input
    if (speakInputBtn) {
        speakInputBtn.addEventListener('click', function() {
            const text = historicalText.value;
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
            const text = document.getElementById('modernText').textContent;
            if (text && !text.includes('Click Translate')) {
                speakText(text, 'en-US');
            }
        });
    }
    
    // Translate button
    if (translateBtn) {
        translateBtn.addEventListener('click', function() {
            translateHistorical();
        });
    }
    
    // Copy button
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            copyToClipboard(document.getElementById('modernText').textContent);
        });
    }
    
    // Download button
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            downloadHistorical();
        });
    }
    
    // Panel toggles
    if (toggleExplanationBtn) {
        toggleExplanationBtn.addEventListener('click', function() {
            togglePanel('.explanation-panel .panel-content', toggleExplanationBtn);
        });
    }
    
    if (toggleEtymologyBtn) {
        toggleEtymologyBtn.addEventListener('click', function() {
            togglePanel('.etymology-panel .panel-content', toggleEtymologyBtn);
        });
    }
    
    if (toggleContextBtn) {
        toggleContextBtn.addEventListener('click', function() {
            togglePanel('.context-panel .panel-content', toggleContextBtn);
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

async function translateHistorical() {
    const text = document.getElementById('historicalText').value;
    
    if (!text.trim()) {
        alert('Please enter historical text to translate');
        return;
    }
    
    const modernText = document.getElementById('modernText');
    modernText.textContent = 'Translating...';
    
    try {
        const response = await fetch('/api/translate-historical', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            modernText.textContent = data.modern_text;
            modernText.classList.remove('placeholder');
            
            // Display confidence
            const confidenceScore = document.getElementById('confidenceScore');
            confidenceScore.textContent = `${Math.round(data.confidence * 100)}%`;
            
            // Show buttons
            document.getElementById('copyBtn').style.display = 'inline-block';
            document.getElementById('speakOutputBtn').style.display = 'inline-block';
            document.getElementById('downloadBtn').style.display = 'inline-block';
            
            // Display word-to-word mappings
            displayHistoricalWordMappings(data.explanations);
            
            // Display explanations
            displayHistoricalExplanation(data.explanations);
            displayEtymology(data.explanations);
            displayContext(data);
        } else {
            modernText.textContent = 'Translation failed';
        }
    } catch (error) {
        console.error('Error:', error);
        modernText.textContent = 'Error during translation';
    }
}

function displayHistoricalWordMappings(explanations) {
    // Create word mapping display if it doesn't exist
    let wordMappingDisplay = document.getElementById('wordMappingDisplay');
    if (!wordMappingDisplay) {
        wordMappingDisplay = document.createElement('div');
        wordMappingDisplay.id = 'wordMappingDisplay';
        wordMappingDisplay.className = 'panel';
        wordMappingDisplay.innerHTML = '<div class="panel-header">Word-by-Word Translation</div><div id="wordMappingContent" class="panel-content"></div>';
        const modernText = document.getElementById('modernText');
        modernText.parentElement.insertBefore(wordMappingDisplay, modernText.nextSibling);
    }
    
    const wordMappingContent = document.getElementById('wordMappingContent');
    wordMappingContent.innerHTML = '';
    
    if (explanations && explanations.length > 0) {
        let html = '<table style="width: 100%; border-collapse: collapse;">';
        html += '<tr style="background: #e0e7ff; border-bottom: 2px solid #3b82f6;"><th style="padding: 8px; text-align: left;">Historical</th><th style="padding: 8px; text-align: left;">Modern</th><th style="padding: 8px; text-align: left;">Era</th></tr>';
        
        explanations.forEach((item, idx) => {
            const bgColor = idx % 2 === 0 ? '#f9fafb' : '#ffffff';
            html += `<tr style="background: ${bgColor}; border-bottom: 1px solid #e5e7eb;">`;
            html += `<td style="padding: 8px;"><strong>${item.original}</strong></td>`;
            html += `<td style="padding: 8px;">${item.modern}</td>`;
            html += `<td style="padding: 8px; font-size: 0.85em; color: #6b7280;">${item.era || 'Unknown'}</td>`;
            html += '</tr>';
        });
        html += '</table>';
        wordMappingContent.innerHTML = html;
    }
}

function displayHistoricalExplanation(explanations) {
    const explanationContent = document.getElementById('explanationContent');
    explanationContent.innerHTML = '';
    explanationContent.classList.remove('placeholder');
    
    explanations.forEach(item => {
        const explanationItem = document.createElement('div');
        explanationItem.className = 'historical-item';
        
        explanationItem.innerHTML = `
            <div style="font-weight: 600; color: #1e40af; margin-bottom: 5px;">
                "${item.original}" → "${item.modern}"
            </div>
            <div style="color: #3b82f6; margin-bottom: 5px;">
                <strong>Era:</strong> ${item.era}
            </div>
            <div style="color: #3b82f6;">
                <strong>Explanation:</strong> ${item.explanation}
            </div>
        `;
        
        explanationContent.appendChild(explanationItem);
    });
}

function displayEtymology(explanations) {
    const etymologyContent = document.getElementById('etymologyContent');
    etymologyContent.innerHTML = '';
    etymologyContent.classList.remove('placeholder');
    
    const summaryDiv = document.createElement('div');
    summaryDiv.className = 'historical-item';
    summaryDiv.innerHTML = `
        <div style="color: #3b82f6; line-height: 1.6;">
            <strong>Etymology Analysis:</strong><br>
            This text contains words and phrases from different historical periods. Each word has evolved over centuries with changes in pronunciation, meaning, and usage. The explanations above show how these historical terms map to their modern equivalents, preserving the original intent while making the text accessible to contemporary readers.
        </div>
    `;
    etymologyContent.appendChild(summaryDiv);
}

function displayContext(data) {
    const contextContent = document.getElementById('contextContent');
    contextContent.innerHTML = '';
    contextContent.classList.remove('placeholder');
    
    const contextDiv = document.createElement('div');
    contextDiv.className = 'historical-item';
    contextDiv.innerHTML = `
        <div style="color: #3b82f6; line-height: 1.6;">
            <strong>Historical Context:</strong><br>
            <strong>Confidence Level:</strong> ${Math.round(data.confidence * 100)}%<br><br>
            This text has been translated from historical English to modern English. The translation maintains the original meaning while converting archaic vocabulary and grammar patterns to contemporary usage. Perfect for understanding historical documents, literature, and correspondence.
        </div>
    `;
    contextContent.appendChild(contextDiv);
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

function downloadHistorical() {
    const sourceText = document.getElementById('historicalText').value;
    const modernText = document.getElementById('modernText').textContent;
    
    const content = `HISTORICAL/OLD ENGLISH TEXT:\n${sourceText}\n\nMODERN ENGLISH TEXT:\n${modernText}`;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `historical_translation_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}
