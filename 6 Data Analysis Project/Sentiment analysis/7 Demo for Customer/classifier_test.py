from sentiment_classifier import SentimentClassifier

clf = SentimentClassifier()

reviews = ['Не рекомендую к покупке! Самый худший телефон на свете!',
            'Телефон интуитивно понятен. Памяти много. Хороший звук.']
            
for review in reviews:
    print(review, ' - ', clf.get_prediction_message(review))