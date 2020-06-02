#importing flask libraries
from flask_ngrok import run_with_ngrok
from flask import Flask,request, url_for, redirect, render_template
import pickle

#import libraries to generate tweet
import os
import tweepy as tw
import pandas as pd


app = Flask(__name__)
run_with_ngrok(app)


@app.route('/')
def index():
  return render_template('final.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    #function to predict the input tweet

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
                textTweet = tweet_info.retweeted_status.full_text
            else:
                textTweet = tweet_info.full_text

       
        model = pickle.load(open('drive/My Drive/Colab Notebooks/Demo/MLmodel/finalmodel.pickle','rb'))
        pred  = model.predict([textTweet])
        return render_template('final.html',prediction = pred)

if __name__ == '__main__':
  app.run()
