from flask import Flask, request, render_template
from sentiment_classifier import SentimentClassifier
import time

app = Flask(__name__)

print("Preparing classifier")
start_time = time.time()
classifier = SentimentClassifier()
print("Classifier is ready")
print(time.time() - start_time, "seconds")

@app.route("/")
def index():
    return render_template('info.html') 

@app.route('/info')
def info(name=None):
    return render_template('info.html') 

@app.route('/demo', methods = ['GET', 'POST'])
def demo(text="", prediction_message=""):
    if request.method == "POST":
        text = request.form["text"]
        prediction_message = classifier.get_prediction_message(text)
    return render_template('demo.html', text=text, prediction_message=prediction_message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)