import re
from typing import List, Dict, Optional
from unidecode import unidecode

class TextCleaner:
    def __init__(self,  text: str):
        self.original_text = text
        self.text = text
        self.cleaning_steps = []

    def remove_html_tags(self) -> 'TextCleaner':
        before = len(self.text)
        self.text = re.sub(r'<[^>]+>', '', self.text)
        after = len(self.text)
        
        self.cleaning_steps.append({
            'step': 'remove_html_tags',
            'chars_removed': before - after
        })
        
        return self
    
    def remove_urls(self) -> 'TextCleaner':
        
        before = len(self.text)
        # Remove http/https URLs
        self.text = re.sub(r'https?://\S+', '', self.text)
        # Remove www URLs
        self.text = re.sub(r'www\.\S+', '', self.text)
        after = len(self.text)
        
        self.cleaning_steps.append({
            'step': 'remove_urls',
            'chars_removed': before - after
        })
        
        return self
    
    def remove_emails(self) -> 'TextCleaner':

        before = len(self.text)
        self.text = re.sub(r'\S+@\S+', '', self.text)
        after = len(self.text)
        
        self.cleaning_steps.append({
            'step': 'remove_emails',
            'chars_removed': before - after
        })
        
        return self
    
    def remove_phone_numbers(self) -> 'TextCleaner':

        before = len(self.text)
        
        # Pattern 1: 555-1234 or 555-123-4567
        self.text = re.sub(r'\d{3}[-.]?\d{3}[-.]?\d{4}', '', self.text)
        
        # Pattern 2: (555) 123-4567
        self.text = re.sub(r'\(\d{3}\)\s*\d{3}[-.]?\d{4}', '', self.text)
        
        after = len(self.text)
        
        self.cleaning_steps.append({
            'step': 'remove_phone_numbers',
            'chars_removed': before - after
        })
        
        return self
    
    def remove_numbers(self) -> 'TextCleaner':

        before = len(self.text)
        self.text = re.sub(r'\d+\.?\d*', '', self.text)
        after = len(self.text)
        
        self.cleaning_steps.append({
            'step': 'remove_numbers',
            'chars_removed': before - after
        })
        
        return self
    
    def remove_special_characters(self, keep_spaces: bool = True) -> 'TextCleaner':

        before = len(self.text)
        
        if keep_spaces:
            # Keep letters, numbers, and spaces
            self.text = re.sub(r'[^a-zA-Z0-9\s]', '', self.text)
        else:
            # Keep only letters and numbers
            self.text = re.sub(r'[^a-zA-Z0-9]', '', self.text)
        
        after = len(self.text)
        
        self.cleaning_steps.append({
            'step': 'remove_special_characters',
            'chars_removed': before - after
        })
        
        return self
    
    def to_lowercase(self) -> 'TextCleaner':

        self.text = self.text.lower()
        
        self.cleaning_steps.append({
            'step': 'to_lowercase',
            'chars_removed': 0
        })
        
        return self
    
    def to_uppercase(self) -> 'TextCleaner':

        self.text = self.text.upper()
        
        self.cleaning_steps.append({
            'step': 'to_uppercase',
            'chars_removed': 0
        })
        
        return self
    
    def normalize_whitespace(self) -> 'TextCleaner':

        before = len(self.text)
        
        # Replace tabs and newlines with spaces
        self.text = self.text.replace('\t', ' ').replace('\n', ' ')
        
        # Multiple spaces -> single space
        self.text = re.sub(r'\s+', ' ', self.text)
        
        # Strip leading/trailing whitespace
        self.text = self.text.strip()
        
        after = len(self.text)
        
        self.cleaning_steps.append({
            'step': 'normalize_whitespace',
            'chars_removed': before - after
        })
        
        return self
    
    def normalize_unicode(self) -> 'TextCleaner':

        before = len(self.text)
        self.text = unidecode(self.text)
        after = len(self.text)
        
        self.cleaning_steps.append({
            'step': 'normalize_unicode',
            'chars_removed': before - after
        })
        
        return self
    
    def remove_extra_spaces(self) -> 'TextCleaner':

        before = len(self.text)
        self.text = ' '.join(self.text.split())
        after = len(self.text)
        
        self.cleaning_steps.append({
            'step': 'remove_extra_spaces',
            'chars_removed': before - after
        })
        
        return self
    
    def get_cleaned_text(self) -> str:

        return self.text
    
    def get_report(self) -> Dict:

        return {
            'original_length': len(self.original_text),
            'final_length': len(self.text),
            'chars_removed': len(self.original_text) - len(self.text),
            'steps_applied': self.cleaning_steps
        }
    
    def reset(self) -> 'TextCleaner':

        self.text = self.original_text
        self.cleaning_steps = []
        return self


if __name__ == "__main__":
    print("TESTING WITH FILE")
    print("=" * 60)

    with open('data/sample_text.txt', 'r') as f:
        file_text = f.read()

    cleaner2 = TextCleaner(file_text)
    cleaned2 = (cleaner2
                .remove_html_tags()
                .remove_urls()
                .remove_emails()
                .remove_phone_numbers()
                .remove_numbers()
                .remove_special_characters()
                .normalize_whitespace()
                .to_lowercase()
                .get_cleaned_text())

    print("\nCleaned file text:")
    print(cleaned2)