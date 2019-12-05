# -*- coding: utf-8 -*-

from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests
import cPickle as pkl
import pickle
from collections import OrderedDict
import glob
import os
import re
import csv
import string
import pandas as pd
import numpy as np
from cassandra.cluster import Cluster
import warnings
from cassandra.policies import RoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
warnings.simplefilter('ignore')
import logging
import json
from os import system, name 
from time import sleep 
import io
from pyspark.sql.functions import explode
import pyspark.sql.functions as f
import datetime
from pyspark.sql import SparkSession
from itertools import product
import sys
from pyspark.sql.functions import udf
from timeit import default_timer as timer
pd.set_option('display.max_columns', None)  
from pyspark.sql.functions import lit,unix_timestamp
from pyspark.sql import functions as F
from pyspark.sql.types import *
reload(sys)
sys.setdefaultencoding("utf-8")

conf = SparkConf().set("spark.cassandra.connection.host", "localhost")\
.set("spark.cassandra.connection.keep_alive_ms", "12000")\
.set("spark.cassandra.input.consistency.level","LOCAL_ONE")\
.set("spark.cassandra.output.consistency.level","LOCAL_ONE")\
.set("spark.cassandra.output.concurrent.writes",1000)\
.set("spark.cassandra.output.batch.grouping.key","Partition")\
.set("spark.cassandra.output.batch.size.rows",1)\
.set("spark.kryoserializer.buffer.max","1g")\
.set("spark.streaming.blockInterval","8000") \
.set("spark.streaming.concurrentJobs","10")\
.set("spark.cleaner.ttl","3min")\
.set("spark.cleaner.periodicGC.interval","3min") \
.set("spark.cleaner.referenceTracking.blocking", "false")\
.set("spark.worker.ui.retainedExecutors", "100")\
.set("spark.worker.ui.retainedDrivers",20) \
.set("spark.sql.ui.retainedExecutions","100")\
.set("spark.streaming.ui.retainedBatches","100") \
.set("spark.ui.retainedJobs", "100").set("spark.ui.retainedStages", "100")\
.set("spark.ui.retainedTasks","100") \
.set("spark.streaming.backpressure.enabled","true")

sc = SparkContext.getOrCreate(conf)
ssc = StreamingContext(sc, 10)
sc.setLogLevel("ERROR")
dataStream1 = ssc.socketTextStream("localhost",9012)


def get_sql_context_instance(spark_context):
	if ('sqlContextSingletonInstance' not in globals()):
		globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
	return globals()['sqlContextSingletonInstance']


def process1(time,rdd):

	print("1st dstream")
	
	if not rdd.isEmpty():		#co_occuring_list = rdd.map(get_co_occuring_hash_tag)
		print(rdd.collect())
		print("done")


def process2(time,rdd):

	print("2nd dstream")
	
	if not rdd.isEmpty():		#co_occuring_list = rdd.map(get_co_occuring_hash_tag)
		print(rdd.collect())
		print("done")


def get_hashtag(json_dictionary):

	combine_hashtags_list=[]
	full_text = json_dictionary['text']

	if not isinstance(json_dictionary, dict):
		json_dictionary=json_dictionary.__dict__ 
	truncated = json_dictionary['truncated']
	
	try:
		if truncated:

			extended_tweet_dict = json_dictionary['extended_tweet']
			# tweet_text = extended_tweet_dict['full_text']
			entities = extended_tweet_dict['entities']		
			##for #tag..............
			if entities.has_key('hashtags'):
				hashtags_list = entities['hashtags']  ## in list format from crawler
				
				for h in hashtags_list:
					ht = h['text']
					combine_hashtags_list.append('#'+ht)
					combine_hashtags_list=list(set(combine_hashtags_list))
		else:
			##for #tag..............
			if json_dictionary['entities'].has_key('hashtags'):
				hashtags_list = json_dictionary['entities']['hashtags']  ## in list format from crawler
				# hashtags_list1 = []
				for h in hashtags_list:
					ht = h['text']
					combine_hashtags_list.append('#'+ht)
					combine_hashtags_list=list(set(combine_hashtags_list))
		

		combine_sentiment_hash = zip([full_text],combine_hashtags_list)

		return combine_sentiment_hash

	except:

		e = sys.exc_info()[0]
		print("Error: %s" % e)
		return combine_hashtags_list


