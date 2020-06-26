import pickle

class SentimentClassifier(object):
    def __init__(self):
        self.pipe = pickle.load(open('model/pipe.pickle', 'rb'))
        self.classes_dict = {0: "negative", 1: "positive", -1: "prediction error"}

    def predict_text(self, text):
        try:
            return self.pipe.predict([text])[0]
        except:
            print("prediction error")
            return -1

    def predict_list(self, list_of_texts):
        try:
            return self.pipe.predict(list_of_texts)
        except:
            print('prediction error')
            return None

    def get_prediction_message(self, text):
        prediction = self.predict_text(text)
        return self.classes_dict[prediction]