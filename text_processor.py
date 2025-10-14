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

