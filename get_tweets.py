import tweepy
import csv
import credentials as creds

#Twitter API credentials
consumer_key = '2Z4wEHdx0FDmq9y5X0rHiU72E'
consumer_secret = 'e9Dmg5p5NpDrH2U6SzUSa1vdr4yI9lZqSO9UF3zDFzwt1T9Jj9'
access_key = '549870381-O0BYSb5GJHf2HEabrWkBVw7vN1NHC4z7l3SGeKhh'
access_secret = 'B6luotvY1Ptnm13YH1KWHNOfcBovjzFwE7dNrTtGRKeK3'

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	alltweets = []
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	alltweets.extend(new_tweets)
	oldest = alltweets[-1].id - 1
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest) 
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1].id - 1

		print "...%s tweets downloaded so far" % (len(alltweets))

	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

        csv_out = open('donald_tweets.csv', 'wb')
        writer = csv.writer(csv_out)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
        csv_out.close()

username = "realDonaldTrump"
print "Downloading new tweets from @", username
get_all_tweets(username)
