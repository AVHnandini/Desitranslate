# 📑 DESI TRANSLATE - COMPLETE FILE INDEX

## 🎯 Start Here!

**Quick Start**: Read [QUICKSTART.md](QUICKSTART.md) first - Get running in 5 minutes!

---

## 📂 ROOT DIRECTORY FILES

### Core Application
| File | Size | Purpose |
|------|------|---------|
| [app.py](app.py) | 15 KB | Main Flask application with all routes and API endpoints |
| [config.py](config.py) | 2 KB | Configuration settings and application constants |
| [requirements.txt](requirements.txt) | 1 KB | Python dependencies list |

### Utilities
| File | Purpose |
|------|---------|
| [manage_translations.py](manage_translations.py) | Translation database management utility |

### Documentation
| File | Purpose | Read When |
|------|---------|-----------|
| [README.md](README.md) | Complete documentation | Need full details |
| [QUICKSTART.md](QUICKSTART.md) | Setup and usage guide | Starting out |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project statistics | Need overview |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Developer guide | Extending project |

### System Files
| File | Purpose |
|------|---------|
| [.gitignore](.gitignore) | Git repository exclusions |

---

## 📁 TEMPLATES DIRECTORY

### HTML Templates (`templates/`)

| File | Lines | Purpose |
|------|-------|---------|
| [base.html](templates/base.html) | 45 | Navigation and layout template |
| [login.html](templates/login.html) | 30 | User login page |
| [register.html](templates/register.html) | 35 | User registration page |
| [index.html](templates/index.html) | 105 | Home page with feature cards |
| [translator.html](templates/translator.html) | 95 | Text/Voice translator page |
| [idiom.html](templates/idiom.html) | 75 | Idiom translator page |
| [slang.html](templates/slang.html) | 75 | Slang normalizer page |
| [historical.html](templates/historical.html) | 75 | Historical document translator |
| [video.html](templates/video.html) | 85 | Video subtitle translator |

---

## 🎨 STATIC FILES DIRECTORY

### CSS Stylesheets (`static/css/`)

| File | Lines | Purpose |
|------|-------|---------|
| [style.css](static/css/style.css) | 1200+ | Main stylesheet with responsive design |
| [auth.css](static/css/auth.css) | 450+ | Authentication pages styling |

### JavaScript Files (`static/js/`)

| File | Lines | Purpose |
|------|-------|---------|
| [main.js](static/js/main.js) | 30 | Global navigation and utilities |
| [auth.js](static/js/auth.js) | 80 | Login and registration logic |
| [home.js](static/js/home.js) | 50 | Home page animations |
| [translator.js](static/js/translator.js) | 250+ | Text translator with voice features |
| [idiom.js](static/js/idiom.js) | 150+ | Idiom translation logic |
| [slang.js](static/js/slang.js) | 140+ | Slang normalization logic |
| [historical.js](static/js/historical.js) | 140+ | Historical translation logic |
| [video.js](static/js/video.js) | 150+ | Video subtitle translation logic |

### Images Directory (`static/images/`)
- Ready for future image assets
- Currently empty (for logos, icons, etc.)

---

## 📊 RULES & DATA DIRECTORY

### JSON Data Files (`rules/`)

| File | Entries | Purpose |
|------|---------|---------|
| [dictionaries.json](rules/dictionaries.json) | 45+ | Translation dictionaries (en→hi, es, fr) |
| [grammar_rules.json](rules/grammar_rules.json) | 5 | Grammar rule explanations |
| [idioms.json](rules/idioms.json) | 10 | Idiom database with translations |

---

## 🔐 DATABASE

### SQLite Database
- **File**: `users.db` (created at runtime)
- **Purpose**: Store user credentials
- **Tables**: users (id, username, email, password, created_at)

---

## 📖 READING GUIDE BY PURPOSE

### "I want to get started quickly"
1. Read [QUICKSTART.md](QUICKSTART.md) - 5 minutes
2. Follow the setup steps
3. Start translating!

