# 🚀 QUICK START GUIDE - DESI TRANSLATE

## System Requirements
- Windows 10/11 or macOS/Linux
- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## ⚡ Quick Setup (5 minutes)

### Step 1: Navigate to Project Directory
```powershell
cd "C:\Users\nandi\Documents\nlp2"
```

### Step 2: Create Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run the Application
```powershell
python app.py
```

### Step 5: Open in Browser
```
http://localhost:5000
```

---

## 👤 First Time Setup

### Create Your Account
1. Click **"Register"** button on login page
2. Enter username, email, and password
3. Click **"Create Account"**
4. You'll be redirected to login page
5. Login with your credentials

---

## 📖 Feature Quick Links

### Text Translator
- **URL**: `http://localhost:5000/text-translator`
- **Features**:
  - Type or speak text
  - Select target language
  - Get instant translation with explanations
  - Listen to pronunciation
  - Copy or download results

### Idiom Translator
- **URL**: `http://localhost:5000/idiom-translator`
- **Examples to try**:
  - "break a leg"
  - "piece of cake"
  - "raining cats and dogs"
  - "once in a blue moon"

### Slang Normalizer
- **URL**: `http://localhost:5000/slang-normalizer`
- **Try these**:
  - "omg u r so gr8 thx 4 msg"
  - "btw did u c that lol"
  - "nvm ill msg u l8r"

### Historical Translator
- **URL**: `http://localhost:5000/historical-translator`
- **Try these**:
  - "Thou art wise"
  - "Doth thee forsooth"
  - "Hath thine knowledge"

### Video Subtitle Translator
- **URL**: `http://localhost:5000/video-translator`
- **Supports**: SRT and VTT subtitle files
- **Drag and drop** file or paste content

---

## 🎯 Translation Examples

### English to Hindi
**Input**: "Hello, how are you today?"
**Output**: "नमस्ते, आप आज कैसे हैं?"
**Explanation**: Word-by-word breakdown with grammar rules

### English to Spanish
**Input**: "Good morning, friend!"
**Output**: "¡Buenos días, amigo!"
**Explanation**: Grammar rules and pronunciation guide

### English to French
**Input**: "I love this beautiful day"
**Output**: "J'aime cette belle journée"
**Explanation**: Grammar rules and pronunciation guide

---

## 🔧 Common Tasks

### Change Translation Language
1. Open any translator page
2. Use the **"To Language"** dropdown
3. Select: Hindi, Spanish, or French
4. Click Translate again

### Download Translation
1. Translate text
2. Click **"Download"** button
3. File saved as `translation_[timestamp].txt`

### Listen to Translation
1. After translation, click **🔊 Speaker** icon
2. Browser will play the translated text
3. Adjust volume in browser settings

### Use Voice Input
1. Click **🎤 Microphone** icon
2. Speak clearly
3. Text appears automatically

### Share Translation
1. Click **Copy** button
2. Paste in email, chat, or document
3. Share with others

---

## 🐛 Troubleshooting

### Application Won't Start
```
Error: Address already in use
Solution: Change port in app.py from 5000 to 5001
```

### Login Page Not Working
```
Delete users.db to reset database
python app.py
```

### Voice Features Not Working
```
Use Chrome or Edge browser
Ensure microphone is enabled
Check browser permissions
```

### Translation Seems Wrong
```
Database has basic dictionary
Add more words to rules/dictionaries.json
Restart the application
```

---

## 📁 File Locations

| File | Purpose |
|------|---------|
| `app.py` | Main application |
| `templates/*.html` | Web pages |
| `static/css/*.css` | Styling |
| `static/js/*.js` | Functionality |
| `rules/*.json` | Translation data |
| `users.db` | User database |
| `requirements.txt` | Dependencies |

---

## 🚪 Stopping the Application

Press `Ctrl + C` in the terminal window:
```
^C
```

---

## 💡 Tips & Tricks

1. **Keyboard Shortcut**: Press `Ctrl + Enter` to translate
2. **Mobile**: Works on phones and tablets
3. **Offline**: Once loaded, basic functionality works offline
4. **Multiple Tabs**: Open in different tabs for quick switching
5. **Bookmark**: Save favorite pages for quick access

---

## 📚 Next Steps

1. ✅ Complete the setup
2. ✅ Create your account
3. ✅ Try each translator feature
4. ✅ Add custom dictionary words to `rules/dictionaries.json`
5. ✅ Explore all features

---

## 🎓 Learning Resources

- **Flask Docs**: https://flask.palletsprojects.com/
- **Web Speech API**: https://www.w3.org/TR/speech-api/
- **JSON Format**: https://www.json.org/
- **Python**: https://docs.python.org/3/

---

## 📞 Getting Help

1. Check the **README.md** for detailed documentation
2. Review **config.py** for settings
3. Examine **rules/** folder for translation data
4. Check browser console for JavaScript errors (F12)

---

## 🎉 You're All Set!

Your Desi Translate application is ready to use. Start translating and learning languages today!

**Happy Translating!** 🌍✨

---

*Desi Translate v1.0.0 - January 2026*
