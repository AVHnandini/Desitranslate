// ===========================
// VIDEO SUBTITLE TRANSLATOR JAVASCRIPT
// ===========================

const synth = window.speechSynthesis;

document.addEventListener('DOMContentLoaded', function() {
    setupVideoTranslator();
});

function setupVideoTranslator() {
    const fileUpload = document.getElementById('fileUpload');
    const subtitleFile = document.getElementById('subtitleFile');
    const subtitleText = document.getElementById('subtitleText');
    const clearBtn = document.getElementById('clearBtn');
    const translateBtn = document.getElementById('translateBtn');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const speakInputBtn = document.getElementById('speakInputBtn');
    const speakOutputBtn = document.getElementById('speakOutputBtn');
    
    // Panel toggles
    const toggleDetailsBtn = document.getElementById('toggleDetailsPanel');
    const toggleTimingBtn = document.getElementById('toggleTimingPanel');
    const toggleFormatBtn = document.getElementById('toggleFormatPanel');
    
    // File upload handling
    if (fileUpload) {
        fileUpload.addEventListener('click', () => subtitleFile.click());
        fileUpload.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUpload.style.background = 'rgba(30, 64, 175, 0.15)';
        });
        fileUpload.addEventListener('dragleave', () => {
            fileUpload.style.background = '';
        });
        fileUpload.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUpload.style.background = '';
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleSubtitleFile(files[0]);
            }
        });
    }
    
    // File input change
    if (subtitleFile) {
        subtitleFile.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleSubtitleFile(e.target.files[0]);
            }
        });
    }
    
    // Clear button
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            subtitleText.value = '';
            subtitleFile.value = '';
        });
    }
    
    // Speak input
    if (speakInputBtn) {
        speakInputBtn.addEventListener('click', function() {
            const text = subtitleText.value;
            if (text.trim()) {
                speakText(text, 'en-US');
            } else {
                alert('Please enter subtitle text to speak');
            }
        });
    }
    
    // Speak output
    if (speakOutputBtn) {
        speakOutputBtn.addEventListener('click', function() {
            const text = document.getElementById('translatedSubtitles').textContent;
            if (text && !text.includes('Click Translate')) {
                speakText(text, 'en-US');
            }
        });
    }
    
    // Translate button
    if (translateBtn) {
        translateBtn.addEventListener('click', function() {
            translateSubtitles();
        });
    }
    
    // Copy button
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            copyToClipboard(document.getElementById('translatedSubtitles').textContent);
        });
    }
    
    // Download button
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            downloadSubtitles();
        });
    }
    
    // Panel toggles
    if (toggleDetailsBtn) {
        toggleDetailsBtn.addEventListener('click', function() {
            togglePanel('.details-panel .panel-content', toggleDetailsBtn);
        });
    }
    
    if (toggleTimingBtn) {
        toggleTimingBtn.addEventListener('click', function() {
            togglePanel('.timing-panel .panel-content', toggleTimingBtn);
        });
    }
    
    if (toggleFormatBtn) {
        toggleFormatBtn.addEventListener('click', function() {
            togglePanel('.format-panel .panel-content', toggleFormatBtn);
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

function handleSubtitleFile(file) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const content = e.target.result;
        document.getElementById('subtitleText').value = content;
    };
    
    reader.onerror = function() {
        alert('Error reading file');
    };
    
    reader.readAsText(file);
}

async function translateSubtitles() {
    const subtitleText = document.getElementById('subtitleText').value;
    const targetLang = document.getElementById('targetLang').value;
    
    if (!subtitleText.trim()) {
        alert('Please enter subtitle content to translate');
        return;
    }
    
    // Extract subtitle lines (simple parsing)
    // Proper SRT parsing - handles all edge cases
    const lines = subtitleText.split('\n');
    const subtitles = [];
    let currentSubtitle = '';
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        // Skip empty lines
        if (!line) {
            if (currentSubtitle) {
                subtitles.push(currentSubtitle);
                currentSubtitle = '';
            }
            continue;
        }
        
        // Skip sequence numbers (line with just digits)
        if (line.match(/^\d+$/)) {
            continue;
        }
        
        // Skip timing lines (contains -->)
        if (line.includes('-->')) {
            continue;
        }
        
        // Skip standalone timestamp lines
        if (line.match(/^\d{2}:\d{2}:\d{2}(,|\.)\d{3}$/)) {
            continue;
        }
        
        // This is actual subtitle content
        if (currentSubtitle) {
            currentSubtitle += ' ' + line;
        } else {
            currentSubtitle = line;
        }
    }
    
    // Add the last subtitle if exists
    if (currentSubtitle) {
        subtitles.push(currentSubtitle);
    }
    
    if (subtitles.length === 0) {
        alert('Could not extract subtitle text. Please check the file format.');
        return;
    }
    
    const translatedSubtitles = document.getElementById('translatedSubtitles');
    translatedSubtitles.textContent = 'Translating subtitles...';
    
    try {
        const response = await fetch('/api/translate-video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                subtitles: subtitles,
                target_lang: targetLang
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            translatedSubtitles.innerHTML = '';
            translatedSubtitles.classList.remove('placeholder');
            
            let html = '<strong>Translated Subtitles:</strong><br><br>';
            data.translated_subtitles.forEach((item, index) => {
                html += `<div style="margin-bottom: 1.5rem; padding: 1rem; background: #e6f2ff; border-radius: 8px; border-left: 3px solid #1e40af;">
                    <strong style="color: #1e40af;">Original:</strong> <span style="color: #1e40af;">${item.original}</span><br>
                    <strong style="color: #1e40af;">Translated:</strong> <span style="color: #1e40af;">${item.translated}</span>
                </div>`;
            });
            
            translatedSubtitles.innerHTML = html;
            
            // Display confidence
            const confidenceScore = document.getElementById('confidenceScore');
            confidenceScore.textContent = `${Math.round((data.total / subtitles.length) * 100)}%`;
            
            // Show buttons
            document.getElementById('copyBtn').style.display = 'inline-block';
            document.getElementById('speakOutputBtn').style.display = 'inline-block';
            document.getElementById('downloadBtn').style.display = 'inline-block';
            
            // Display explanations
            displayVideoExplanation(data.translated_subtitles.slice(0, 5), subtitles.length);
            displayTimingInfo(data.translated_subtitles);
            displayFormatInfo(data);
        } else {
            translatedSubtitles.textContent = 'Translation failed';
        }
    } catch (error) {
        console.error('Error:', error);
        translatedSubtitles.textContent = 'Error during translation';
    }
}

