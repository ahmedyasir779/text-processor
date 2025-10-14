import re
from typing import List, Dict, Tuple
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter

class SentimentAnalyzer:
    def __init__(self):
        # Initialize VADER
        self.vader = SentimentIntensityAnalyzer()

        # Emotion keywords (expanded lexicon)
        self.emotion_keywords = {
            'joy': ['happy', 'joy', 'excited', 'wonderful', 'amazing', 'fantastic', 
                   'delighted', 'pleased', 'thrilled', 'awesome', 'love', 'excellent',
                   '😊', '😄', '😃', '🎉', '❤️', '💖'],
            
            'sadness': ['sad', 'unhappy', 'disappointed', 'sorry', 'depressed', 
                       'terrible', 'awful', 'horrible', 'unfortunate', 'regret',
                       '😢', '😭', '😞', '💔'],
            
            'anger': ['angry', 'mad', 'furious', 'annoyed', 'irritated', 'frustrated',
                     'outraged', 'hate', 'disgusted', 'rage', 'worst',
                     '😡', '😠', '🤬'],
            
            'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'terrified',
                    'frightened', 'concern', 'panic', 'alarmed',
                    '😨', '😰', '😱'],
            
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'unexpected',
                        'wow', 'omg', 'incredible', 'unbelievable',
                        '😲', '😮', '🤯'],
            
            'trust': ['trust', 'reliable', 'honest', 'genuine', 'authentic', 'sincere',
                     'confident', 'believe', 'faith'],
            
            'anticipation': ['excited', 'eager', 'looking forward', 'anticipate', 
                           'hopeful', 'expecting', 'can\'t wait']
        }

        # Negation words (flip sentiment)
        self.negations = ['not', 'no', 'never', 'neither', 'nobody', 'nothing', 
                         'nowhere', 'hardly', 'barely', 'scarcely', 'n\'t']
        
        # Intensifiers (strengthen sentiment)
        self.intensifiers = ['very', 'extremely', 'really', 'absolutely', 'totally',
                            'completely', 'utterly', 'highly', 'so', 'too']
        

    def analyze_sentiment(self, text: str) -> Dict:
        # Get VADER scores
        scores = self.vader.polarity_scores(text)

        # Classify based on compound score
        if scores['compound'] >= 0.05:
            classification = 'positive'
            emoji = '😊'
        elif scores['compound'] <= -0.05:
            classification = 'negative'
            emoji = '😢'
        else:
            classification = 'neutral'
            emoji = '😐'

        # Determine intensity
        abs_score = abs(scores['compound'])
        if abs_score >= 0.7:
            intensity = 'strong'
        elif abs_score >= 0.4:
            intensity = 'moderate'
        else:
            intensity = 'weak'

        return {
            'classification': classification,
            'emoji': emoji,
            'intensity': intensity,
            'scores': {
                'compound': round(scores['compound'], 3),
                'positive': round(scores['pos'], 3),
                'negative': round(scores['neg'], 3),
                'neutral': round(scores['neu'], 3)
            }
        }

    def detect_emotions(self, text: str) -> Dict[str, float]:
        text_lower = text.lower()
        emotion_scores = {}

        for emotion, keywords in self.emotion_keywords.items():
            # Count how many keywords found
            count = sum(1 for keyword in keywords if keyword in text_lower)

            # Calculate score (normalized by number of words)
            words = text_lower.split()
            score = count / len(words) if words else 0

            # Store if above threshold
            if score > 0:
                emotion_scores[emotion] = round(score * 10, 2) # Scale up for readability

        # Sort by score
        return dict(sorted(emotion_scores.items(),
                           key=lambda x: x[1],
                           reverse=True))
    

    def extract_opinions(self, text: str) -> List[Dict]:

        # Opinion indicators
        opinion_patterns = [
            r'I think (.*?)[.!?]',
            r'I believe (.*?)[.!?]',
            r'I feel (.*?)[.!?]',
            r'In my opinion, (.*?)[.!?]',
            r'I would say (.*?)[.!?]',
            r'It seems (.*?)[.!?]',
            r'I consider (.*?)[.!?]',
        ]

        opinions = []
        for pattern in opinion_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)

            for match in matches:
                opinion_text = match.group(0)
                sentiment = self.analyze_sentiment(opinion_text)
                
                opinions.append({
                    'text': opinion_text,
                    'sentiment': sentiment['classification'],
                    'score': sentiment['scores']['compound']
                })
        
        return opinions
            
    def analyze_aspects(self, text: str, aspects: List[str]) -> Dict[str, Dict]:
        text_lower = text.lower()
        results = {}
        
        for aspect in aspects:
            # Find sentences mentioning this aspect
            sentences = [s for s in text.split('.') 
                        if aspect.lower() in s.lower()]
            
            if sentences:
                # Analyze sentiment of these sentences
                combined = '. '.join(sentences)
                sentiment = self.analyze_sentiment(combined)
                results[aspect] = sentiment
            else:
                results[aspect] = {
                    'classification': 'not_mentioned',
                    'scores': {'compound': 0}
                }
        
        return results
    
    def get_subjectivity(self, text: str) -> float:
        text_lower = text.lower()
        
        # Subjective indicators
        subjective_words = ['i', 'me', 'my', 'feel', 'think', 'believe', 
                           'love', 'hate', 'amazing', 'terrible']
        
        # Count subjective words
        words = text_lower.split()
        subjective_count = sum(1 for word in words if word in subjective_words)
        
        # Add emoji weight
        emoji_count = len(re.findall(r'[😀-🙏]', text))
        
        # Calculate score
        total_indicators = subjective_count + emoji_count
        score = min(total_indicators / len(words), 1.0) if words else 0
        
        return round(score, 3)
    
    def compare_texts(self, text1: str, text2: str) -> Dict:
        sent1 = self.analyze_sentiment(text1)
        sent2 = self.analyze_sentiment(text2)
        
        # Calculate difference
        diff = sent1['scores']['compound'] - sent2['scores']['compound']
        
        if diff > 0.1:
            comparison = "Text 1 is more positive"
        elif diff < -0.1:
            comparison = "Text 2 is more positive"
        else:
            comparison = "Similar sentiment"
        
        return {
            'text1_sentiment': sent1,
            'text2_sentiment': sent2,
            'difference': round(diff, 3),
            'comparison': comparison
        }
    
    def batch_analyze(self, texts: List[str]) -> Dict:
        sentiments = [self.analyze_sentiment(text) for text in texts]
        
        # Count classifications
        classifications = [s['classification'] for s in sentiments]
        counts = Counter(classifications)
        
        # Average scores
        avg_compound = sum(s['scores']['compound'] for s in sentiments) / len(sentiments)
        
        return {
            'total_texts': len(texts),
            'positive_count': counts.get('positive', 0),
            'negative_count': counts.get('negative', 0),
            'neutral_count': counts.get('neutral', 0),
            'average_score': round(avg_compound, 3),
            'overall_sentiment': 'positive' if avg_compound > 0.05 else 
                               ('negative' if avg_compound < -0.05 else 'neutral')
        }

