# Public Wi-Fi Usage Pattern Analysis Using Hadoop, MapReduce, Hive and R

## 1. Project title
Public Wi-Fi Usage Pattern Analysis Using Hadoop, MapReduce, Hive and R

## 2. Abstract
This micro-project demonstrates the Hadoop ecosystem for a realistic academic Big Data problem: analyzing public Wi-Fi usage records. The project uses HDFS for storage, MapReduce for distributed processing, Hive for SQL-based analytics, and R for statistical analysis and visualization. The records are synthetic and generated for academic demonstration. The dataset is intentionally designed to resemble real public Wi-Fi connection patterns while avoiding unsupported claims about real users or real-world Wi-Fi networks.

## 3. Problem statement
Public Wi-Fi networks produce large volumes of connection events. Institutions, telecom operators, and city planners often need to know: which hotspots are most popular, when usage peaks, how long users remain connected, and how much bandwidth is consumed. Traditional single-node tools are limited when the dataset grows beyond a few million records. A Big Data approach is required to process and analyze such datasets efficiently.

## 4. Objectives
1. Store Wi-Fi connection logs in HDFS
2. Process data using MapReduce jobs
3. Query data using Hive
4. Perform statistical analysis and charts using R
5. Generate practical insights for hotspot performance and usage patterns
6. Demonstrate the Hadoop ecosystem clearly in an academic setting

## 5. Existing problem
A basic spreadsheet approach is not suitable for large-scale Wi-Fi telemetry because:
- log files can span millions of records
- hotspot usage varies by hour, day, and device type
- repeated aggregation queries become expensive on a single machine
- real-time operational analysis requires distributed processing

## 6. Proposed system
The proposed architecture uses HDFS for distributed storage, YARN for resource management, MapReduce for batch processing, Hive for SQL-based analytics, and R for reporting and visualization. The workflow is:

CSV Dataset
    ↓
Data Preprocessing
    ↓
HDFS
    ↓
MapReduce + Hive
    ↓
Processed Results
    ↓
R Statistical Analysis
    ↓
Charts + Insights

## 7. Technologies used
- Hadoop HDFS
- Hadoop YARN
- Hadoop MapReduce
- Apache Hive
- R Programming
- Python for synthetic dataset generation and MapReduce streaming scripts
- Shell scripting for HDFS, Hive, and execution automation

## 8. Dataset description
The dataset is a synthetic Wi-Fi log dataset created for academic demonstration. It includes fields such as:
- connection_id
- date
- time
- hotspot_id
- hotspot_location
- user_id
- device_type
- duration_minutes
- data_used_mb
- optional fields: authentication_type, network_type, session_status, download_mb, upload_mb

The project generates 10,000+ records and is designed to scale to much larger datasets. Because this environment currently does not have Hadoop/Hive/R installed, the dataset is intentionally simulated.

## 9. System architecture
The system is organized as follows:
- data/raw contains the raw CSV file
- HDFS stores the raw dataset
- MapReduce scripts summarize hotspot counts, duration, data usage, and hourly usage
- Hive queries perform richer analytical processing
- R reads processed outputs and creates charts and summary reports

## 10. Hadoop architecture
The Hadoop ecosystem used in this project is built around the following components:
- HDFS: reliable distributed storage
- YARN: cluster resource management and scheduling
- MapReduce: distributed data processing
- Hive: high-level SQL layer over distributed data

## 11. HDFS role
HDFS is the storage backbone. It stores the raw Wi-Fi dataset, keeps large files distributed, and provides a scalable location for intermediate and final outputs. The project uses the following HDFS directory:

- /wifi
- /wifi/raw
- /wifi/output

## 12. MapReduce workflow
MapReduce is the core distributed processing layer. Each MapReduce job follows the classic workflow:
1. Mapper reads a CSV record from HDFS
2. Mapper emits intermediate key-value pairs
3. Shuffle and Sort groups pairs by key
4. Reducer aggregates the values for each key
5. Final result is written back to HDFS