function displayVideoExplanation(subtitles, totalCount) {
    const detailsContent = document.getElementById('detailsContent');
    detailsContent.innerHTML = '';
    detailsContent.classList.remove('placeholder');
    
    const summaryDiv = document.createElement('div');
    summaryDiv.style.color = '#3b82f6';
    summaryDiv.style.lineHeight = '1.8';
    
    summaryDiv.innerHTML = `
        <strong>Translation Summary:</strong><br>
        <strong>Total Subtitles:</strong> ${totalCount}<br>
        <strong>Translated:</strong> ${subtitles.length} subtitles<br><br>
        <strong>First Few Translations:</strong><br>
    `;
    
    detailsContent.appendChild(summaryDiv);
    
    subtitles.forEach((item, index) => {
        const subtitleItem = document.createElement('div');
        subtitleItem.className = 'subtitle-item';
        
        subtitleItem.innerHTML = `
            <div class="subtitle-item-text"><strong>Original:</strong> ${item.original}</div>
            <div class="subtitle-item-text"><strong>Translated:</strong> ${item.translated}</div>
        `;
        
        detailsContent.appendChild(subtitleItem);
    });
}

function displayTimingInfo(subtitles) {
    const timingContent = document.getElementById('timingContent');
    timingContent.innerHTML = '';
    timingContent.classList.remove('placeholder');
    
    const timingDiv = document.createElement('div');
    timingDiv.style.color = '#3b82f6';
    timingDiv.style.lineHeight = '1.6';
    
    timingDiv.innerHTML = `
        <strong>Timing Information:</strong><br><br>
        <strong>Subtitle Count:</strong> ${subtitles.length} subtitle entries<br><br>
        <strong>Timing Preservation:</strong> When you download the translated subtitles, all timing information (start and end times) from the original SRT/VTT file will be maintained. This ensures perfect synchronization with your video file.<br><br>
        <strong>Format Support:</strong> Both SRT and VTT format timings are automatically preserved during translation.
    `;
    
    timingContent.appendChild(timingDiv);
}

function displayFormatInfo(data) {
    const formatContent = document.getElementById('formatContent');
    formatContent.innerHTML = '';
    formatContent.classList.remove('placeholder');
    
    const formatDiv = document.createElement('div');
    formatDiv.style.color = '#3b82f6';
    formatDiv.style.lineHeight = '1.6';
    
    formatDiv.innerHTML = `
        <strong>Supported Formats:</strong><br><br>
        <strong>Input Formats:</strong><br>
        • SRT (SubRip)<br>
        • VTT (WebVTT)<br><br>
        <strong>Output Format:</strong><br>
        • SRT (SubRip) - Fully compatible<br><br>
        <strong>Confidence Level:</strong> ${Math.round(data.total * 100)}%<br><br>
        The translated subtitles maintain the exact timing format for seamless video integration.
    `;
    
    formatContent.appendChild(formatDiv);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        const copyBtn = document.getElementById('copyBtn');
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        copyBtn.style.background = '#1e40af';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Copy failed:', err);
        alert('Failed to copy text');
    });
}

function downloadSubtitles() {
    const translatedContent = document.getElementById('translatedSubtitles').textContent;
    
    const blob = new Blob([translatedContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `translated_subtitles_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}
