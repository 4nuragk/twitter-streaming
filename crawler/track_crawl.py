import tweepy, time, json, sys, datetime, traceback, pprint, logging, os, atexit, math
from tweepy.streaming import StreamListener
from collections import OrderedDict 
import socket
import cPickle as pkl
import pickle
from keras.models import model_from_json
import numpy as np
import glob
import os
import re
import string
reload(sys)
sys.setdefaultencoding('utf-8')
import gc
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.collocations import *
from operator import itemgetter
from pattern.en import parse
from timeit import default_timer as timer


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


#Create and configure logger                                                   
logging.basicConfig(filename="new_crawler_track_tweet_10sec.log", format='INFO %(asctime)s %(message)s', filemode='a')
#Creating an object                                                            
logger=logging.getLogger()                                                     
#Setting the threshold of logger to DEBUG                                      
logger.setLevel(logging.INFO) 
#logger.info("5698999")

##initialization..........
tweet_count = 0
datetime1 = datetime.datetime.utcnow()
d1 = str(datetime1).split(".")[0].replace("-", "").replace(":", "").replace(" ", "_")
filename =str(d1)+"-t.json"

final_dict = OrderedDict()

def extract_words(text):
	result = []
	stop = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u"you're", u"you've", u"you'll", u"you'd", u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u"she's", u'her', u'hers', u'herself', u'it', u"it's", u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u"that'll", u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u"don't", u'should', u"should've", u'now', u'd', u'll', u'm', u'o', u're', u've', u'y', u'ain', u'aren', u"aren't", u'couldn', u"couldn't", u'didn', u"didn't", u'doesn', u"doesn't", u'hadn', u"hadn't", u'hasn', u"hasn't", u'haven', u"haven't", u'isn', u"isn't", u'ma', u'mightn', u"mightn't", u'mustn', u"mustn't", u'needn', u"needn't", u'shan', u"shan't", u'shouldn', u"shouldn't", u'wasn', u"wasn't", u'weren', u"weren't", u'won', u"won't", u'wouldn', u"wouldn't", 'sir','day','title','shri','crore','day','time',"a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the","&amp;","?",'!',',',';',':','.','\t','$','/','|','amp','url']
	text = re.sub(r'[^\x00-\x7F]+',' ', text)
	text = text.replace('<br />', ' ')
	text = text.replace('--', ' ').replace('\'s', '')
	text = re.sub(r'[^\w\s]','',text)
	words = []
	for word in text.split():
		word = word.lstrip('-\'\"').rstrip('-\'\"')
		if len(word)>2:
			words.append(word.lower())
	text = ' '.join(words)
	result.append(text.strip())
	return result


def grab_data(sentences):
	seqs = [None] * len(sentences)
	for idx, ss in enumerate(sentences):
		words = ss.strip().lower().split()
		seqs[idx] = [dictionary[w] if w in dictionary else 1 for w in words]
	return seqs


def flatten(neste_list):
	flatten_matrix = [val for sublist in neste_list for val in sublist]
	return flatten_matrix

def pad(l, fill_value, width):

	if len(l) >= width:
		return l[0: width]
	else:
		padding = [fill_value] * (width - len(l))
		padding.extend(l)
		return padding


############################## START Keyword extraction #################################

def extract_link(text):
	regex = r'https?://[^\s<>"]+|www\.[^\s<>)"]+'
	match = re.findall(regex, text)
	links = [] 
	for x in match: 
		if x[-1] in string.punctuation: links.append(x[:-1])
		else: links.append(x)
	return links
	
def cleanup(query): 
	try:
		urls = extract_link(" " + query + " ")
		for url in urls: 
			query = re.sub(url, "", query)
		q = query.strip()
	except:
		q = query
	q = re.sub(' RT ', '', ' ' + q + ' ').strip() 
	return q 


def convert_tag_format(query): 
	word = query.split(' ')
	postag = [(x.split('/')[0], x.split('/')[1]) for x in word]
	return postag 
	

def get_pos_tags(text): 
	tagged_sent = parse(text)	
	return convert_tag_format(tagged_sent), tagged_sent
	
def normalise(word):
	word = word.lower()
	return word