def get_hashtag_tweetid(json_dictionary):

	combine_hashtags_list=[]
	full_text = json_dictionary['text']

	if not isinstance(json_dictionary, dict):
		json_dictionary=json_dictionary.__dict__ 
	truncated = json_dictionary['truncated']
	# try:
	tweet_id = json_dictionary['id_str']
	if truncated:

		extended_tweet_dict = json_dictionary['extended_tweet']
		entities = extended_tweet_dict['entities']		
		##for #tag..............
		if entities.has_key('hashtags'):
			hashtags_list = entities['hashtags']  ## in list format from crawler
			
			for h in hashtags_list:
				ht = h['text']
				combine_hashtags_list.append('#'+ht)
				combine_hashtags_list=list(set(combine_hashtags_list))
	else:
		##for #tag..............
		if json_dictionary['entities'].has_key('hashtags'):
			hashtags_list = json_dictionary['entities']['hashtags']  ## in list format from crawler
			for h in hashtags_list:
				ht = h['text']
				combine_hashtags_list.append('#'+ht)
				combine_hashtags_list=list(set(combine_hashtags_list))


	combine_hash = zip([full_text],combine_hashtags_list)
	ids =[[tweet_id]] * len(combine_hash)

	combine_ids_hash = zip(combine_hash,ids)

	return combine_ids_hash



	#((u'RT @IsmailMehak: W', u'#IAmWithSidShukla'), (1, [u'1202628470611689473']))


def checker_tweet(data):

	try:

		check_data1 = data[0][0]#text
		check_data2 = data[0][1]#tag
		check_data4 = data[1][0]#count
		check_data5 = data[1][1]#tweetid

		return data

	except: 
		return ((u'dummy', u'dummy'), (1, [u'dummy']))

def window_hashtag_rdd(time,rdd):

	print("----------- %s -----------" % str(time))
	start = timer()
	print("10 sec window")

	try:
		if not rdd.isEmpty():		#co_occuring_list = rdd.map(get_co_occuring_hash_tag)
			sql_context = get_sql_context_instance(rdd.context)
			#spark = SparkSession.builder.appName("SparkCassandra1").config(conf=conf).getOrCreate()
			today_date = datetime.datetime.utcnow().date()
			today_time = str(time.strftime('%H:%M:%S'))
			check_rdd = rdd.map(checker_tweet)
			row_rdd = check_rdd.map(lambda w: Row(created_date=today_date,created_time=today_time, tweet_text=w[0][0], token_name=w[0][1], count=w[1][0],tweetid_list=w[1][1]))
			window_hashtag_rdd = sql_context.createDataFrame(row_rdd)
			window_hashtag_rdd.write.format("org.apache.spark.sql.cassandra")\
			.mode('append')\
			.options(table="hashtag_test", keyspace="test_keyspace")\
			.save()
			sql_context.clearCache()
			window_hashtag_rdd.show()
			end_time = timer()
			time_taken = end_time - start
			print("The time taken to count sensitive is %s",time_taken)

	except:

		e = sys.exc_info()[0]
		print("Error: %s" % e)


def main():

	start_time = timer()
	newstream1 = dataStream1.map(lambda recieved: json.loads(recieved))
	
	########################################################################################################################
	total_hashtags=newstream1.map(get_hashtag)
	total_hashtags_index = total_hashtags.flatMap(lambda xs: [(x, 1) for x in xs]) 

	tweet_id_list_with_hashtag = newstream1.map(get_hashtag_tweetid)
	combine_tweet_id_list_with_hashtag = tweet_id_list_with_hashtag.flatMap(lambda xs:[(x[0], x[1]) for x in xs if x!=[]])

	count_hashtags = total_hashtags_index.reduceByKey(lambda a,b:a+b)
	count_hashtags_id = combine_tweet_id_list_with_hashtag.reduceByKey(lambda a,b:(a+b))

	id_hashtag_union = count_hashtags.union(count_hashtags_id)
	combine_hashtag_id = id_hashtag_union.reduceByKey(lambda a,b:(a,b))
	combine_hashtag_id.foreachRDD(window_hashtag_rdd)
	#########################################################################################################################

	end_time = timer()
	print("This is the start time",start_time)
	print("This is the end time",end_time)
	time_elapsed = start_time-end_time
	print("Time elpsed is",time_elapsed)
	ssc.start()
	ssc.awaitTermination()


		
if __name__=='__main__':

	main()
	
