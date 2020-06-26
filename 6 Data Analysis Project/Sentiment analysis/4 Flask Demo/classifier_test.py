from sentiment_classifier import SentimentClassifier

clf = SentimentClassifier()

reviews = ['The phone is nice to use. The interface is intuitive.',
            'this phone doesnt include phone card calling.']
            
for review in reviews:
    print(review, ' - ', clf.get_prediction_message(review))