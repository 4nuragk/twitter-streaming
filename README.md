# Twitter-streaming
In this repo we will stream crawl and save data from Twitter using Apache Spark and Cassandra.

## Follow these steps to setup spark (On any Linux Platfrom)

### Java Installation is mandatory for spark. Check installation by the command 'jps'. It must output jps.

### STEP 1:
a. Download spark from https://www.apache.org/dyn/closer.lua/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz (We are using the spark version 2.4.4 and hadoop version 2.7 as of Dec 2019)
b. Extract the tar file to a specific directory(your choice).
c. Now edit the .bashrc file(vim ~/.bashrc) put this two lines(replace the <path to dir> to your path of installation).
    #SPARK
    export SPARK_HOME=<path to the dir>/spark-2.4.4-bin-hadoop2.7
    export PATH=$SPARK_HOME/bin:$PATH
d. source the bashrc
    # source ~/.bashrc
e. cd to the spark dir/sbin
    # cd $SPARK_HOME/sbin
f. start the master. 
    # bash start-master.sh
g. go to your localhost and port 8080(http://localhost:8080) in your browser and copy the spark master url which will be in the format spark://HOST:PORT
h. now in your sbin dir, start slave (using the master url you copied):
    # bash start-slave.sh spark://HOST:PORT
Your Spark installation is ready to use. Check 'jps' and you'll see master and slave running.
