// ===========================
// TEXT TRANSLATOR JAVASCRIPT
// ===========================

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const speechRecognition = SpeechRecognition ? new SpeechRecognition() : null;

document.addEventListener('DOMContentLoaded', function() {
    setupTranslator();
});

function setupTranslator() {
    const sourceText = document.getElementById('sourceText');
    const targetLang = document.getElementById('targetLang');
    const charCount = document.querySelector('.char-count');
    const voiceBtn = document.getElementById('voiceBtn');
    const clearBtn = document.getElementById('clearBtn');
    const translateBtn = document.getElementById('translateBtn');
    const speakBtn = document.getElementById('speakBtn');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const togglePanelBtn = document.getElementById('togglePanel');
    
    // Character counter
    if (sourceText) {
        sourceText.addEventListener('input', function() {
            charCount.textContent = `${this.value.length}/500`;
        });
    }
    
    // Voice input
    if (voiceBtn && speechRecognition) {
        voiceBtn.addEventListener('click', function() {
            startVoiceInput();
        });
    } else if (voiceBtn && !speechRecognition) {
        voiceBtn.disabled = true;
        voiceBtn.title = 'Speech Recognition not supported';
    }
    
    // Clear button
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            sourceText.value = '';
            charCount.textContent = '0/500';
            sourceText.focus();
        });
    }
    
    // Translate button
    if (translateBtn) {
        translateBtn.addEventListener('click', function() {
            translateText();
        });
    }
    
    // Speak button
    if (speakBtn) {
        speakBtn.addEventListener('click', function() {
            speakTranslation();
        });
    }
    
    // Copy button
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            copyToClipboard(document.getElementById('translatedText').textContent);
        });
    }
    
    // Download button
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            downloadTranslation();
        });
    }
    
    // Toggle explanation panel
    if (togglePanelBtn) {
        togglePanelBtn.addEventListener('click', function() {
            const panelContent = document.querySelector('.panel-content');
            panelContent.style.display = panelContent.style.display === 'none' ? 'block' : 'none';
            togglePanelBtn.textContent = panelContent.style.display === 'none' ? '▼' : '▲';
        });
    }
}

function startVoiceInput() {
    const voiceStatus = document.getElementById('voiceStatus');
    
    if (!speechRecognition) {
        alert('Speech Recognition not supported in your browser');
        return;
    }
    
    speechRecognition.lang = 'en-US';
    speechRecognition.start();
    
    voiceStatus.style.display = 'block';
    document.getElementById('voiceBtn').disabled = true;
    
    speechRecognition.onresult = function(event) {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        
        const sourceText = document.getElementById('sourceText');
        sourceText.value = transcript;
        sourceText.dispatchEvent(new Event('input'));
        
        voiceStatus.style.display = 'none';
        document.getElementById('voiceBtn').disabled = false;
    };
    
    speechRecognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        voiceStatus.style.display = 'none';
        document.getElementById('voiceBtn').disabled = false;
    };
}

async function translateText() {
    const sourceText = document.getElementById('sourceText').value;
    const sourceLang = document.getElementById('sourceLang').value;
    const targetLang = document.getElementById('targetLang').value;
    
    if (!sourceText.trim()) {
        alert('Please enter text to translate');
        return;
    }
    
    const translatedTextDiv = document.getElementById('translatedText');
    translatedTextDiv.textContent = 'Translating...';
    
    try {
        // Call the detailed translation API
        const response = await fetch('/api/translate-detailed', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: sourceText,
                source_lang: sourceLang,
                target_lang: targetLang
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Display translated text
            translatedTextDiv.textContent = data.translated_text;
            translatedTextDiv.classList.remove('placeholder');
            
            // Display confidence
            const confidenceScore = document.getElementById('confidenceScore');
            confidenceScore.textContent = `${data.confidence}%`;
            
            // Show copy and speak buttons
            document.getElementById('copyBtn').style.display = 'inline-block';
            document.getElementById('speakBtn').style.display = 'inline-block';
            document.getElementById('downloadBtn').style.display = 'inline-block';
            
            // Display word-to-word mapping
            displayWordMapping(data);
            
            // Display detailed explanation with word table
            displayDetailedExplanation(data);
        } else {
            translatedTextDiv.textContent = 'Translation failed';
        }
    } catch (error) {
        console.error('Error:', error);
        translatedTextDiv.textContent = 'Error during translation';
    }
}

