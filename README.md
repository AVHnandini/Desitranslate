# 🌍 Desi Translate - Professional Language Translation Platform

A full-stack web application for translating text, voice, idioms, slang, historical documents, and video subtitles with detailed grammar and rule-based explanations.

## ✨ Features

### 1. **Text/Voice Translator**
- Translate text from English to Hindi, Spanish, French
- Voice input using Web Speech API
- Voice output with speech synthesis
- Step-by-step grammar explanations
- Confidence score for each translation
- Copy and download functionality

### 2. **Idiom & Proverb Translator**
- Convert English idioms to target languages
- Cultural meanings and explanations
- Origin and example usage information
- Support for multiple languages

### 3. **Chat/SMS Slang Normalizer**
- Transform internet slang to proper English
- Support for 30+ common abbreviations (ur, u, omg, etc.)
- Detailed explanation for each conversion
- Professional writing assistance

### 4. **Historical/Colonial Document Translator**
- Convert Old English to modern English
- Etymological and linguistic information
- Support for Middle English terms
- Era-based categorization

### 5. **Video Subtitle Translator**
- Upload subtitle files (SRT, VTT formats)
- Drag and drop file upload
- Translate entire subtitle sets
- Download translated subtitles

### 6. **User Authentication**
- Secure registration and login
- Session management
- Password hashing with Werkzeug
- User database with SQLite

## 🎨 Design Features

- **Modern UI**: White/Blue gradient color scheme
- **Glassmorphism**: Frosted glass effect on panels and cards
- **Responsive Design**: Works perfectly on desktop and mobile
- **Smooth Animations**: Fade-in, slide, scale animations throughout
- **Accessibility**: Proper semantic HTML and keyboard navigation

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite
- **Authentication**: Werkzeug (password hashing)
- **Architecture**: MVC pattern with JSON-based rules

### Frontend
- **Languages**: HTML5, CSS3, Vanilla JavaScript
- **Features**: 
  - Web Speech API for voice recognition
  - Speech Synthesis API for voice output
  - Fetch API for AJAX requests
  - Local storage for user preferences

### Translation Engine
- **Type**: Rule-based (dictionary + grammar rules)
- **Rules**: JSON files for dictionaries, grammar rules, and idioms
- **Confidence Scoring**: Word-level confidence indicators

## 📁 Project Structure

```
nlp2/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── templates/
│   ├── base.html                  # Base template with navbar
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── index.html                 # Home page with feature cards
│   ├── translator.html            # Text/Voice translator
│   ├── idiom.html                 # Idiom translator
│   ├── slang.html                 # Slang normalizer
│   ├── historical.html            # Historical translator
│   └── video.html                 # Video subtitle translator
├── static/
│   ├── css/
│   │   ├── style.css              # Main stylesheet
│   │   └── auth.css               # Authentication page styles
│   ├── js/
│   │   ├── main.js                # Global JavaScript
│   │   ├── auth.js                # Authentication logic
│   │   ├── home.js                # Home page interactions
│   │   ├── translator.js          # Text translator
│   │   ├── idiom.js               # Idiom translator
│   │   ├── slang.js               # Slang normalizer
│   │   ├── historical.js          # Historical translator
│   │   └── video.js               # Video subtitle translator
│   └── images/                    # (For future use)
└── rules/
    ├── dictionaries.json          # Translation dictionaries
    ├── grammar_rules.json         # Grammar rules
    └── idioms.json                # Idiom database
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Step 1: Clone/Download Project
```bash
cd c:\Users\nandi\Documents\nlp2
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 5: Access the App
1. Open your browser
2. Navigate to `http://localhost:5000`
3. Register a new account or login
4. Start translating!

## 📚 Usage Guide

### Text/Voice Translator
1. Go to "Text/Voice" section
2. Enter text or click microphone icon
3. Select target language
4. Click "Translate"
5. View translation, explanation, and confidence score
6. Click speaker icon to hear pronunciation
7. Copy or download results

### Idiom Translator
1. Go to "Idioms" section
2. Enter an English idiom (e.g., "break a leg")
3. Select target language
4. View meaning, translation, and cultural context
5. Copy results as needed