### "I want to understand the project"
1. Read [README.md](README.md) - Complete overview
2. Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Statistics
3. Review [DEVELOPMENT.md](DEVELOPMENT.md) - Architecture

### "I want to extend the project"
1. Read [DEVELOPMENT.md](DEVELOPMENT.md) - Developer guide
2. Check [config.py](config.py) - Configuration
3. Review [app.py](app.py) - Backend code
4. Examine [rules/](rules/) - Data structure

### "I want to customize the UI"
1. Edit [static/css/style.css](static/css/style.css) - Colors, fonts
2. Modify [templates/](templates/) - HTML structure
3. Update [static/js/](static/js/) - Interactions

### "I want to add new languages"
1. Edit [rules/dictionaries.json](rules/dictionaries.json)
2. Add new language pair with words
3. Update HTML select elements
4. Test in browser

### "I want to understand the code"
1. Start with [app.py](app.py) - Main backend
2. Read [templates/base.html](templates/base.html) - HTML structure
3. Check [static/js/translator.js](static/js/translator.js) - Frontend logic
4. Review [config.py](config.py) - Settings

---

## 🎯 FILE RELATIONSHIPS

### Authentication Flow
```
register.html → auth.js → app.py (/register) → users.db
     ↓            ↓            ↓                    ↓
register      register()    @app.route         Create user
form          handler       register
```

### Translation Flow
```
translator.html → translator.js → app.py (/api/translate) → rules/dictionaries.json
      ↓                ↓              ↓                          ↓
input           translateText()   def translate_text()      lookup word
text            handler          function                  return translation
```

### Page Structure
```
base.html (navbar, layout)
    ↓
├── login.html (auth page)
├── register.html (auth page)
├── index.html (home page)
├── translator.html (feature page)
├── idiom.html (feature page)
├── slang.html (feature page)
├── historical.html (feature page)
└── video.html (feature page)
```

---

## 🔗 API ENDPOINT TO FILE MAPPING

| Endpoint | Handler File | Returns |
|----------|--------------|---------|
| POST /login | [auth.js](static/js/auth.js) + [app.py](app.py) | JSON response |
| POST /register | [auth.js](static/js/auth.js) + [app.py](app.py) | JSON response |
| POST /api/translate | [translator.js](static/js/translator.js) + [app.py](app.py) | Translation JSON |
| POST /api/translate-idiom | [idiom.js](static/js/idiom.js) + [app.py](app.py) | Idiom JSON |
| POST /api/normalize-slang | [slang.js](static/js/slang.js) + [app.py](app.py) | Normalized text |
| POST /api/translate-historical | [historical.js](static/js/historical.js) + [app.py](app.py) | Modern text |
| POST /api/translate-video | [video.js](static/js/video.js) + [app.py](app.py) | Subtitles JSON |

---

## 📋 FEATURE TO FILE MAPPING

| Feature | HTML | JavaScript | Python | Data |
|---------|------|-----------|--------|------|
| User Auth | login.html, register.html | auth.js | app.py | users.db |
| Text Translator | translator.html | translator.js | app.py | dictionaries.json |
| Voice Input | translator.html | translator.js | app.py | - |
| Voice Output | translator.html | translator.js | - | - |
| Idiom Translator | idiom.html | idiom.js | app.py | idioms.json |
| Slang Normalizer | slang.html | slang.js | app.py | - |
| Historical Translator | historical.html | historical.js | app.py | - |
| Video Subtitles | video.html | video.js | app.py | dictionaries.json |
| Navigation | base.html | main.js | app.py | - |
| Home Page | index.html | home.js | app.py | - |
| Styling | All templates | - | - | style.css, auth.css |

---

## 🚀 DEPLOYMENT FILES

### Required for Deployment
- [app.py](app.py) - Application
- [requirements.txt](requirements.txt) - Dependencies
- [config.py](config.py) - Configuration
- [templates/](templates/) - All HTML files
- [static/](static/) - All CSS/JS/images
- [rules/](rules/) - All translation data

