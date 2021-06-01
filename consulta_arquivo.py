# -*- coding: utf-8 -*-
import tweepy
from datetime import datetime

consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

resultados = tweepy.Cursor(api.search, tweet_mode="extended", q='#vacina OR #Vacina OR #vacinação OR #Vacinação OR #coronavac OR #Coronavac OR #astrazeneca OR #Astrazeneca OR #pfizer OR #Pfizer OR #covid19 OR #coronavírus OR #coronavirus', lang='pt', rpp=100).items(100000)

arquivo = open("tweets.txt", "w", encoding='UTF-8')
print("COMENCOU A GRAVAR " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

for tweet in resultados:

     hashtags = ''  # Lista que conterá as hashtags do POST.

     if tweet.entities.get('hashtags'):
          for hashtag in tweet.entities.get('hashtags'):
               hashtags += '#' + hashtag.get('text', '')

     # TWEET MESSAGE
     tweet_message = str(tweet.full_text).replace("\n", " ")
     if 280 - len(tweet_message) >= 0:
          tweet_message = str(tweet_message).ljust(280)
     else:
          tweet_message = str(tweet_message)[:280]

     # USER
     if 20 - len(str(tweet.user.screen_name)) >= 0:
          user = str(tweet.user.screen_name).ljust(20)
     else:
          user = str(tweet.user.screen_name)[:20]

     # CREATION DATE
     create_date = str(tweet.created_at).split('-')
     create_date = str(create_date[0]) + str(create_date[1]) + str(create_date[2][:2])

     # LOCATION
     if 50 - len(str(tweet.user.location)) >= 0:
          location = str(tweet.user.location).ljust(50)
     else:
          location = str(tweet.user.location)[:50]

     # HASHTAGS
     if 200 - len(str(hashtags)) >= 0:
          hashtags = str(hashtags).ljust(200)
     else:
          hashtags = str(hashtags)[:200]

     dado = tweet.id_str + str(tweet_message) + str(user) + str(create_date) + str(location) + str(hashtags) + '\n'

     arquivo.write(dado)

arquivo.close()
print("TERMINOU DE GRAVAR " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))