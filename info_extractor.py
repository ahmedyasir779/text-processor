"""
Information Extraction Module
Extract structured data from unstructured text
"""

import re
from typing import List, Dict, Optional
from datetime import datetime


class InfoExtractor:

    def __init__(self, text: str):
        self.text = text
        
        # Pre-compiled patterns (faster)
        self.patterns = {
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'url': re.compile(r'https?://[^\s]+'),
            'phone_intl': re.compile(r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'),
            'phone_us': re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'),
            'date_slash': re.compile(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b'),
            'date_dash': re.compile(r'\b\d{4}-\d{2}-\d{2}\b'),
            'time_24h': re.compile(r'\b([01]?[0-9]|2[0-3]):[0-5][0-9]\b'),
            'time_12h': re.compile(r'\b\d{1,2}:[0-5][0-9]\s*(?:AM|PM|am|pm)\b'),
            'currency_usd': re.compile(r'\$\d+(?:,\d{3})*(?:\.\d{2})?'),
            'currency_sar': re.compile(r'(?:SAR|SR)\s*\d+(?:,\d{3})*(?:\.\d{2})?'),
            'hashtag': re.compile(r'#\w+'),
            'mention': re.compile(r'@\w+'),
            'credit_card': re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
            'zip_code': re.compile(r'\b\d{5}(?:-\d{4})?\b'),
            'ipv4': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
        }
    
    def extract_emails(self) -> List[str]:
        return self.patterns['email'].findall(self.text)
    
    def extract_urls(self) -> List[str]:
        return self.patterns['url'].findall(self.text)
    
    def extract_phones(self) -> List[str]:
        phones = []
        phones.extend(self.patterns['phone_intl'].findall(self.text))
        phones.extend(self.patterns['phone_us'].findall(self.text))
        return list(set(phones))  # Remove duplicates
    
    def extract_dates(self) -> List[str]:
        dates = []
        dates.extend(self.patterns['date_slash'].findall(self.text))
        dates.extend(self.patterns['date_dash'].findall(self.text))
        return dates
    
    def extract_times(self) -> List[str]:
        times = []
        times.extend(self.patterns['time_24h'].findall(self.text))
        times.extend(self.patterns['time_12h'].findall(self.text))
        return times
    
    def extract_currency(self) -> List[str]:
        amounts = []
        amounts.extend(self.patterns['currency_usd'].findall(self.text))
        amounts.extend(self.patterns['currency_sar'].findall(self.text))
        return amounts
    
    def extract_hashtags(self) -> List[str]:
        return self.patterns['hashtag'].findall(self.text)
    
    def extract_mentions(self) -> List[str]:
        return self.patterns['mention'].findall(self.text)
    
    def extract_credit_cards(self) -> List[str]:
        cards = self.patterns['credit_card'].findall(self.text)
        # Mask for security: show only last 4 digits
        masked = [f"****-****-****-{card[-4:]}" for card in cards]
        return masked
    
    def extract_ip_addresses(self) -> List[str]:
        return self.patterns['ipv4'].findall(self.text)
    
    def extract_custom_pattern(self, pattern: str, flags=0) -> List[str]:
        regex = re.compile(pattern, flags)
        return regex.findall(self.text)
    
    def extract_all(self) -> Dict:
        return {
            'emails': self.extract_emails(),
            'urls': self.extract_urls(),
            'phones': self.extract_phones(),
            'dates': self.extract_dates(),
            'times': self.extract_times(),
            'currency': self.extract_currency(),
            'hashtags': self.extract_hashtags(),
            'mentions': self.extract_mentions(),
            'credit_cards': self.extract_credit_cards(),
            'ip_addresses': self.extract_ip_addresses(),
        }
    
    def get_summary(self) -> str:
        all_info = self.extract_all()
        
        summary = []
        summary.append("INFORMATION EXTRACTION SUMMARY")
        summary.append("=" * 60)
        
        for info_type, items in all_info.items():
            if items:
                summary.append(f"\n{info_type.upper().replace('_', ' ')} ({len(items)}):")
                for item in items[:5]:  # Show first 5
                    summary.append(f"  - {item}")
                if len(items) > 5:
                    summary.append(f"  ... and {len(items) - 5} more")
        
        return '\n'.join(summary)

