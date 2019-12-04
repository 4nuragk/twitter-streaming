# -*- coding: utf-8 -*-

import traceback, logging
import tweepy, datetime
from cassandra.cluster import Cluster
import unicodedata
from cassandra import ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import RoundRobinPolicy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Create and configure logger                                                   
logging.basicConfig(filename="get_place_available_trends.log", format='INFO %(asctime)s %(message)s', filemode='a')
#Creating an object                                                            
logger=logging.getLogger()                                                     
#Setting the threshold of logger to DEBUG                                      
logger.setLevel(logging.INFO) 
#logger.info("5698999")


# Gets top 50 current trends of the place specified by WEOID
def getCurrentTrends(api, place):
	# India(WEOID)-23424848
	return api.trends_place(place)
	
	
def get_homeTimeline(api, place):
	return api.home_timeline()
	
def get_available_trends(api, place):
	return api.trends_available() #tweepy function
	





if __name__ == '__main__':
	consumer_key = "DeCjdJeNZnyLXnAsAptnlkf3l"
	consumer_secret = "a3QRWUkHbksGxnxTvnf38FFv4ZliJit6LDyqHWwakuARzMubHt"
	access_token = "833992697157390336-1pZFbsRdDiokB8tXdQjdGmVXlTPHgfi"
	access_token_secret = "6UhIHY2xLwu4CsOIDdjDTOobXLo63BG1zXM1AG98XjJoh"


	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

    

	
	try:
		logger.info("start crawl trending from india")
		trending_list1 = []
		trends_list = getCurrentTrends(api, '23424848')
		print(trends_list)
		

		flag = False

		fd = open('trendingTopic_India_twitter.txt','w')	
		for item in trends_list:
			for i in xrange(len(item['trends'])):
				print >> fd , item['trends'][i]['name']				
				key = str(item['trends'][i]['name'])
				value = str(item['trends'][i]['tweet_volume'])
				t1 = {key: value}
				trending_list1.append((t1))	
			if not flag:
				d1 = item['created_at']
				if isinstance(d1, datetime.datetime):
					date1 = d1.date()
				else:
					d1 = datetime.datetime.strptime(d1, "%Y-%m-%dT%H:%M:%SZ")
					date1 = d1.date()
				loc = item['locations'][0]['name']
		print trending_list1
		fd.close()
		
		logger.info("completed")
	except Exception, e:		
		logger.info("394878")
		logger.info(str(e))
		sys.exit()



	
	try:
		logger.info("start crawl trending from delhi")
		trending_list1_delhi = []
		trends_list = getCurrentTrends(api, '20070458')
		for item in trends_list:
			for i in xrange(len(item['trends'])):				
				key = str(item['trends'][i]['name'])
				value = str(item['trends'][i]['tweet_volume'])
				t1 = {key: value}
				trending_list1_delhi.append((t1))	
			if not flag:
				d1 = item['created_at']
				if isinstance(d1, datetime.datetime):
					date1 = d1.date()
				else:
					d1 = datetime.datetime.strptime(d1, "%Y-%m-%dT%H:%M:%SZ")
					date1 = d1.date()
					loc = item['locations'][0]['name']
		print trending_list1_delhi
		logger.info("completed")
	except Exception, e:
		logger.info("3111")                                                    
		logger.info(str(e))                                                      
		sys.exit()

	try:
		logger.info("start crawl trending from world")
		trending_list1_world = []
		trends_list = getCurrentTrends(api, '1')
		for item in trends_list:
			for i in xrange(len(item['trends'])):				
				key = str(item['trends'][i]['name'])
				value = str(item['trends'][i]['tweet_volume'])
				t1 = {key: value}
				trending_list1_world.append((t1))	
			if not flag:
				d1 = item['created_at']
				if isinstance(d1, datetime.datetime):
					date1 = d1.date()
				else:
					d1 = datetime.datetime.strptime(d1, "%Y-%m-%dT%H:%M:%SZ")
					date1 = d1.date()
					loc = item['locations'][0]['name']
		print trending_list1_world
		logger.info("completed")
	except Exception, e:
		logger.info("3222")                                                    
		logger.info(str(e))                                                      
		sys.exit()