CREATE DATABASE IF NOT EXISTS wifi_analytics;
USE wifi_analytics;

CREATE EXTERNAL TABLE IF NOT EXISTS wifi_usage_raw (
    connection_id STRING,
    date STRING,
    time STRING,
    hotspot_id STRING,
    hotspot_location STRING,
    user_id STRING,
    device_type STRING,
    duration_minutes INT,
    data_used_mb DOUBLE,
    authentication_type STRING,
    network_type STRING,
    session_status STRING,
    download_mb DOUBLE,
    upload_mb DOUBLE
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/wifi/raw'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE TABLE IF NOT EXISTS wifi_usage_internal (
    connection_id STRING,
    date STRING,
    time STRING,
    hotspot_id STRING,
    hotspot_location STRING,
    user_id STRING,
    device_type STRING,
    duration_minutes INT,
    data_used_mb DOUBLE,
    authentication_type STRING,
    network_type STRING,
    session_status STRING,
    download_mb DOUBLE,
    upload_mb DOUBLE
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
