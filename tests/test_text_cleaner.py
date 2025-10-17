"""
Unit tests for TextCleaner module
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from text_cleaner import TextCleaner


class TestTextCleaner:
    """Test suite for TextCleaner class"""
    
    @pytest.fixture
    def sample_text(self):
        """Create sample messy text for testing"""
        return """
        <h1>Hello World!</h1>
        Visit https://example.com and www.test.com
        Email: test@example.com
        Call: (555) 123-4567 or +1-555-987-6543
        Price: $99.99
        Special chars: @#$%^&*()
        Extra    spaces    and
        
        newlines
        Café résumé naïve
        """
    
    def test_initialization(self, sample_text):
        """Test TextCleaner initialization"""
        cleaner = TextCleaner(sample_text)
        
        assert cleaner.original_text == sample_text
        assert cleaner.text == sample_text
        assert len(cleaner.cleaning_steps) == 0
    
    def test_remove_html_tags(self):
        """Test HTML tag removal"""
        text = "<h1>Title</h1><p>Content</p>"
        cleaner = TextCleaner(text)
        result = cleaner.remove_html_tags().get_cleaned_text()
        
        assert "<h1>" not in result
        assert "</h1>" not in result
        assert "Title" in result
        assert "Content" in result
    
    def test_remove_urls(self):
        """Test URL removal"""
        text = "Check https://example.com and www.test.com"
        cleaner = TextCleaner(text)
        result = cleaner.remove_urls().get_cleaned_text()
        
        assert "https://example.com" not in result
        assert "www.test.com" not in result
        assert "Check" in result
    
    def test_remove_emails(self):
        """Test email removal"""
        text = "Contact me@example.com or support@test.org"
        cleaner = TextCleaner(text)
        result = cleaner.remove_emails().get_cleaned_text()
        
        assert "me@example.com" not in result
        assert "support@test.org" not in result
        assert "Contact" in result
    
    def test_remove_phone_numbers(self):
        """Test phone number removal"""
        text = "Call (555) 123-4567 or 555-987-6543"
        cleaner = TextCleaner(text)
        result = cleaner.remove_phone_numbers().get_cleaned_text()
        
        assert "555-123-4567" not in result
        assert "(555)" not in result
    
    def test_remove_numbers(self):
        """Test number removal"""
        text = "The price is 99.99 and quantity is 42"
        cleaner = TextCleaner(text)
        result = cleaner.remove_numbers().get_cleaned_text()
        
        assert "99.99" not in result
        assert "42" not in result
        assert "price" in result
    
    def test_remove_special_characters(self):
        """Test special character removal"""
        text = "Hello! @#$%^&*() World!!!"
        cleaner = TextCleaner(text)
        result = cleaner.remove_special_characters().get_cleaned_text()
        
        assert "@" not in result
        assert "#" not in result
        assert "!" not in result
        assert "Hello" in result
    
    def test_to_lowercase(self):
        """Test lowercase conversion"""
        text = "HELLO World"
        cleaner = TextCleaner(text)
        result = cleaner.to_lowercase().get_cleaned_text()
        
        assert result == "hello world"
    
    def test_to_uppercase(self):
        """Test uppercase conversion"""
        text = "hello world"
        cleaner = TextCleaner(text)
        result = cleaner.to_uppercase().get_cleaned_text()
        
        assert result == "HELLO WORLD"
    
    def test_normalize_whitespace(self):
        """Test whitespace normalization"""
        text = "Hello    world\n\n\twith   spaces"
        cleaner = TextCleaner(text)
        result = cleaner.normalize_whitespace().get_cleaned_text()
        
        assert "    " not in result
        assert "\n" not in result
        assert "\t" not in result
        assert result == "Hello world with spaces"
    
    def test_normalize_unicode(self):
        """Test unicode normalization"""
        text = "café résumé naïve"
        cleaner = TextCleaner(text)
        result = cleaner.normalize_unicode().get_cleaned_text()
        
        assert "café" not in result  # Should be converted
        assert "cafe" in result
    
    def test_method_chaining(self, sample_text):
        """Test that method chaining works"""
        cleaner = TextCleaner(sample_text)
        result = (cleaner
                 .remove_html_tags()
                 .remove_urls()
                 .remove_emails()
                 .normalize_whitespace()
                 .to_lowercase()
                 .get_cleaned_text())
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert len(result) < len(sample_text)
    
    def test_get_report(self, sample_text):
        """Test cleaning report generation"""
        cleaner = TextCleaner(sample_text)
        cleaner.remove_html_tags().remove_urls()
        report = cleaner.get_report()
        
        assert 'original_length' in report
        assert 'final_length' in report
        assert 'chars_removed' in report
        assert 'steps_applied' in report
        assert len(report['steps_applied']) == 2
    
    def test_reset(self, sample_text):
        """Test reset functionality"""
        cleaner = TextCleaner(sample_text)
        
        # Modify text
        cleaner.remove_html_tags().to_lowercase()
        modified = cleaner.get_cleaned_text()
        
        # Reset
        cleaner.reset()
        reset_text = cleaner.get_cleaned_text()
        
        assert reset_text == sample_text
        assert reset_text != modified