"""
Unit tests for InfoExtractor module
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from info_extractor import InfoExtractor


class TestInfoExtractor:
    """Test suite for InfoExtractor class"""
    
    @pytest.fixture
    def sample_text(self):
        """Create sample text with various information"""
        return """
        Contact: john@example.com or support@test.org
        Call: (555) 123-4567 or +1-800-555-0199
        Visit: https://example.com and www.test.com
        Date: 12/31/2023 or 2024-01-15
        Time: 14:30 or 3:45 PM
        Price: $99.99 or SAR 375.50
        #Python #MachineLearning @username
        IP: 192.168.1.1
        """
    
    def test_initialization(self, sample_text):
        """Test InfoExtractor initialization"""
        extractor = InfoExtractor(sample_text)
        
        assert extractor.text == sample_text
        assert len(extractor.patterns) > 0
    
    def test_extract_emails(self, sample_text):
        """Test email extraction"""
        extractor = InfoExtractor(sample_text)
        emails = extractor.extract_emails()
        
        assert len(emails) >= 2
        assert "john@example.com" in emails
        assert "support@test.org" in emails
    
    def test_extract_urls(self, sample_text):
        """Test URL extraction"""
        extractor = InfoExtractor(sample_text)
        urls = extractor.extract_urls()
        
        assert len(urls) >= 1
        assert any("https://example.com" in url for url in urls)
    
    def test_extract_phones(self, sample_text):
        """Test phone number extraction"""
        extractor = InfoExtractor(sample_text)
        phones = extractor.extract_phones()
        
        assert len(phones) >= 1
    
    def test_extract_dates(self, sample_text):
        """Test date extraction"""
        extractor = InfoExtractor(sample_text)
        dates = extractor.extract_dates()
        
        assert len(dates) >= 2
        assert "12/31/2023" in dates
        assert "2024-01-15" in dates
    
    def test_extract_times(self, sample_text):
        """Test time extraction"""
        extractor = InfoExtractor(sample_text)
        times = extractor.extract_times()
        
        assert len(times) >= 1
    
    def test_extract_currency(self, sample_text):
        """Test currency extraction"""
        extractor = InfoExtractor(sample_text)
        currency = extractor.extract_currency()
        
        assert len(currency) >= 2
        assert "$99.99" in currency
    
    def test_extract_hashtags(self, sample_text):
        """Test hashtag extraction"""
        extractor = InfoExtractor(sample_text)
        hashtags = extractor.extract_hashtags()
        
        assert len(hashtags) >= 2
        assert "#Python" in hashtags
        assert "#MachineLearning" in hashtags
    
    def test_extract_mentions(self, sample_text):
        """Test mention extraction"""
        extractor = InfoExtractor(sample_text)
        mentions = extractor.extract_mentions()
        
        assert len(mentions) >= 1
        assert "@username" in mentions
    
    def test_extract_ip_addresses(self, sample_text):
        """Test IP address extraction"""
        extractor = InfoExtractor(sample_text)
        ips = extractor.extract_ip_addresses()
        
        assert len(ips) >= 1
        assert "192.168.1.1" in ips
    
    def test_extract_all(self, sample_text):
        """Test extracting all information types"""
        extractor = InfoExtractor(sample_text)
        all_info = extractor.extract_all()
        
        assert isinstance(all_info, dict)
        assert 'emails' in all_info
        assert 'urls' in all_info
        assert 'phones' in all_info
        assert 'dates' in all_info
        
        # Check that at least some info was found
        total_found = sum(len(v) for v in all_info.values())
        assert total_found > 0
    
    def test_extract_custom_pattern(self):
        """Test custom pattern extraction"""
        text = "Invoice: INV-12345, INV-67890"
        extractor = InfoExtractor(text)
        
        pattern = r'INV-\d{5}'
        invoices = extractor.extract_custom_pattern(pattern)
        
        assert len(invoices) == 2
        assert "INV-12345" in invoices
        assert "INV-67890" in invoices
    
    def test_get_summary(self, sample_text):
        """Test summary generation"""
        extractor = InfoExtractor(sample_text)
        summary = extractor.get_summary()
        
        assert isinstance(summary, str)
        assert "INFORMATION EXTRACTION SUMMARY" in summary
        assert len(summary) > 0