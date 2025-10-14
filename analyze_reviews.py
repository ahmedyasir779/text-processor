from sentiment_analyzer import SentimentAnalyzer

# Sample product reviews
reviews = [
    "This laptop is amazing! Fast performance and great build quality. Battery lasts all day. Highly recommend! 😊",
    
    "Disappointed with this purchase. The price is way too high for what you get. Customer service was unhelpful.",
    
    "Pretty good laptop. Performance is decent but battery life could be better. For the price, it's okay.",
    
    "TERRIBLE! Stopped working after 2 months. Worst purchase ever. Don't waste your money! 😡",
    
    "Love everything about it! The quality is excellent, price is fair, and shipping was fast. 5 stars! ⭐⭐⭐⭐⭐",
]

print("=" * 70)
print("PRODUCT REVIEW ANALYSIS")
print("=" * 70)

analyzer = SentimentAnalyzer()

# Analyze each review
print("\n INDIVIDUAL REVIEWS:\n")
for i, review in enumerate(reviews, 1):
    sentiment = analyzer.analyze_sentiment(review)
    emotions = analyzer.detect_emotions(review)
    
    print(f"{i}. Review: {review[:60]}...")
    print(f"   Sentiment: {sentiment['classification'].upper()} {sentiment['emoji']}")
    print(f"   Score: {sentiment['scores']['compound']}")
    if emotions:
        top_emotion = list(emotions.keys())[0]
        print(f"   Top emotion: {top_emotion}")
    print()

# Batch analysis
print("\n OVERALL STATISTICS:\n")
batch_results = analyzer.batch_analyze(reviews)
print(f"Total reviews: {batch_results['total_texts']}")
print(f"Positive: {batch_results['positive_count']} ({batch_results['positive_count']/batch_results['total_texts']*100:.0f}%)")
print(f"Neutral: {batch_results['neutral_count']} ({batch_results['neutral_count']/batch_results['total_texts']*100:.0f}%)")
print(f"Negative: {batch_results['negative_count']} ({batch_results['negative_count']/batch_results['total_texts']*100:.0f}%)")
print(f"\nOverall sentiment: {batch_results['overall_sentiment'].upper()}")
print(f"Average score: {batch_results['average_score']}")

# Aspect analysis (combine all reviews)
print("\n\n ASPECT ANALYSIS (across all reviews):\n")
all_text = " ".join(reviews)
aspects = ['quality', 'price', 'battery', 'service', 'performance']
aspect_results = analyzer.analyze_aspects(all_text, aspects)

for aspect, sentiment in aspect_results.items():
    if sentiment['classification'] != 'not_mentioned':
        print(f"{aspect.capitalize()}: {sentiment['classification']} "
              f"(score: {sentiment['scores']['compound']:.2f})")
    else:
        print(f"{aspect.capitalize()}: Not mentioned")

print("\n" + "=" * 70)