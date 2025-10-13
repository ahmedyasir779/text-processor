import re
from typing import List, Dict, Set
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.stem import WordNetLemmatizer
import spacy


class TextProcessor:
    def __init__(self, text: str, language: str = 'english'):

        self.text = text
        self.language = language
        self.tokens = []
        self.sentences = []
        
        # Initialize processors
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        
        # Load spaCy model (lazy loading)
        self._nlp = None
        
        # Get stop words
        try:
            self.stop_words = set(stopwords.words(language))
        except:
            print(f"Warning: Stop words for '{language}' not found. Using English.")
            self.stop_words = set(stopwords.words('english'))
    
    @property
    def nlp(self):
        if self._nlp is None:
            try:
                self._nlp = spacy.load('en_core_web_sm')
            except:
                print("Warning: spaCy model not loaded. Some features won't work.")
                print("Run: python -m spacy download en_core_web_sm")
        return self._nlp
    
    def tokenize_words(self) -> List[str]:
        self.tokens = word_tokenize(self.text)
        return self.tokens
    
    def tokenize_sentences(self) -> List[str]:
        self.sentences = sent_tokenize(self.text)
        return self.sentences
    
    def remove_stopwords(self, tokens: List[str] = None) -> List[str]:
        if tokens is None:
            tokens = self.tokenize_words()
        
        # Remove stop words (case-insensitive)
        filtered = [word for word in tokens 
                   if word.lower() not in self.stop_words]
        
        return filtered
    
    def stem_words(self, tokens: List[str] = None) -> List[str]:
        if tokens is None:
            tokens = self.tokenize_words()
        
        stemmed = [self.stemmer.stem(word) for word in tokens]
        return stemmed
    
    def lemmatize_words(self, tokens: List[str] = None) -> List[str]:
        if tokens is None:
            tokens = self.tokenize_words()
        
        lemmatized = [self.lemmatizer.lemmatize(word.lower()) 
                     for word in tokens]
        return lemmatized
    
    def get_word_frequency(self, tokens: List[str] = None) -> Dict[str, int]:
        if tokens is None:
            tokens = self.tokenize_words()
        
        freq = {}
        for word in tokens:
            word_lower = word.lower()
            freq[word_lower] = freq.get(word_lower, 0) + 1
        
        # Sort by frequency (most common first)
        sorted_freq = dict(sorted(freq.items(), 
                                 key=lambda x: x[1], 
                                 reverse=True))
        return sorted_freq
    
    def extract_nouns(self) -> List[str]:
        if self.nlp is None:
            return []
        
        doc = self.nlp(self.text)
        nouns = [token.text for token in doc if token.pos_ == 'NOUN']
        return nouns
    
    def extract_verbs(self) -> List[str]:
        if self.nlp is None:
            return []
        
        doc = self.nlp(self.text)
        verbs = [token.text for token in doc if token.pos_ == 'VERB']
        return verbs
    
    def extract_adjectives(self) -> List[str]:
        if self.nlp is None:
            return []
        
        doc = self.nlp(self.text)
        adjectives = [token.text for token in doc if token.pos_ == 'ADJ']
        return adjectives
    
    def get_pos_tags(self) -> List[tuple]:
        tokens = self.tokenize_words()
        pos_tags = nltk.pos_tag(tokens)
        return pos_tags
    
    def get_statistics(self) -> Dict:
        tokens = self.tokenize_words()
        sentences = self.tokenize_sentences()
        
        # Remove punctuation for word count
        words = [w for w in tokens if w.isalnum()]
        
        # Unique words
        unique_words = set(w.lower() for w in words)
        
        # Average word length
        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        
        # Average sentence length
        avg_sent_length = len(words) / len(sentences) if sentences else 0
        
        return {
            'total_characters': len(self.text),
            'total_tokens': len(tokens),
            'total_words': len(words),
            'unique_words': len(unique_words),
            'total_sentences': len(sentences),
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sent_length, 2),
            'lexical_diversity': round(len(unique_words) / len(words), 3) if words else 0
        }


# ============================================
# TESTING CODE
# ============================================

if __name__ == "__main__":
    # Test text
    test_text = """
    The cats are running quickly in the beautiful garden. 
    They jumped over the fence yesterday.
    The better solution was found by the researchers.
    Machine learning is revolutionizing technology!
    """
    
    print("=" * 60)
    print("TEXT PROCESSOR - TEST")
    print("=" * 60)
    
    print("\n📝 ORIGINAL TEXT:")
    print(test_text)
    
    # Initialize processor
    processor = TextProcessor(test_text)
    
    # 1. Tokenization
    print("\n\n1️⃣ WORD TOKENIZATION:")
    words = processor.tokenize_words()
    print(f"Tokens: {words[:20]}...")  # Show first 20
    print(f"Total tokens: {len(words)}")
    
    print("\n2️⃣ SENTENCE TOKENIZATION:")
    sentences = processor.tokenize_sentences()
    for i, sent in enumerate(sentences, 1):
        print(f"  {i}. {sent.strip()}")
    
    # 3. Stop word removal
    print("\n\n3️⃣ REMOVE STOP WORDS:")
    filtered = processor.remove_stopwords(words)
    print(f"Before: {words[:15]}")
    print(f"After: {filtered[:15]}")
    print(f"Removed {len(words) - len(filtered)} stop words")
    
    # 4. Stemming
    print("\n\n4️⃣ STEMMING:")
    stemmed = processor.stem_words(words)
    print("Original → Stemmed:")
    for orig, stem in list(zip(words, stemmed))[:10]:
        if orig != stem:
            print(f"  {orig} → {stem}")
    
    # 5. Lemmatization
    print("\n\n5️⃣ LEMMATIZATION:")
    lemmatized = processor.lemmatize_words(words)
    print("Original → Lemmatized:")
    for orig, lem in list(zip(words, lemmatized))[:10]:
        if orig.lower() != lem:
            print(f"  {orig} → {lem}")
    
    # 6. Word frequency
    print("\n\n6️⃣ WORD FREQUENCY:")
    freq = processor.get_word_frequency(filtered)
    print("Top 10 most common words:")
    for word, count in list(freq.items())[:10]:
        print(f"  {word}: {count}")
    
    # 7. POS tagging
    print("\n\n7️⃣ PART-OF-SPEECH TAGS:")
    pos_tags = processor.get_pos_tags()
    print("First 15 tagged words:")
    for word, tag in pos_tags[:15]:
        print(f"  {word} → {tag}")
    
    # 8. Extract word types
    print("\n\n8️⃣ EXTRACT WORD TYPES:")
    
    nouns = processor.extract_nouns()
    print(f"\nNouns (things): {nouns}")
    
    verbs = processor.extract_verbs()
    print(f"Verbs (actions): {verbs}")
    
    adjectives = processor.extract_adjectives()
    print(f"Adjectives (descriptions): {adjectives}")
    
    # 9. Statistics
    print("\n\n9️⃣ TEXT STATISTICS:")
    stats = processor.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS COMPLETE!")
    print("=" * 60)