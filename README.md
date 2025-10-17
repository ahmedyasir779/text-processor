# 📝 Text Processing Toolkit

A professional NLP toolkit for cleaning, processing, and extracting information from text.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

### 🧹 Text Cleaning
- Remove HTML tags, URLs, emails, phone numbers
- Normalize unicode characters (café → cafe)
- Handle special characters and whitespace
- Case conversion (upper/lower)

### ⚙️ Linguistic Processing
- **Tokenization** - Split text into words and sentences
- **Stop word removal** - Remove common words (the, a, is, etc.)
- **Stemming** - Crude word reduction (running → run)
- **Lemmatization** - Smart word reduction (better → good)
- **POS tagging** - Identify word types (nouns, verbs, adjectives)
- **Word frequency analysis** - Find most common words
- **Text statistics** - Lexical diversity, avg word length, etc.

### 📊 Information Extraction (Pattern-Based)
Extract structured data using regex:
- ✉️ Email addresses
- 📞 Phone numbers (multiple formats)
- 🌐 URLs
- 📅 Dates (multiple formats)
- ⏰ Times (12h/24h)
- 💰 Currency (USD, SAR)
- #️⃣ Hashtags & @mentions
- 🔢 IP addresses
- 💳 Credit cards (masked for security)

### 🤖 Named Entity Recognition (AI-Based)
Extract entities using spaCy:
- 👤 People names
- 🏢 Organizations
- 📍 Locations (cities, countries)
- 📅 Dates and times
- 💰 Money amounts
- 🎨 HTML visualization

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/ahmedyasir779/text-processor.git
cd text-processor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python download_nltk_data.py

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Basic Usage

**Clean text:**
```bash
python cli.py --file input.txt --clean --output clean.txt
```

**Extract emails, phones, URLs:**
```bash
python cli.py --file document.txt --extract-info
```

**Named entity recognition:**
```bash
python cli.py --file article.txt --extract-entities --visualize
```

**Full analysis:**
```bash
python cli.py --file text.txt --all
```

**Quick test:**
```bash
python cli.py --text "Apple Inc. is in Cupertino. Email: tim@apple.com" --all
```

## 📖 Usage Examples

### Example 1: Clean Messy Text

**Input:**
```
<h1>Contact Us</h1>
Visit https://example.com or email support@example.com
Call (555) 123-4567 today!!!
Price: $99.99
```

**Command:**
```bash
python cli.py --file messy.txt --clean --output clean.txt
```

**Output:**
```
Contact Us Visit or Call today Price 99 99
```

### Example 2: Extract Contact Information

**Command:**
```bash
python cli.py --file contacts.txt --extract-info
```

**Output:**
```
📌 EMAILS (2):
   • support@example.com
   • info@company.com

📌 PHONES (3):
   • (555) 123-4567
   • +1-555-987-6543
   • 555.111.2222

📌 URLS (1):
   • https://example.com
```

### Example 3: Named Entity Recognition

**Input:**
```
Ahmed works at Google in Riyadh.
He met Sarah from Microsoft yesterday.
The meeting cost $5000.
```

**Command:**
```bash
python cli.py --file meeting.txt --extract-entities
```

**Output:**
```
👤 People (2): Ahmed, Sarah
🏢 Organizations (2): Google, Microsoft
📍 Locations (1): Riyadh
💰 Money (1): $5000
```

### Example 4: Text Analysis

**Command:**
```bash
python cli.py --file article.txt --process --stats --frequency
```

**Output:**
```
📊 TEXT STATISTICS
Total words: 450
Unique words: 215
Total sentences: 25
Avg word length: 5.2
Avg sentence length: 18.0 words
Lexical diversity: 47.78%

TOP 10 MOST COMMON WORDS
1. technology: 12
2. data: 9
3. machine: 8
...
```

## 🔧 Usage as Python Library
```python
from text_cleaner import TextCleaner
from text_processor import TextProcessor
from info_extractor import InfoExtractor
from ner_extractor import NERExtractor

# 1. Clean text
cleaner = TextCleaner(messy_text)
clean_text = (cleaner
              .remove_html_tags()
              .remove_urls()
              .normalize_whitespace()
              .to_lowercase()
              .get_cleaned_text())

# 2. Process text
processor = TextProcessor(clean_text)
tokens = processor.tokenize_words()
lemmatized = processor.lemmatize_words(tokens)
freq = processor.get_word_frequency(lemmatized)

# 3. Extract structured info
info = InfoExtractor(text)
emails = info.extract_emails()
phones = info.extract_phones()
dates = info.extract_dates()

# 4. Named entity recognition
ner = NERExtractor()
entities = ner.extract(text)
persons = ner.get_persons()
organizations = ner.get_organizations()
```

## 🗂️ Project Structure
```
text-processor/
├── text_cleaner.py        # Text cleaning module
├── text_processor.py      # Linguistic processing
├── info_extractor.py      # Pattern-based extraction
├── ner_extractor.py       # AI-based NER
├── cli.py                 # Command-line interface
├── download_nltk_data.py  # NLTK data downloader
├── tests/                 # Test suite
├── data/                  # Sample data
├── output/                # Generated results
├── requirements.txt       # Dependencies
├── CHANGELOG.md           # Version history
└── README.md              # This file
```

## 🛠️ CLI Options
```
Input:
  --file, -f          Input text file
  --text, -t          Input text string

Processing Stages:
  --clean, -c         Clean text
  --process, -p       Linguistic processing
  --extract-info      Extract structured information
  --extract-entities  Named entity recognition

Options:
  --lowercase         Convert to lowercase
  --remove-stopwords  Remove stop words
  --lemmatize         Apply lemmatization
  --frequency         Show word frequencies
  --extract-pos       Extract nouns/verbs/adjectives
  --stats             Show statistics
  --visualize         Create HTML visualization

Output:
  --output, -o        Output file path
  --all               Run complete pipeline
```

## 📝 Requirements
```
Python 3.8+
nltk
spacy
unidecode
regex
colorama
```

## 🧪 Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific module tests
pytest tests/test_cleaner.py -v
```

## 📚 Documentation

- [CHANGELOG.md](CHANGELOG.md) - Version history and changes

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

**Ahmed**
- GitHub: [@YOUR-USERNAME](https://github.com/ahmedyasir779)
- LinkedIn: [Your Profile](https://www.linkedin.com/in/ahmed-yasir-907561206)

## 🙏 Acknowledgments

- Built as part of a 4-month AI/ML engineering learning journey
- Week 2 of 16-week roadmap
- Part of Month 1: Data & NLP Fundamentals

---

⭐ Star this repo if you find it useful!

📫 Questions? Open an issue or reach out!