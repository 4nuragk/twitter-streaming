
CREATE KEYSPACE test_keyspace WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};

CREATE TABLE test_keyspace.hashtag_test (
    created_date date,
    created_time text,
    token_name text,
    count bigint,
    tweet_text text,
    tweetid_list list<text>,
    PRIMARY KEY (created_date, created_time, token_name)
)