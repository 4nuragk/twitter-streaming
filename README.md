# Twitter-streaming
In this repo we will stream crawl and save data from Twitter using Apache Spark and Cassandra.

## Follow these steps to setup spark (On any Linux Platfrom)

### Java Installation is mandatory for spark. Check installation by the command 'jps'. It must output jps.

* STEP 1:
a. Download spark from https://www.apache.org/dyn/closer.lua/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz (We are using the spark version 2.4.4 and hadoop version 2.7 as of Dec 2019)<br>
b. Extract the tar file to a specific directory(your choice).<br>
c. Now edit the .bashrc file(vim ~/.bashrc) put this two lines(replace the "<path to dir>" to your path of installation).<br>
    #SPARK<br>
    export SPARK_HOME=<path to the dir>/spark-2.4.4-bin-hadoop2.7<br>
    export PATH=$SPARK_HOME/bin:$PATH<br>
d. source the bashrc<br>
    # source ~/.bashrc<br>
e. cd to the spark dir/sbin<br>
    # cd $SPARK_HOME/sbin<br>
f. start the master. <br>
    # bash start-master.sh<br>
g. go to your localhost and port 8080(http://localhost:8080) in your browser and copy the spark master url which will be in the format spark://HOST:PORT<br>
h. now in your sbin dir, start slave (using the master url you copied):<br>
    # bash start-slave.sh spark://HOST:PORT<br>
Your Spark installation is ready to use. Check 'jps' and you'll see master and slave running.<br>
