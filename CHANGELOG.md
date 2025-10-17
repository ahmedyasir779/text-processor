# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] 

### Added
- **TextCleaner Module** 
  - HTML tag removal with regex
  - URL detection and removal
  - Email and phone number cleaning
  - Unicode normalization (café → cafe)
  - Whitespace normalization
  - Special character handling
  - Case conversion (upper/lower)
  
- **TextProcessor Module** 
  - Word tokenization using NLTK
  - Sentence tokenization
  - Stop word removal (English)
  - Stemming with PorterStemmer
  - Lemmatization with WordNetLemmatizer
  - POS (Part-of-Speech) tagging
  - Extract nouns, verbs, adjectives using spaCy
  - Word frequency analysis
  - Text statistics (lexical diversity, avg lengths)
  
- **InfoExtractor Module** 
  - Pattern-based extraction with regex
  - Email addresses
  - Phone numbers (US, international)
  - URLs (http/https/www)
  - Dates (multiple formats: slash, dash)
  - Times (12h/24h formats)
  - Currency (USD $, SAR)
  - Hashtags and mentions
  - Credit card numbers (masked)
  - IP addresses (IPv4)
  - Custom pattern support
  
- **NERExtractor Module** 
  - Named Entity Recognition with spaCy
  - Extract people names
  - Extract organizations
  - Extract locations (GPE)
  - Extract dates
  - Extract money amounts
  - Entity type counting
  - HTML visualization of entities
  - Custom label extraction
  
- **CLI Tool** 
  - Unified command-line interface
  - Colorful output with colorama
  - Multiple processing stages
  - File and direct text input
  - Flexible output options
  - Comprehensive help documentation
  - --all shortcut for full pipeline

### Technical Details
- **Total modules:** 4 core + 1 CLI
- **Lines of code:** ~1,800
- **Test coverage:** 85%+
- **Dependencies:** nltk, spacy, unidecode, regex, colorama
- **Python version:** 3.8+

### Performance
- Text cleaning: < 50ms for 1000 words
- NER extraction: < 200ms for 1000 words
- Pattern matching: < 10ms for 1000 words

### Lessons Learned
1. **Regex is powerful but tricky** - Spent hours debugging phone number patterns
2. **spaCy vs NLTK trade-offs** - spaCy is accurate but heavy, NLTK is lightweight
3. **Text preprocessing is 80% of NLP** - Clean data = better results
4. **Method chaining improves UX** - Makes APIs elegant and readable
5. **Pre-compiled regex patterns are faster** - 3x speed improvement
6. **Unicode is complex** - Many edge cases with international text

### Known Issues
- Credit card detection may have false positives
- Date parsing doesn't handle all formats (e.g., "Jan 1st")
- spaCy model download is 50MB (could be optimized)

### Future Improvements
- Add more languages (Arabic, Spanish, etc.)
- Implement custom NER training
- Add sentiment analysis
- Support for PDF/Word document parsing
- Batch processing for multiple files

## [0.3.0] 
### Added
- Named Entity Recognition module
- spaCy integration

## [0.2.0] 
### Added
- Text processing module
- Lemmatization and stemming

## [0.1.0] 
### Added
- Initial text cleaning module
- Basic regex patterns