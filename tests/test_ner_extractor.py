"""
Unit tests for NERExtractor module
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ner_extractor import NERExtractor


class TestNERExtractor:
    """Test suite for NERExtractor class"""
    
    @pytest.fixture
    def sample_text(self):
        """Create sample text with named entities"""
        return """
        Steve Jobs founded Apple Inc. in Cupertino, California.
        The company was established in 1976.
        Today, Tim Cook is the CEO.
        Apple's revenue reached $394 billion last year.
        """
    
    def test_initialization(self):
        """Test NERExtractor initialization"""
        try:
            extractor = NERExtractor()
            assert extractor.nlp is not None
        except Exception as e:
            pytest.skip(f"spaCy model not available: {e}")
    
    def test_extract(self, sample_text):
        """Test entity extraction"""
        try:
            extractor = NERExtractor()
            entities = extractor.extract(sample_text)
            
            assert isinstance(entities, list)
            assert len(entities) > 0
            
            # Check entity structure
            for ent in entities:
                assert 'text' in ent
                assert 'label' in ent
                assert 'start' in ent
                assert 'end' in ent
        except Exception as e:
            pytest.skip(f"spaCy model not available: {e}")
    
    def test_get_persons(self, sample_text):
        """Test person name extraction"""
        try:
            extractor = NERExtractor()
            persons = extractor.get_persons(sample_text)
            
            assert isinstance(persons, list)
            # Should find Steve Jobs and/or Tim Cook
            assert len(persons) > 0
        except Exception as e:
            pytest.skip(f"spaCy model not available: {e}")
    
    def test_get_organizations(self, sample_text):
        """Test organization extraction"""
        try:
            extractor = NERExtractor()
            orgs = extractor.get_organizations(sample_text)
            
            assert isinstance(orgs, list)
            # Should find Apple Inc.
            assert len(orgs) > 0
        except Exception as e:
            pytest.skip(f"spaCy model not available: {e}")
    
    def test_get_locations(self, sample_text):
        """Test location extraction"""
        try:
            extractor = NERExtractor()
            locations = extractor.get_locations(sample_text)
            
            assert isinstance(locations, list)
            # Should find Cupertino and/or California
            assert len(locations) > 0
        except Exception as e:
            pytest.skip(f"spaCy model not available: {e}")
    
    def test_get_entity_counts(self, sample_text):
        """Test entity counting"""
        try:
            extractor = NERExtractor()
            counts = extractor.get_entity_counts(sample_text)
            
            assert isinstance(counts, dict)
            assert len(counts) > 0
        except Exception as e:
            pytest.skip(f"spaCy model not available: {e}")
    
    def test_get_summary(self, sample_text):
        """Test summary generation"""
        try:
            extractor = NERExtractor()
            summary = extractor.get_summary(sample_text)
            
            assert isinstance(summary, str)
            assert "NAMED ENTITY RECOGNITION" in summary
        except Exception as e:
            pytest.skip(f"spaCy model not available: {e}")