Examples:
- hotspot connection count: hotspot_id -> total connections
- average duration: hotspot_id -> average duration
- total data usage: hotspot_id -> total data used
- hour usage: hour -> number of connections

## 13. Hive workflow
Hive provides a SQL-like interface over data stored in HDFS. Instead of writing custom Java jobs for every query, Hive allows analytical tasks to be expressed as HQL. This is useful for:
- total connection counts
- hotspot distribution
- duration and usage summaries
- device-type trends
- daily and hourly hotspot analysis

## 14. R workflow
R is used after Hadoop/Hive processing to analyze aggregated CSV outputs. It reads the processed results, performs summary statistics, and generates charts including:
- hotspot connection bar chart
- usage trend line chart
- data consumption chart
- device distribution
- histogram of durations
- hotspot-hour heatmap
- average duration by hotspot

## 15. Installation requirements
The project is intended for a Hadoop 2.x/3.x environment.

Recommended software:
- Java JDK 8 or newer
- Hadoop 2.x or 3.x
- Hive 2.x or 3.x
- R 4.x or newer
- Python 3.8+
- Optional: bash shell on Linux/macOS; Windows users may use WSL or Git Bash

## 16. Hadoop setup
Typical installation and validation steps:

```bash
java -version
hadoop version
hdfs version
start-dfs.sh
start-yarn.sh
jps
```

Check that NameNode, DataNode, ResourceManager, and NodeManager are running.

## 17. Hive setup
```bash
hive --version
```
If Hive is installed in a custom location, export it:

```bash
export HIVE_HOME=/path/to/hive
export PATH=$HIVE_HOME/bin:$PATH
```

## 18. R setup
```bash
R --version
Rscript --version
```
If R is installed in a custom location:

```bash
export PATH=/usr/local/bin:$PATH
```

## 19. Dataset generation
The dataset is generated with Python and saved to:

- data/raw/wifi_usage.csv

The generator creates 10,000+ rows and includes required and optional columns. It is clearly synthetic and intended for academic demonstration.

## 20. HDFS commands
```bash
hdfs dfs -mkdir -p /wifi/raw
hdfs dfs -mkdir -p /wifi/output
hdfs dfs -put -f data/raw/wifi_usage.csv /wifi/raw/
hdfs dfs -ls -R /wifi
hdfs dfs -cat /wifi/raw/wifi_usage.csv | head
hdfs dfs -get /wifi/output/hotspot_count/part-00000 output/mapreduce/hotspot_count.txt
hdfs dfs -rm -r /wifi/test
```

## 21. MapReduce commands
Hadoop Streaming is used with Python mappers and reducers.

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files mapreduce/hotspot_count.py \
  -mapper "python3 hotspot_count.py map" \
  -reducer "python3 hotspot_count.py reduce" \
  -input /wifi/raw/wifi_usage.csv \
  -output /wifi/output/hotspot_count
```

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files mapreduce/duration_analysis.py \
  -mapper "python3 duration_analysis.py map" \
  -reducer "python3 duration_analysis.py reduce" \
  -input /wifi/raw/wifi_usage.csv \
  -output /wifi/output/duration_analysis
```

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files mapreduce/data_usage.py \
  -mapper "python3 data_usage.py map" \
  -reducer "python3 data_usage.py reduce" \
  -input /wifi/raw/wifi_usage.csv \
  -output /wifi/output/data_usage
```

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files mapreduce/hourly_usage.py \
  -mapper "python3 hourly_usage.py map" \
  -reducer "python3 hourly_usage.py reduce" \
  -input /wifi/raw/wifi_usage.csv \
  -output /wifi/output/hourly_usage
```

## 22. Hive commands
```bash
hive -f hive/create_database.hql
hive -f hive/create_tables.hql
hive -f hive/load_data.hql
hive -f hive/analytics_queries.hql
```

