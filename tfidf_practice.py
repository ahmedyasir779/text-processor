from sklearn.feature_extraction.text import TfidfVectorizer

# Sample documents
documents = [
    "Python is a programming language",
    "Machine learning is part of artificial intelligence",
    "Python is great for machine learning",
    "Java is also a programming language",
    "Deep learning is a subset of machine learning"
]

print("=" * 70)
print("TF-IDF FEATURE EXTRACTION - PRACTICE")


# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform documents
tfidf_matrix = vectorizer.fit_transform(documents)

# Get feature names (words)
feature_names = vectorizer.get_feature_names_out()

print(f"\n Documents: {len(documents)}")
print(f" Unique words (features): {len(feature_names)}")
print(f"\nFeature names: {feature_names}")

# Show TF-IDF scores for first document
print(f"\n\n TF-IDF scores for first document:")
print(f"Document: \"{documents[0]}\"")
print("\nWord → Score:")

doc_vector = tfidf_matrix[0].toarray()[0]
for word, score in zip(feature_names, doc_vector):
    if score > 0:
        print(f"  {word}: {score:.3f}")

# Compare two documents
print(f"\n\n Comparing documents:")
print(f"Doc 1: \"{documents[0]}\"")
print(f"Doc 3: \"{documents[2]}\"")
print("\nCommon words with high scores:")

doc1_vector = tfidf_matrix[0].toarray()[0]
doc3_vector = tfidf_matrix[2].toarray()[0]

for word, score1, score3 in zip(feature_names, doc1_vector, doc3_vector):
    if score1 > 0 and score3 > 0:
        print(f"  {word}: doc1={score1:.3f}, doc3={score3:.3f}")

print("\n" + "=" * 70)