## conditions for acceptable word: length, stopword
def acceptable_word(word):
    accepted = bool(4 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted

## extract entity from BIO encoding 
def extract_entity(filetext):
	last_entity = '' 
	last_tag = '' 
	mention2entities = {} 
	for line in filetext.split('\n'): 
		line = line.strip() 
		if line == '': 
			continue
		line_split = line.split('\t')
		if re.search('B-', line_split[1]): 
			if last_entity != '': 
				if not last_tag in mention2entities:
					mention2entities[last_tag] = [] 
				mention2entities[last_tag].append(last_entity.strip())
			last_entity = line_split[0] + ' '
			last_tag = line_split[1][2:] 
		elif re.search('I-', line_split[1]): 
			last_entity += line_split[0] + ' '
	if last_entity != '': 
		if not last_tag in mention2entities:
			mention2entities[last_tag] = [] 
		mention2entities[last_tag].append(last_entity.strip())
	return 	mention2entities

	
def get_entities_from_phrase(tagged_sent, phrase2consider): 
	word = tagged_sent.split(' ')
	bio_tags = [normalise(x.split('/')[0])+ '\t'+ x.split('/')[2] for x in word]
	bio_text = '\n'.join(bio_tags)
	mention2entities = extract_entity(bio_text)
	#print mention2entities.keys() 
	
	## strip off unacceptable words 
	_mention2entities = {} 
	for mention in mention2entities: 
		if not mention in phrase2consider: 
			continue
		_mention2entities[mention] = [] 
		for entity in mention2entities[mention]: 
			_entity = ' '.join([word for word in entity.split(' ') if acceptable_word(word)]).strip()
			if _entity != '': 
				_mention2entities[mention].append(_entity)
			
	entities = []
	for mention in _mention2entities: 
		entities.extend(_mention2entities[mention])
	return entities	
	

def getKeywords(text, phrase2consider=['NP', 'ADJP']): 
	_text = cleanup(text)
	try:
		postoks, tagged_sent = get_pos_tags(_text)
		entities = get_entities_from_phrase(tagged_sent, phrase2consider)
	except: 
		return []
	return entities


symbols = ['&amp;', '!',',',';','.','(',')','\'']
stopwords = ['sir','day','title','shri','crore','day','time',"a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
#find keyword from one text
def find_keyword(tweet_text):
	# print tweet_text
	x=tweet_text
	# print type(x)
	if x is not None:
		x=x.strip()	
		#print x
		#sys.exit()
		token = x.strip().split()
		l=[]
		for t in token :
			if t.find('@')>=0 or t.find('#') >=0 or t.find('...') >=0 or t.find('http:') >=0 or t.find('https:') >=0  :
				pass
			else :
				l.append(t)
		bi=[]			
		temp = ' '.join(l)			
		keywords_list = getKeywords(temp)
		return keywords_list


### END Keyword extraction ### 


class MyStreamListener(StreamListener):	
	
	# consumer_key = ""
	# consumer_secret = ""
	# access_token = ""
	# access_token_secret = ""  


	#Sets up connection with OAuth
	def __init__(self,csocket):
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(auth)
		self.client_socket = csocket

	def on_data(self, data):
		try:
	
			print("--------------------")
			# start_time = time.time()
			full_tweet = json.loads(data)


			if full_tweet.has_key('retweeted_status'):
				if not isinstance(full_tweet['retweeted_status'], dict):
					full_tweet['retweeted_status']=full_tweet['retweeted_status'].__dict__ 
				retweeted_text = full_tweet['retweeted_status']['text']


			if full_tweet.has_key('quoted_status'):
				if not isinstance(full_tweet['quoted_status'], dict):
					full_tweet['quoted_status']=full_tweet['quoted_status'].__dict__
				quoted_text = full_tweet['quoted_status']['text']
				result_quoted_keyword = find_keyword(quoted_text)
				full_tweet['quoted_status']['keyword']=result_quoted_keyword



			tweet_text = full_tweet['text']	
			print(tweet_text)


			# result_keyword = find_keyword(tweet_text)
			# full_tweet['keyword']=result_keyword

			#print(full_tweet)
			data=json.dumps(full_tweet,encoding="utf-8")
			self.client_socket.send(data.encode("utf-8")+ '\n')
			#write_tweets(data.encode("utf-8")+ '\n')
		except Exception, e:
			logger.info("Error in on_data()------->")
			
			
			# traceback.print_exc(file=sys.stdout)
			logger.info(str(datetime.datetime.now()))
			logger.info(str(sys.exc_info()[0]))
			logger.info("Error ===================>")
			logger.info(str(e))

	def on_error(self, status_code):
		self.client_socket.close()
		logger.info("Error in on_error()------->")
		sys.exit()
		# logger.info(datetime.datetime.now(),status_code)
		if status_code == 420:
			# returning False in on_data disconnects the stream
			logger.info('420')
			return False

	def on_limit(self, status):
		logger.info("Error in on_limit()------->")
		logger.info('Limit threshold exceeded'+str(status))

	def on_timeout(self, status):
		logger.info("Error in on_timeout()------->")
		logger.info('Stream disconnected; continuing...')





class twitterHelper:	
	

	# consumer_key = ""
	# consumer_secret = ""
	# access_token = ""
	# access_token_secret = ""  

	
	#Sets up connection with OAuth
	def __init__(self,tcp_connection):    
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(auth)
		self.tcp_connection = tcp_connection

	def getStreamTweets(self, topicList):
		try:
			logger.info(topicList)
			myStreamListener = MyStreamListener(self.tcp_connection)
			myStream = tweepy.Stream(auth=self.api.auth, listener=myStreamListener)
			myStream.filter(track=topicList, is_async=True)
			# myStream.filter(follow=UserList, async=True)
		except Exception, e:
			logger.info("Error in getStreamTweets()------->")
			logger.info(str(e))




def exit_handler():
	global final_dict, filename, tweets_d
	if len(final_dict) > 50:
		datetime1 = datetime.datetime.utcnow()
		d1 = str(datetime1).split(".")[0].replace("-", "").replace(":", "").replace(" ", "_")
		filename =str(d1)+"-t.json"
		# home_directory = os.environ['HOME']
		# tweets_d = home_directory + "/store/streaming_tweets/track_tweets/"
		f = open(tweets_d+filename, 'w')
		json.dump(final_dict, f, ensure_ascii=False, indent=4)
		f.close()
		logger.info('My application connection broken')





# Writes all tweets of a user to a file in json format
def write_tweets(twdata):  
	global tweet_count, final_dict, filename, tweets_d, start_time1
	diff_time = math.ceil(timer()-start_time1)
	# print "write tweets1"
	if diff_time>=11:
		# if tweet_count == 1000:	
		print "write tweets"	
		f = open(tweets_d+filename, 'w')
		json.dump(final_dict, f, ensure_ascii=False, indent=4)
		f.close()		
		##initialization..........
		tweet_count = 0
		datetime1 = datetime.datetime.utcnow()
		d1 = str(datetime1).split(".")[0].replace("-", "").replace(":", "").replace(" ", "_")
		filename =str(d1)+"-t.json"
		start_time1 = timer()
		final_dict = OrderedDict()

	else:
		# bundle_id = str(twdata['id_str'])
		# str11 = bundle_id+", Tweet Count: "+str(tweet_count)
		if diff_time==6:
		# if tweet_count%500==0:
			str11 = "Tweet Count: "+str(tweet_count)
			logger.info(str11)
		# logger.info(tweet_count)
		final_dict.update({tweet_count:twdata})
		tweet_count += 1


if __name__ == '__main__':
	## get home directory....
	#home_directory = os.environ['HOME']
	#tweets_d = home_directory + "/store/streaming_tweets/track_tweets/"
	#tweets_d = "/home/hemanta/store/streaming_tweets/track_tweets/"

	print("test")
	TCP_IP = "localhost"
	TCP_PORT = 9012
	conn = None
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((TCP_IP,TCP_PORT))
	s.listen(1)
	print("Waiting for TCP connection...")
	conn, addr = s.accept()
	print("Connected... Starting getting tweets.")


	t=twitterHelper(conn)
	topicList = []
	#get the trend from twitter................................................................5
	fd = open('trendingTopic_India_twitter.txt','r')
	for line in fd :
		topicList.append(line.strip())
	fd.close()

	xyzList = []
	xyz = open('trackList.txt','r')
	for line in xyz:
		xyzList.append(line.strip())
	xyz.close()

	main_list = topicList+xyzList
	logger.info("Streaming Started ---------------------------------- > ")
	start_time1 = timer()
	t.getStreamTweets(main_list)

	atexit.register(exit_handler)