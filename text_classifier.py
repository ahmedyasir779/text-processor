from typing import List, Dict, Tuple, Optional
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from collections import Counter


class TextClassifier:
    def __init__(self, algorithm: str = 'naive_bayes', vectorizer_type: str = 'tfidf', max_features: int = 5000):

        self.algorithm = algorithm
        self.vectorizer_type = vectorizer_type
        self.max_features = max_features

        # Initialize vectorizer
        if vectorizer_type == 'tfidf':
            self.vectorizer = TfidfVectorizer(
                    max_features=max_features,
                    ngram_range=(1,2), # Unigrams and bigrams
                    stop_words='english')
        else:
            self.vectorizer = CountVectorizer(
                    max_features=max_features,
                    ngram_range=(1,2),
                    stop_words='english')
                
        # Initialize model
        if algorithm == 'naive_bayes':
            self.model = MultinomialNB()
        elif algorithm == 'logistic_regression':
            self.model = LogisticRegression(max_iter=1000, random_state=42)
        elif algorithm == 'svm':
            self.model = LinearSVC(random_state=42)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        self.is_trained = False
        self.classes = None
    
    def train(self, texts: List[str], labels: List[str], 
              test_size: float = 0.2) -> Dict:
        print(f"Training {self.algorithm} classifier...")
        print(f"Total samples: {len(texts)}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, 
            test_size=test_size, 
            random_state=42,
            stratify=labels  # Maintain class distribution
        )
        
        print(f"Training samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")
        
        # Vectorize text
        print("\nVectorizing text...")
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        print(f"Features extracted: {X_train_vec.shape[1]}")
        
        # Train model
        print("\nTraining model...")
        self.model.fit(X_train_vec, y_train)
        self.is_trained = True
        self.classes = self.model.classes_
        
        # Evaluate on test set
        print("\nEvaluating...")
        y_pred = self.model.predict(X_test_vec)
        
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        print(f"\n Training complete!")
        print(f"Accuracy: {accuracy:.3f}")
        
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': conf_matrix,
            'test_predictions': list(zip(X_test[:5], y_test[:5], y_pred[:5]))
        }
    
    def predict(self, texts: List[str]) -> List[str]:
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        # Vectorize
        X_vec = self.vectorizer.transform(texts)
        
        # Predict
        predictions = self.model.predict(X_vec)
        
        return predictions.tolist()
    
    def predict_proba(self, texts: List[str]) -> List[Dict[str, float]]:
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        # Check if model supports probability prediction
        if not hasattr(self.model, 'predict_proba'):
            raise ValueError(f"{self.algorithm} doesn't support probability prediction")
        
        # Vectorize
        X_vec = self.vectorizer.transform(texts)
        
        # Predict probabilities
        probas = self.model.predict_proba(X_vec)
        
        # Convert to list of dicts
        results = []
        for proba in probas:
            prob_dict = {
                class_name: float(prob)
                for class_name, prob in zip(self.classes, proba)
            }
            results.append(prob_dict)
        
        return results
    
    def get_top_features(self, label: str, n: int = 10) -> List[Tuple[str, float]]:
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        # Get feature names
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get class index
        class_idx = list(self.classes).index(label)
        
        # Get feature importance (different for each algorithm)
        if self.algorithm == 'naive_bayes':
            # For Naive Bayes, use log probabilities
            importances = self.model.feature_log_prob_[class_idx]
        elif self.algorithm == 'logistic_regression':
            # For Logistic Regression, use coefficients
            if len(self.classes) == 2:
                importances = self.model.coef_[0]
            else:
                importances = self.model.coef_[class_idx]
        elif self.algorithm == 'svm':
            # For SVM, use coefficients
            if len(self.classes) == 2:
                importances = self.model.coef_[0]
            else:
                importances = self.model.coef_[class_idx]
        
        # Get top features
        top_indices = np.argsort(importances)[-n:][::-1]
        top_features = [
            (feature_names[i], float(importances[i]))
            for i in top_indices
        ]
        
        return top_features
    
    def save_model(self, filepath: str):
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        model_data = {
            'algorithm': self.algorithm,
            'vectorizer': self.vectorizer,
            'model': self.model,
            'classes': self.classes
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✓ Model saved to {filepath}")
    
    @classmethod
    def load_model(cls, filepath: str) -> 'TextClassifier':
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        classifier = cls(algorithm=model_data['algorithm'])
        classifier.vectorizer = model_data['vectorizer']
        classifier.model = model_data['model']
        classifier.classes = model_data['classes']
        classifier.is_trained = True
        
        print(f"✓ Model loaded from {filepath}")
        return classifier


# ============================================
# TESTING CODE
# ============================================

if __name__ == "__main__":
    print("=" * 70)
    print("TEXT CLASSIFIER - TEST")
    print("=" * 70)
    
    # Sample data: Topic classification
    texts = [
        # Sports
        "The team won the championship game yesterday",
        "Football match ended in a draw with 2-2 score",
        "Basketball player scored 30 points in the game",
        "Tennis tournament finals happening next week",
        "Cricket match postponed due to rain",
        "Olympic committee announces new qualifying rules",
        "Fans celebrate historic World Cup victory",
        "Injury forces star player to withdraw from tournament",
        "Coach praises team’s defense after tight win",
        "Formula 1 driver claims pole position in qualifying",
        
        # Technology
        "New Python framework released for web development",
        "Machine learning model achieves 95% accuracy",
        "Smartphone update includes new AI features",
        "Cloud computing services expanding rapidly",
        "Cybersecurity threats increasing worldwide",
        "Quantum computing breakthrough promises faster encryption",
        "Tech giants invest heavily in renewable energy data centers",
        "New laptop features faster chips and longer battery life",
        "VR headset offers ultra-realistic experience",
        "AI chatbot revolutionizes customer service industry",
        
        # Business
        "Stock market hits record high today",
        "Company announces quarterly earnings report",
        "Startup raises 10 million in funding",
        "CEO resigns after scandal",
        "New merger between tech companies announced",
        "Investors optimistic about economic recovery",
        "Oil prices rise amid supply concerns",
        "Retail giant expands into new international markets",
        "Real estate sector shows signs of slowdown",
        "Cryptocurrency exchange faces regulatory pressure",
        
        # Health
        "New vaccine shows promising results in trials",
        "Study reveals benefits of regular exercise",
        "Hospital introduces advanced surgical technique",
        "Mental health awareness campaign launched",
        "Nutrition experts recommend balanced diet",
        "Doctors warn about rise in diabetes cases",
        "New cancer treatment approved by authorities",
        "Research links sleep quality to heart health",
        "Fitness trackers help users maintain daily goals",
        "Public health officials monitor flu outbreak",
    ]

    
    labels = (
        ['sports'] * 10 + 
        ['technology'] * 10 + 
        ['business'] * 10 + 
        ['health'] * 10
    )
    
    print(f"\n Training data: {len(texts)} documents")
    print(f" Classes: {set(labels)}")
    
    # Test 1: Train classifier
    print("\n" + "=" * 70)
    print(" TRAINING CLASSIFIER")
    print("=" * 70)
    
    classifier = TextClassifier(
        algorithm='naive_bayes',
        vectorizer_type='tfidf'
    )
    
    results = classifier.train(texts, labels, test_size=0.25)
    
    print(f"\n Results:")
    print(f"Accuracy: {results['accuracy']:.3f}")
    
    print(f"\n Sample predictions:")
    for text, true_label, pred_label in results['test_predictions']:
        match = "✓" if true_label == pred_label else "✗"
        print(f"{match} Text: {text[:50]}...")
        print(f"  True: {true_label}, Predicted: {pred_label}")
    
    # Test 2: Predict new texts
    print("\n\n" + "=" * 70)
    print(" PREDICTING NEW TEXTS")
    print("=" * 70)
    
    new_texts = [
        "The soccer team scored three goals",
        "Python programming tutorial for beginners",
        "Company stock price increased by 10 percent",
        "Doctor recommends daily vitamins",
    ]
    
    predictions = classifier.predict(new_texts)
    
    for text, prediction in zip(new_texts, predictions):
        print(f"\nText: {text}")
        print(f"Predicted category: {prediction.upper()}")
    
    # Test 3: Prediction probabilities
    print("\n\n" + "=" * 70)
    print(" PREDICTION PROBABILITIES")
    print("=" * 70)
    
    probabilities = classifier.predict_proba(new_texts[:2])
    
    for text, probs in zip(new_texts[:2], probabilities):
        print(f"\nText: {text}")
        print("Probabilities:")
        for category, prob in sorted(probs.items(), 
                                     key=lambda x: x[1], 
                                     reverse=True):
            print(f"  {category}: {prob:.3f}")
    
    # Test 4: Top features per class
    print("\n\n" + "=" * 70)
    print(" TOP FEATURES PER CLASS")
    print("=" * 70)
    
    for label in classifier.classes:
        print(f"\n{label.upper()}:")
        top_features = classifier.get_top_features(label, n=5)
        for feature, importance in top_features:
            print(f"  {feature}: {importance:.3f}")
    
    # Test 5: Save and load model
    print("\n\n" + "=" * 70)
    print(" SAVE AND LOAD MODEL")
    print("=" * 70)
    
    # Save
    classifier.save_model('models/text_classifier.pkl')
    
    # Load
    loaded_classifier = TextClassifier.load_model('models/text_classifier.pkl')
    
    # Test loaded model
    test_text = ["Football game scheduled for tomorrow"]
    prediction = loaded_classifier.predict(test_text)
    print(f"\nTest with loaded model:")
    print(f"Text: {test_text[0]}")
    print(f"Prediction: {prediction[0]}")
    
    print("\n" + "=" * 70)
    print(" ALL TESTS COMPLETE!")
    print("=" * 70)