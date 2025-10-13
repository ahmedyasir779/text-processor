"""
Download required NLTK data
Run this once to download necessary datasets
"""

import nltk

print("Downloading NLTK data...")

# Download required datasets
nltk.download('punkt')          # For tokenization
nltk.download('stopwords')      # For stop word removal
nltk.download('wordnet')        # For lemmatization
nltk.download('omw-1.4')        # Multilingual wordnet
nltk.download('averaged_perceptron_tagger')  # For POS tagging
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')


print("\n✓ All NLTK data downloaded successfully!")