The database created is:

```sql
CREATE DATABASE IF NOT EXISTS wifi_analytics;
```

## 23. R execution commands
```bash
Rscript r/analysis.R
Rscript r/visualizations.R
```

## 24. Expected outputs
The project generates:
- hotspot connection summary in HDFS or Hive output
- average duration by hotspot
- total data usage by hotspot
- hourly usage counts
- charts in output/charts/
- summary report in output/reports/

## 25. Results
Expected analytical results include:
- most frequently used hotspot
- peak usage hour
- highest total consumption hotspot
- device-type usage mix
- day-wise trends and hotspot activity patterns

These are demonstrated using aggregated results from MapReduce and Hive, then visualized with R.

## 26. Limitations
- The project uses synthetic data, not real Wi-Fi telemetry
- The examples are academic and educational
- Exact values depend on randomly generated records
- Real cluster tuning is required for enterprise-scale workloads

## 27. Future scope
- Add streaming ingestion using Kafka or Flume
- Move from batch MapReduce to Spark SQL
- Add dashboards using Shiny in R or a web dashboard
- Connect to real public Wi-Fi telemetry sources

## Project structure
```text
Public-WiFi-BigData/
├── data/
│   ├── generate_wifi_usage.py
│   ├── raw/
│   │   └── wifi_usage.csv
│   └── processed/
├── mapreduce/
│   ├── hotspot_count.py
│   ├── duration_analysis.py
│   ├── data_usage.py
│   └── hourly_usage.py
├── hive/
│   ├── create_database.hql
│   ├── create_tables.hql
│   ├── load_data.hql
│   └── analytics_queries.hql
├── r/
│   ├── analysis.R
│   └── visualizations.R
├── scripts/
│   ├── upload_to_hdfs.sh
│   ├── run_mapreduce.sh
│   └── run_hive.sh
├── output/
│   ├── mapreduce/
│   ├── hive/
│   ├── charts/
│   └── reports/
├── README.md
├── requirements.txt
└── .gitignore
```

## Step-by-step execution
1. Create the dataset with Python
2. Upload the dataset into HDFS
3. Run MapReduce jobs
4. Run Hive queries
5. Run R analysis scripts
6. Review charts and the summary report

## Sample expected output
Example values are illustrative only:

```text
Most used hotspot: HS-204
Peak usage hour: 18:00-19:00
Average duration: 53.4 minutes
Total data consumed: 842,341 MB
Top device type: Smartphone
```

## Troubleshooting guide
### Hadoop/HDFS unavailable
If `hadoop` is not installed or not in PATH, install Hadoop and verify:

```bash
hadoop version
hdfs version
```

### Hive unavailable
If `hive` cannot be found:

```bash
which hive
hive --version
```

### R unavailable
If `Rscript` is not found:

```bash
which Rscript
Rscript --version
```

### Dataset missing
Run:

```bash
python3 data/generate_wifi_usage.py
```

### Malformed CSV rows
The MapReduce and Hive scripts skip malformed rows or flag them in logs.

### Null values / invalid duration
The generator and scripts validate:
- missing values
- negative durations
- invalid data usage
- malformed time values

## Academic concept mapping
- HDFS → distributed storage layer
- YARN → resource management layer
- MapReduce → distributed processing
- Hive → SQL analytics over Big Data
- R → statistics and visualization

## Note on the public dataset reference
The prompt references a Hugging Face Wi-Fi dataset. This project uses a synthetic dataset generated locally to keep the academic exercise portable and reproducible in any environment. The synthetic dataset follows the same learning objective: hotspot usage, time trends, duration analysis, and consumption patterns. If a real dataset is later available, the same HDFS/Hive/R pipeline can be applied with minimal changes.

## Final note
This project is a demonstration of the Hadoop ecosystem for educational purposes. It is intentionally designed to be clear, reproducible, and easy to adapt to a college practical environment.
