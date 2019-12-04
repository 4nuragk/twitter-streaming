# Twitter-streaming
In this repo we will stream crawl and save data from Twitter using Apache Spark and Cassandra.

## Follow these steps to setup your system (Linux Platfrom only)

**Java Installation is mandatory. Check installation by the command 'jps'. It must output jps**

### STEP 1: Setting up Spark
* Download spark from https://www.apache.org/dyn/closer.lua/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz (We are using the spark version 2.4.4 and hadoop version 2.7 as of Dec 2019)<br>
* Extract the tar file to a specific directory(your choice).<br>
* Now edit the .bashrc file(vim ~/.bashrc) put these lines(replace the "path to dir" to your path of installation).<br>
    * #SPARK<br>
    * export SPARK_HOME=path to the dir/spark-2.4.4-bin-hadoop2.7<br>
    * export PATH=$SPARK_HOME/bin:$PATH<br>
* source the bashrc<br>
    * source ~/.bashrc<br>
* cd to the spark dir/sbin<br>
    * cd $SPARK_HOME/sbin<br>
* start the master. <br>
    * bash start-master.sh<br>
* go to your localhost and port 8080(http://localhost:8080) in your browser and copy the spark master url which will be in the format spark://HOST:PORT<br>
* now in your sbin dir, start slave (using the master url you copied):<br>
    * bash start-slave.sh spark://HOST:PORT<br>
Your Spark installation is ready to use. **Check 'jps' and you'll see master and slave running.**<br>

### Step 2: Setting up cassandra

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
### Step 3: Anaconda

* Install anaconda(We will be using python 2.7):
   * curl -O https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
* Create environment and install dependencies:
   * conda env create -f environment.yml
* Activate the environment:
   * conda activate spark