### Slang Normalizer
1. Go to "Slang" section
2. Paste chat/SMS text with abbreviations
3. Click "Normalize Text"
4. Review conversion with explanations
5. Download professional version

### Historical Translator
1. Go to "Historical" section
2. Paste Old/Middle English text
3. Click "Modernize Text"
4. View modern equivalent with etymological notes
5. Download for reference

### Video Subtitle Translator
1. Go to "Subtitles" section
2. Upload SRT/VTT file or paste subtitle text
3. Select target language
4. Click "Translate Subtitles"
5. Download translated subtitles

## 🔐 Security Features

- Password hashing with `werkzeug.security`
- Session-based authentication
- CSRF protection ready (implement in production)
- SQL injection prevention with parameterized queries
- Input validation on all forms

## 🎯 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Translation APIs
- `POST /api/translate` - Text translation
- `POST /api/translate-idiom` - Idiom translation
- `POST /api/normalize-slang` - Slang normalization
- `POST /api/translate-historical` - Historical translation
- `POST /api/translate-video` - Video subtitle translation

### Pages
- `GET /home` - Home page
- `GET /text-translator` - Text translator
- `GET /idiom-translator` - Idiom translator
- `GET /slang-normalizer` - Slang normalizer
- `GET /historical-translator` - Historical translator
- `GET /video-translator` - Video subtitle translator

## 📊 Translation Rules Format

### dictionaries.json
```json
{
  "en_hindi": {
    "word": {
      "word": "translation",
      "pos": "part_of_speech",
      "rule": "grammar_rule",
      "confidence": 0.95
    }
  }
}
```

### grammar_rules.json
```json
{
  "rule_type": {
    "language": "description of rule"
  }
}
```

### idioms.json
```json
{
  "idiom_phrase": {
    "meaning": "English meaning",
    "translations": {
      "hindi": "translation",
      "spanish": "translation"
    },
    "explanation": "detailed explanation",
    "example": "usage example",
    "origin": "origin information"
  }
}
```

## 🎨 Customization

### Colors
Edit the CSS variables in `static/css/style.css`:
```css
:root {
  --primary-color: #1e40af;
  --accent-color: #06b6d4;
  /* ... more colors ... */
}
```

### Adding New Languages
1. Add words to `rules/dictionaries.json`
2. Add grammar rules to `rules/grammar_rules.json`
3. Update language selects in HTML templates

### Adding New Translation Rules
1. Edit respective JSON files in `rules/` folder
2. Restart the Flask server
3. Rules are loaded automatically on app startup

## 🐛 Troubleshooting

### Issue: "Module not found" errors
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Voice input not working
**Solution**: Voice API requires HTTPS in production or is limited in some browsers
- Use Chrome/Edge for best support
- Safari may require HTTPS

### Issue: Database errors
**Solution**: Delete `users.db` to reset the database:
```bash
del users.db
python app.py
```

### Issue: Port 5000 already in use
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📱 Browser Support

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 11+
- ✅ Edge 79+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🚀 Future Enhancements

- [ ] Machine learning-based translation (TensorFlow/PyTorch)
- [ ] Real-time collaborative translation
- [ ] Multiple file format support
- [ ] Translation history and bookmarks
- [ ] User preferences and custom dictionaries
- [ ] Admin panel for rule management
- [ ] API key authentication for production
- [ ] Rate limiting and caching
- [ ] Multi-language support beyond Hindi/Spanish/French
- [ ] Video subtitle extraction from MP4 files
- [ ] Batch translation processing
- [ ] Export to multiple formats (PDF, DOCX, etc.)

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Development

### Running in Debug Mode
```bash
python app.py
```

### Database Management
Access SQLite:
```bash
sqlite3 users.db
```

### Adding Middleware
Update `app.py` to add custom middleware:
```python
@app.before_request
def before_request():
    # Custom logic here
    pass
```

## 📧 Support

For issues or questions, please check the troubleshooting section or create an issue in the project repository.

## 🙏 Acknowledgments

- Built with Flask microframework
- Uses Web Speech API for voice features
- Designed with modern web standards
- Inspired by professional translation services

---

**Desi Translate** - Breaking language barriers with AI-powered explanations. 🌐✨

Version: 1.0.0
Last Updated: January 2026
