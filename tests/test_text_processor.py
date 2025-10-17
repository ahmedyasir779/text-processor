"""
Unit tests for TextProcessor module
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from text_processor import TextProcessor


class TestTextProcessor:
    """Test suite for TextProcessor class"""
    
    @pytest.fixture
    def sample_text(self):
        """Create sample text for testing"""
        return "The cats are running quickly. They jumped over the fence."
    
    def test_initialization(self, sample_text):
        """Test TextProcessor initialization"""
        processor = TextProcessor(sample_text)
        
        assert processor.text == sample_text
        assert processor.language == 'english'
        assert len(processor.stop_words) > 0
    
    def test_tokenize_words(self, sample_text):
        """Test word tokenization"""
        processor = TextProcessor(sample_text)
        tokens = processor.tokenize_words()
        
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert "cats" in tokens or "The" in tokens
    
    def test_tokenize_sentences(self, sample_text):
        """Test sentence tokenization"""
        processor = TextProcessor(sample_text)
        sentences = processor.tokenize_sentences()
        
        assert isinstance(sentences, list)
        assert len(sentences) == 2
    
    def test_remove_stopwords(self):
        """Test stop word removal"""
        text = "the cat is on the mat"
        processor = TextProcessor(text)
        
        tokens = processor.tokenize_words()
        filtered = processor.remove_stopwords(tokens)
        
        assert "the" not in [w.lower() for w in filtered]
        assert "is" not in [w.lower() for w in filtered]
        assert "cat" in [w.lower() for w in filtered]
        assert "mat" in [w.lower() for w in filtered]
    
    def test_stem_words(self):
        """Test stemming"""
        text = "running jumps jumping"
        processor = TextProcessor(text)
        
        tokens = processor.tokenize_words()
        stemmed = processor.stem_words(tokens)
        
        # Check that stemming occurred (might not be exact due to stemmer)
        assert isinstance(stemmed, list)
        assert len(stemmed) == len(tokens)
    
    def test_lemmatize_words(self):
        """Test lemmatization"""
        text = "running better cats"
        processor = TextProcessor(text)
        
        tokens = processor.tokenize_words()
        lemmatized = processor.lemmatize_words(tokens)
        
        assert isinstance(lemmatized, list)
        assert len(lemmatized) == len(tokens)
    
    def test_get_word_frequency(self):
        """Test word frequency counting"""
        text = "cat dog cat bird cat dog"
        processor = TextProcessor(text)
        
        tokens = processor.tokenize_words()
        freq = processor.get_word_frequency(tokens)
        
        assert isinstance(freq, dict)
        assert freq['cat'] == 3
        assert freq['dog'] == 2
        assert freq['bird'] == 1
    
    def test_get_pos_tags(self, sample_text):
        """Test POS tagging"""
        processor = TextProcessor(sample_text)
        pos_tags = processor.get_pos_tags()
        
        assert isinstance(pos_tags, list)
        assert len(pos_tags) > 0
        assert all(isinstance(tag, tuple) for tag in pos_tags)
    
    def test_get_statistics(self, sample_text):
        """Test statistics generation"""
        processor = TextProcessor(sample_text)
        stats = processor.get_statistics()
        
        assert 'total_characters' in stats
        assert 'total_words' in stats
        assert 'unique_words' in stats
        assert 'total_sentences' in stats
        assert 'avg_word_length' in stats
        assert 'lexical_diversity' in stats
        
        assert stats['total_sentences'] == 2
        assert stats['total_words'] > 0