function displayWordMapping(data) {
    // This function is optional - check if elements exist before using them
    const wordMappingDisplay = document.getElementById('wordMappingDisplay');
    const wordMappingContent = document.getElementById('wordMappingContent');
    
    // If these elements don't exist, skip this function
    if (!wordMappingDisplay || !wordMappingContent) {
        return;
    }
    
    if (data.word_mappings && data.word_mappings.length > 0) {
        wordMappingContent.innerHTML = '';
        
        const row = document.createElement('div');
        row.className = 'word-mapping-row';
        
        data.word_mappings.forEach((mapping, index) => {
            const sourceItem = document.createElement('div');
            sourceItem.className = 'word-mapping-item';
            sourceItem.innerHTML = `
                <div class="source-word">${mapping.source_word}</div>
                <div class="pos-tag">${mapping.source_pos}</div>
            `;
            row.appendChild(sourceItem);
            
            // Add arrow
            if (index < data.word_mappings.length - 1) {
                const arrow = document.createElement('div');
                arrow.className = 'word-mapping-arrow';
                arrow.textContent = '→';
                row.appendChild(arrow);
            }
        });
        
        // Add target words row
        const targetRow = document.createElement('div');
        targetRow.className = 'word-mapping-row';
        targetRow.style.marginTop = '20px';
        
        data.word_mappings.forEach((mapping, index) => {
            const targetItem = document.createElement('div');
            targetItem.className = 'word-mapping-item';
            const confLevel = mapping.confidence >= 0.8 ? 'high' : mapping.confidence >= 0.5 ? 'medium' : 'low';
            targetItem.innerHTML = `
                <div class="target-word">${mapping.target_word}</div>
                <div class="pos-tag">${mapping.target_pos}</div>
                <div class="confidence-indicator" style="color: ${confLevel === 'high' ? '#27ae60' : confLevel === 'medium' ? '#f39c12' : '#e74c3c'};">
                    ${Math.round(mapping.confidence * 100)}% confidence
                </div>
            `;
            targetRow.appendChild(targetItem);
            
            // Add arrow
            if (index < data.word_mappings.length - 1) {
                const arrow = document.createElement('div');
                arrow.className = 'word-mapping-arrow';
                arrow.textContent = '↓';
                arrow.style.color = '#95a5a6';
                targetRow.appendChild(arrow);
            }
        });
        
        wordMappingContent.appendChild(row);
        wordMappingContent.appendChild(targetRow);
        wordMappingDisplay.style.display = 'block';
    } else {
        wordMappingDisplay.style.display = 'none';
    }
}

function displayDetailedExplanation(data) {
    // Display linguistic explanation
    const linguisticDiv = document.getElementById('linguisticExplanation');
    const linguisticText = document.getElementById('linguisticText');
    
    if (linguisticDiv && linguisticText && data.linguistic_explanation) {
        linguisticText.textContent = data.linguistic_explanation;
        linguisticDiv.style.display = 'block';
    } else if (linguisticDiv) {
        linguisticDiv.style.display = 'none';
    }
    
    // Display word explanation table
    const tableContainer = document.getElementById('wordExplanationContainer');
    const tableBody = document.getElementById('tableBody');
    
    if (tableContainer && tableBody && data.word_explanations && data.word_explanations.length > 0) {
        tableBody.innerHTML = '';
        
        data.word_explanations.forEach((wordData, index) => {
            const row = document.createElement('tr');
            row.style.animationDelay = `${index * 50}ms`;
            
            // Determine confidence level
            const confLevel = wordData.confidence >= 0.8 ? 'high' : wordData.confidence >= 0.5 ? 'medium' : 'low';
            
            row.innerHTML = `
                <td><strong>${wordData.original_word}</strong></td>
                <td><span class="pos-tag ${wordData.source_pos.toLowerCase()}">${wordData.source_pos}</span></td>
                <td>${wordData.source_meaning || 'N/A'}</td>
                <td><strong>${wordData.translated_word}</strong></td>
                <td><span class="pos-tag ${wordData.target_pos.toLowerCase()}">${wordData.target_pos}</span></td>
                <td>${wordData.rule}</td>
                <td>
                    <div class="confidence-indicator confidence-${confLevel}">
                        <span class="confidence-bar ${confLevel}"></span>
                        ${Math.round(wordData.confidence * 100)}%
                    </div>
                </td>
            `;
            
            tableBody.appendChild(row);
        });
        
        tableContainer.style.display = 'block';
    } else if (tableContainer) {
        tableContainer.style.display = 'none';
    }
}

function displayExplanation(explanations) {
    const explanationContent = document.getElementById('explanationContent');
    explanationContent.innerHTML = '';
    explanationContent.classList.remove('placeholder');
    
    explanations.forEach(item => {
        const explanationItem = document.createElement('div');
        explanationItem.className = 'explanation-item';
        
        const confidenceColor = item.confidence > 0.8 ? '#10b981' : item.confidence > 0.5 ? '#f59e0b' : '#ef4444';
        
        explanationItem.innerHTML = `
            <div class="explanation-item-title">
                "${item.original}" → "${item.translated}"
                <span style="color: ${confidenceColor}; font-size: 0.8rem; margin-left: 0.5rem;">
                    (${Math.round(item.confidence * 100)}%)
                </span>
            </div>
            <div class="explanation-item-detail">
                <strong>Part of Speech:</strong> ${item.pos.toUpperCase()}<br>
                <strong>Rule:</strong> ${item.rule}
            </div>
        `;
        
        explanationContent.appendChild(explanationItem);
    });
}

function speakTranslation() {
    const translatedText = document.getElementById('translatedText').textContent;
    const targetLang = document.getElementById('targetLang').value;
    
    if (!translatedText || translatedText === 'Translation failed') {
        alert('No translation to speak');
        return;
    }
    
    const utterance = new SpeechSynthesisUtterance(translatedText);
    
    // Set language
    switch(targetLang) {
        case 'hindi':
            utterance.lang = 'hi-IN';
            break;
        case 'spanish':
            utterance.lang = 'es-ES';
            break;
        case 'french':
            utterance.lang = 'fr-FR';
            break;
        default:
            utterance.lang = 'en-US';
    }
    
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;
    
    speechSynthesis.cancel();
    speechSynthesis.speak(utterance);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show success feedback
        const copyBtn = document.getElementById('copyBtn');
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
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

function downloadTranslation() {
    const sourceText = document.getElementById('sourceText').value;
    const translatedText = document.getElementById('translatedText').textContent;
    const targetLang = document.getElementById('targetLang').value;
    
    const content = `SOURCE TEXT (ENGLISH):\n${sourceText}\n\nTRANSLATED TEXT (${targetLang.toUpperCase()}):\n${translatedText}`;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `translation_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// Allow Enter key to translate
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && e.ctrlKey) {
        translateText();
    }
});
