# Data Synchronization with MySQL - MongoDB - Redis

<h3 align="center">Languages and Tools:</h3>
<p align="center"> 
  <!-- Programming Languages -->
  <a href="https://www.python.org" target="_blank" rel="noreferrer"> 
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> 
  </a>

  <!-- Tools / Platforms / Frameworks -->
  <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> 
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> 
  </a> 
  <a href="https://kafka.apache.org/" target="_blank" rel="noreferrer"> 
    <img src="https://www.vectorlogo.zone/logos/apache_kafka/apache_kafka-icon.svg" alt="kafka" width="40" height="40"/> 
  </a> 
  <a href="https://spark.apache.org/" target="_blank" rel="noreferrer"> 
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/apachespark/apachespark-original-wordmark.svg" alt="spark" width="40" height="40"/>
  </a>
  <a href="https://www.linux.org/" target="_blank" rel="noreferrer"> 
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/> 
  </a> 
  <a href="https://www.mongodb.com/" target="_blank" rel="noreferrer"> 
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mongodb/mongodb-original-wordmark.svg" alt="mongodb" width="40" height="40"/> 
  </a> 
  <a href="https://www.mysql.com/" target="_blank" rel="noreferrer"> 
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="mysql" width="40" height="40"/> 
  </a> 
  <a href="https://redis.io" target="_blank" rel="noreferrer"> 
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/redis/redis-original-wordmark.svg" alt="redis" width="40" height="40"/> 
  </a>
</p>

## Architecture
![Data_Synchronization_Solution_Architecture](https://raw.githubusercontent.com/SlowJii/Data-Synchronization-with-MySQL-MongoDB-and-Redis/refs/heads/master/images/architecture.png)

## **Workflow**

### 1. Data Generation and Initialization
- **Objective**: Create structured data based on a predefined schema  
- **Implementation**:
  - Use Python to generate the dataset  
  - Establish a connection to MySQL using libraries such as `mysql-connector-python`
  - Insert generated data into MySQL for initial storage and further processing  

---

### 2. Data Ingestion into MySQL, MongoDB, and Redis via Apache Spark
- **Objective**: Load large volumes of data from MySQL into MongoDB and Redis using Apache Spark  
- **Implementation**:
  - Use Apache Spark to extract data from MySQL  
  - Perform necessary transformations (if any)  
  - Load the processed data into:
    - **MongoDB**: for document-based access  
    - **Redis**: for caching or fast retrieval  

- **Data Validation Challenge**:
  - With large-scale data, there’s a risk of:
    - Data loss (missing records)  
    - Data duplication  
    - Data inconsistency (corruption during transformation or insertion)  

- **Validation Solutions**:
  - **Newbie Approach**:
    - Utilize log tables during insertion to track the number of records processed and inserted  
    - Manually verify counts across source and target systems  
  - **Professional Approach**:
    - Implement automated data validation mechanisms:

---

### 3. Trigger-Based Data Monitoring in MySQL
- **Objective**: Monitor data changes in MySQL and respond to insert/update events  
- **Implementation**:
  - Create **SQL triggers** in MySQL that activate upon insert/update operations  
  - Triggers will populate a dedicated **logging or change-tracking table**  
  - This table acts as a source for downstream systems to detect data changes in real-time or near real-time  

---

### 4. Kafka Integration for Real-Time Data Streaming
- **Objective**: Stream data changes (from the trigger log table) to real-time consumers using Apache Kafka  
- **Implementation**:
  - Develop a **Kafka producer** to read data from the MySQL trigger table and push it to a **Kafka topic**  
  - Create one or more **Kafka consumers** to subscribe to the topic and process incoming data  

---

### 5. Spark Consumption, Transformation, and Writing to MongoDB and Redis
- **Objective**: Continuously process data in real-time from Kafka and store the results in MongoDB and Redis  
- **Implementation**:
  - **Spark Structured Streaming** consumes data from the Kafka topic  
  - Perform data **transformation and enrichment** using Spark operations  
  - Store the transformed data into:
    - **MongoDB**: for flexible document-based queries and persistent storage  
    - **Redis**: for fast in-memory access, ideal for caching and real-time analytics  

