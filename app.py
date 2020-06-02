
from flask import Flask,request, url_for, redirect, render_template
import pickle

#import libraries to generate tweet
import tweepy as tw
import pandas as pd

app = Flask(__name__)

model = pickle.load(open('finalmodel.pickle','rb'))

@app.route('/')
def index():
    return render_template('index.html')
    #return 'Deployed Okay!'


@app.route('/predict',methods=['POST'])
def predict():
  
    if request.method =='POST':
        newDate = request.form["date"]

        #defining variables to store twitter credentials
        consumer_key= '1CSlpVY7BhyKLnvaAJu2jjdZ9'
        consumer_secret= 'vlYHeU3WDhWEB5CIAvHyd9LCUry2mpxlhG5OZIlzobRaJIWej1'
        access_token= '1194870598175842304-OzdBXRJcsWK2Lh3xPC9Fxw4it0fidw'
        access_token_secret= 'zFHc6KvHmDq3NZ4uCk77PqlQwqGDbfJno5wAzQ50CdQYg'

        #connecting to twitter api using credentials
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tw.API(auth, wait_on_rate_limit=True)

        search_words = "#hiv/aids"

        #generate tweet based on date entered by user
        tweets = tw.Cursor(api.search,q=search_words,lang="en",since=newDate,tweet_mode='extended').items(1)
        #get tweet text
        for tweet_info in tweets:
            if "retweeted_status" in dir(tweet_info):
                sample = tweet_info.retweeted_status.full_text

            else:
                sample = tweet_info.full_text

        #return render_template('index.html', text = sample)

      
        pred  = model.predict([sample])
        if pred == 1:
            return render_template("index.html",prediction = "Prediction : This tweet is HIV related")
        elif pred == 2:
            return render_template("index.html",prediction = "Prediction : This tweet is not related to HIV")
            
        



if __name__ == "__main__":
    app.run()
