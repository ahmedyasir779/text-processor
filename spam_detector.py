from text_classifier import TextClassifier

# Sample spam/ham data
texts = [
    # Spam (38 total)
    "Congratulations! You've won $1000! Click here now!",
    "URGENT: Your account will be closed. Verify immediately!",
    "Get rich quick! Make $5000 per week working from home!",
    "FREE iPhone! Limited time offer! Act now!!!",
    "You have been selected for a special prize. Claim now!",
    "Lose 30 pounds in 30 days! Magic pills! Order today!",
    "Hot singles in your area want to meet you!",
    "Your package is waiting. Pay $50 shipping fee.",
    "Limited-time offer! Get your discount before midnight!",
    "Claim your free vacation today! Only 5 spots left!",
    "Your loan has been approved! Click to confirm details!",
    "Exclusive deal: Buy one, get one free on all products!",
    "Congratulations, you’re our lucky customer this week!",
    "Earn money while you sleep — no experience needed!",
    "You’ve been chosen to receive a free gift card!",
    "Investment opportunity with guaranteed returns!",
    "Win a car just by completing this short survey!",
    "Click here to fix your computer immediately!",
    "Special promotion ends today — don’t miss out!",
    "Your account has unusual activity, confirm here!",
    "Unlock your full potential with our secret method!",
    "Act now to secure your prize before it expires!",
    "This is your final notice! Claim your refund now!",
    "Instant approval for credit card — apply today!",
    "Access premium content free for 7 days!",
    "Update your billing info to avoid service interruption!",
    "Huge savings! 90% off clearance sale today only!",
    "Congratulations! You qualified for a home loan!",
    "Final reminder: Your reward is waiting!",
    "Get followers instantly — 100% real people!",
    "Boost your income with our easy side hustle!",
    "Limited seats for exclusive online seminar — join now!",
    "Double your money in 10 days — guaranteed!",
    "Free streaming subscription for first 100 signups!",
    "Re: Unpaid invoice — click here to settle now!",
    "Lottery results are in — check if you’re the winner!",
    "Your parcel delivery failed — click to reschedule!",
    "Upgrade your phone plan for free today!",
    "Exclusive insider stock tips — subscribe now!",

    # Ham (38 total)
    "Meeting scheduled for tomorrow at 3pm",
    "Can you send me the report by Friday?",
    "Thanks for your help with the project",
    "Reminder: team lunch on Thursday",
    "Please review the attached document",
    "How was your weekend?",
    "Let's catch up for coffee sometime",
    "The presentation went well yesterday",
    "Don’t forget to submit your timesheet today",
    "Let’s move our meeting to next Monday",
    "Can you confirm attendance for the workshop?",
    "I’ve uploaded the final version of the slides",
    "Happy birthday! Wishing you a great day",
    "Let me know if you need help with the code",
    "Please approve the budget request by end of day",
    "The client meeting went smoothly this morning",
    "I’ll be working from home tomorrow",
    "Do you want to join for lunch later?",
    "Check the shared folder for the updated document",
    "We’re planning a small farewell party on Friday",
    "Just a reminder: deadline is next Tuesday",
    "Can you book a conference room for 2pm?",
    "Your package has been delivered successfully",
    "Let’s finalize the project plan this week",
    "The new intern starts next Monday",
    "I’ll call you once the task is completed",
    "Meeting notes are available on the shared drive",
    "Please resend the attachment, it didn’t go through",
    "Coffee break at 4pm?",
    "Looking forward to our discussion tomorrow",
    "The system maintenance is scheduled for tonight",
    "Let’s review the progress in our next meeting",
    "Please find the invoice attached",
    "Can you update the client on our status?",
    "I’ll handle the deployment this afternoon",
    "Thank you for your quick response",
    "Hope you’re doing well",
    "See you at the office tomorrow morning",
    "Reminder: submit your performance review today",
]

labels = ['spam'] * 39 + ['ham'] * 39

print("=" * 70)
print("SPAM DETECTION CLASSIFIER")
print("=" * 70)

# Train classifier
classifier = TextClassifier(
    algorithm='logistic_regression',
    vectorizer_type='tfidf'
)

print("\n Training spam detector...")
results = classifier.train(texts, labels, test_size=0.3)

print(f"\n Accuracy: {results['accuracy']:.1%}")

# Test on new emails
print("\n\n TESTING NEW EMAILS:")
print("=" * 70)

test_emails = [
    "Congratulations! You won a lottery! Send your details now!",
    "Can we reschedule our meeting to next week?",
    "URGENT!!! Click here to claim your prize!!!",
    "Thanks for the information. I'll review it tonight.",
    "FREE MONEY! No strings attached! Click now!!!",
]

predictions = classifier.predict(test_emails)
probabilities = classifier.predict_proba(test_emails)

for email, prediction, probs in zip(test_emails, predictions, probabilities):
    spam_prob = probs.get('spam', 0)
    
    print(f"\n Email: {email}")
    print(f"   Classification: {prediction.upper()}")
    print(f"   Spam probability: {spam_prob:.1%}")
    
    if prediction == 'spam':
        print(f"     BLOCKED")
    else:
        print(f"    ALLOWED")

# Show spam indicators
print("\n\n SPAM INDICATORS:")
print("=" * 70)
print("Words that indicate spam:")
spam_features = classifier.get_top_features('spam', n=10)
for word, score in spam_features:
    print(f"  • {word}")

print("\n" + "=" * 70)