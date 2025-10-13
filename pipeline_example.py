from text_cleaner import TextCleaner
from text_processor import TextProcessor


messy_text = """
<h1>Product Review</h1>
Check out https://example.com for details!
Email: info@example.com

The products are running smoothly. Better performance than expected!
Cats and dogs are jumping everywhere. 😺🐕

Call us: (555) 123-4567
"""

print("COMPLETE PIPELINE: CLEAN -> PROCESS")
print("=" * 60)

print("\n STEP 1: CLEANING...")
cleaner = TextCleaner(messy_text)
clean_text = (cleaner
              .remove_html_tags()
              .remove_urls()
              .remove_emails()
              .remove_phone_numbers()
              .remove_special_characters()
              .normalize_whitespace()
              .get_cleaned_text())

print(f"Original length: {len(messy_text)} chars")
print(f"Cleaned length: {len(clean_text)} chars")
print(f"\nCleaned text:\n{clean_text}")

print("\n STEP 2: PROCESSING...")
processor = TextProcessor(clean_text)

# Tokenization
tokens = processor.tokenize_words()
print(f"\n Tokens: {tokens}")

# Remove stopwords
filtered = processor.remove_stopwords(tokens)
print(f"\n Filtered (no stopwords): {filtered}")

# Lemmatization
lemmatized = processor.lemmatize_words(filtered)
print(f"\n Lemmatized: {lemmatized}")

# Get frequency
freq = processor.get_word_frequency(lemmatized)
print(f"\n Word frequency:")
for word, count in list(freq.items())[:5]:
    print(f"  {word}: {count}")

# extract key words
print(f"\n Nouns: {processor.extract_nouns()}")
print(f"\n Verbs: {processor.extract_verbs()}")
print(f"\n Adjectives: {processor.extract_adjectives()}")

# Statistics
stats = processor.get_statistics()
print(f"\n Statistics")
print(f"\n Total words: {stats['total_words']}")
print(f"\n Unique words: {stats['unique_words']}")
print(f"\n Lexical diversity: {stats['lexical_diversity']}")

print("\n" + "=" * 60)
print(" Pipeline complete.")