### Optional for Deployment
- [README.md](README.md) - Documentation
- [QUICKSTART.md](QUICKSTART.md) - Setup guide
- [DEVELOPMENT.md](DEVELOPMENT.md) - Dev guide
- [.gitignore](.gitignore) - Git config

---

## 📈 CODE STATISTICS

### By Type
| Type | Files | Lines |
|------|-------|-------|
| HTML | 9 | 635 |
| CSS | 2 | 1,650+ |
| JavaScript | 8 | 940+ |
| Python | 3 | 610+ |
| JSON | 3 | 200+ |
| Markdown | 4 | 800+ |
| **TOTAL** | **29** | **4,835+** |

### By Directory
| Directory | Files | Purpose |
|-----------|-------|---------|
| Root | 8 | Core & docs |
| templates/ | 9 | Web pages |
| static/css/ | 2 | Styling |
| static/js/ | 8 | Frontend logic |
| static/images/ | 0 | Assets (empty) |
| rules/ | 3 | Translation data |

---

## ✅ QUICK FILE REFERENCE

### Need to change...

**Login/Auth System** → [app.py](app.py), [auth.js](static/js/auth.js)

**Colors/Design** → [style.css](static/css/style.css)

**Translations** → [dictionaries.json](rules/dictionaries.json)

**Layout** → [base.html](templates/base.html)

**Translator Logic** → [translator.js](static/js/translator.js), [app.py](app.py)

**Supported Languages** → [HTML templates](templates/), [app.py](app.py)

**Settings/Config** → [config.py](config.py)

**Utilities** → [manage_translations.py](manage_translations.py)

---

## 🎓 LEARNING PATH

For learning the codebase:

1. **Start**: [README.md](README.md) - Overview
2. **Setup**: [QUICKSTART.md](QUICKSTART.md) - Installation
3. **Run**: `python app.py` - Start server
4. **Understand**:
   - [app.py](app.py) - Backend routes
   - [templates/base.html](templates/base.html) - HTML structure
   - [static/css/style.css](static/css/style.css) - Styling
5. **Explore**:
   - [translator.js](static/js/translator.js) - Frontend logic
   - [idiom.html](templates/idiom.html) - Feature example
   - [rules/dictionaries.json](rules/dictionaries.json) - Data format
6. **Extend**: [DEVELOPMENT.md](DEVELOPMENT.md) - Add features

---

## 📞 FILE HELP

| Question | File |
|----------|------|
| How to get started? | [QUICKSTART.md](QUICKSTART.md) |
| How does it work? | [README.md](README.md) |
| Where is the backend? | [app.py](app.py) |
| Where is the styling? | [static/css/style.css](static/css/style.css) |
| Where is the data? | [rules/](rules/) |
| How to extend it? | [DEVELOPMENT.md](DEVELOPMENT.md) |
| How to configure? | [config.py](config.py) |
| What are the stats? | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |

---

## 🔐 Important Files

**Don't Delete:**
- [app.py](app.py) - Core application
- [requirements.txt](requirements.txt) - Dependencies
- [templates/](templates/) - Web pages
- [static/](static/) - CSS, JS, images
- [rules/](rules/) - Translation data

**Safe to Modify:**
- [config.py](config.py) - Settings
- [static/css/](static/css/) - Styling
- [rules/](rules/) - Translation data
- [README.md](README.md) - Documentation

**Read-Only (Recommended):**
- [QUICKSTART.md](QUICKSTART.md) - Setup guide
- [DEVELOPMENT.md](DEVELOPMENT.md) - Dev guide
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Stats

---

## 🎉 You're Ready!

All files are in place and documented. 

**Next Step**: Read [QUICKSTART.md](QUICKSTART.md) and start using the application!

---

**Desi Translate v1.0.0**
*Complete Full-Stack Language Translation Platform*
*All 29 files ready to use!* ✨

Last Updated: January 2026
