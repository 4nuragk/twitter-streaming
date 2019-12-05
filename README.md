# Twitter-streaming
In this repo we will stream crawl and save data from Twitter using Apache Spark and Cassandra.

## Follow these steps to setup your system (Linux Platfrom only)

* First of all, head on to https://developer.twitter.com/en/apply and apply for developer account.
* Copy all the credentials and save it in a file.
* Credentials include:
	1. consumer_key
	2. consumer_secret
	3. access_token
	4. access_token_secret

-----------------------------------------------------------------------------------------------------------------------------

**Java Installation is mandatory. Check installation by:**

* jps
   * it must output jps
* java -version
   * it must output the version
* echo $JAVA_HOME
   * it must output the path
   
* If not, follow these steps: 
   * download: https://drive.google.com/open?id=1vq9fHY0UgRHFxd9PvH3Msu85FcpjZWWb
   * unzip the file
   * sudo scp java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64 /usr/lib/jvm
   * Edit ~/.bashrc and add these lines:<br>
         * export JAVA_HOME="/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64"<br>
         * export PATH=$JAVA_HOME/bin:$PATH<br>
         * export CLASSPATH=.:$JAVA_HOME/jre/lib:$JAVA_HOME/lib:$JAVA_HOME/lib/tools.jar<br>
   * source ~/.bashrc

-----------------------------------------------------------------------------------------------------------------------------

### STEP 1: Setting up Spark

* Download spark from https://www.apache.org/dyn/closer.lua/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz (We are using the spark version 2.4.4 and hadoop version 2.7 as of Dec 2019)
* Extract the tar file to a specific directory(your choice).
* Now edit the .bashrc file(vim ~/.bashrc) put these lines(replace the "path to dir" to your path of installation).
    * #SPARK
    * export SPARK_HOME=path to the dir/spark-2.4.4-bin-hadoop2.7
    * export PATH=$SPARK_HOME/bin:$PATH
* source the bashrc
    * source ~/.bashrc
* cd to the spark dir/sbin
    * cd $SPARK_HOME/sbin
* start the master.
    * bash start-master.sh
* go to your localhost and port 8080(http://localhost:8080) in your browser and copy the spark master url which will be in the format spark://HOST:PORT
* now in your sbin dir, start slave (using the master url you copied):
    * bash start-slave.sh spark://HOST:PORT
Your Spark installation is ready to use. **Check 'jps' and you'll see master and slave running.**

### Step 2: Setting up Cassandra

* Add the Cassandra Repository File:
    * echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
* Add the GPG Key:
    * sudo apt install curl
    * curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
* Install Cassandra on Ubuntu
    * sudo apt update
    * sudo apt install cassandra
* Start Cassandra:
    * sudo systemctl start cassandra
* Check installation:
    * cqlsh localhost
* Import keyspace schema
    * cqlsh localhost -f schema.cql

    
### Step 3: Setting up Anaconda

* Install anaconda(We will be using python 2.7):
   * curl -O https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
   * source ~/.bashrc
* Create environment and install dependencies:
   * conda env create -f environment.yml
* Activate the environment:
   * conda activate venv
   * conda install -c anaconda pattern

----------------------------------------------------------------------------------------------------------------------------

### Running crawler and streaming:

1. cd to streaming diretory
2. Run this command:<br>
	a. MASTER=(put the master url you copied earlier)<br>
	b.	
${SPARK_HOME}/bin/spark-submit         --master ${MASTER}    --packages com.datastax.spark:spark-cassandra-connector_2.11:2.4.2           streaming.py &>out

