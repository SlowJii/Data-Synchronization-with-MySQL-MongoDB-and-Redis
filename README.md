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

This project demonstrates a comprehensive solution for **real-time data synchronization** across three popular and distinct database types, each representing a different storage paradigm:

- **Relational Database:** `MySQL`  
- **NoSQL Document Database:** `MongoDB`  
- **In-Memory Key-Value Store:** `Redis`

The solution addresses the challenge of synchronizing data from a primary source (**MySQL**) to target systems (**MongoDB**, **Redis**). It is designed to handle both pre-existing data and subsequent changes (`INSERT`, `UPDATE`, `DELETE`). These changes are captured using **MySQL Triggers** and then streamed through a data processing pipeline built with **Apache Kafka** and **Apache Spark** to update the other databases.

---

## Architecture & Workflow

The system architecture is designed to ensure consistency, scalability, and low-latency data processing.

The data processing flow is divided into the following key stages:

### 1. Environment Setup & Initial Data Load

- **Containerization**: All databases (MySQL, MongoDB, Redis) are containerized and managed using **Docker**, simplifying setup and deployment.
- **Schema & Connection**: Apache Spark is configured to connect to all three data stores. The data schema (in `JSON` format) is defined within Spark.
- **Initial Data Load**: An initial batch of data is written to MySQL and MongoDB using Spark. This process includes **data validation** steps (e.g., comparing record counts, verifying checksums) to ensure data is loaded completely and correctly.

### 2. Change Data Capture (CDC)

- **MySQL Triggers**: A set of `Triggers` is implemented in MySQL to automatically monitor data modification events (`INSERT`, `UPDATE`, `DELETE`) on specified tables.
- **Log Table**: When a change occurs, the trigger writes a detailed record of that event into a dedicated log table. This table serves as a reliable source of truth for all data changes.

### 3. Streaming Data Changes with Kafka

- **Kafka Producer**: A Kafka producer process continuously polls the log table in MySQL for new entries.
- **Kafka Topic**: The change records are published as messages to a **Kafka Topic**. Using Kafka decouples the source database from downstream consumers, creating a flexible and fault-tolerant architecture.

### 4. Processing and Sinking Data with Spark Structured Streaming

- **Data Consumption**: **Spark Structured Streaming** acts as a consumer, subscribing to the Kafka topic to receive the stream of data changes in real-time.
- **Transformation**: The raw data from Kafka can be transformed, enriched, or cleaned within Spark as needed.
- **Data Sink**: The processed data is finally written to the target systems:
  - **MongoDB**: Documents are updated to maintain a synchronized state with MySQL, ideal for flexible queries and persistent storage.
  - **Redis**: Data is written as key-value pairs, perfect for high-speed access, caching, and real-time analytics.

---

## Technology Stack

- **Language**: Python  
- **Databases**: MySQL, MongoDB, Redis  
- **Data Processing**: Apache Spark (`Spark SQL`, `Spark Structured Streaming`)  
- **Data Streaming**: Apache Kafka  
- **Containerization**: Docker, Docker Compose  
- **Libraries/Connectors**:  
  - `mysql-connector-python`  
  - `spark-sql-kafka`  
  - `spark-mongodb-connector`  
  - `spark-redis`
