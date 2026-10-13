USE wifi_analytics;

-- 1. Total number of connections
SELECT COUNT(*) AS total_connections FROM wifi_usage_internal;

-- 2. Number of connections by hotspot
SELECT hotspot_id, COUNT(*) AS connection_count
FROM wifi_usage_internal
GROUP BY hotspot_id
ORDER BY connection_count DESC;

-- 3. Average duration by hotspot
SELECT hotspot_id, ROUND(AVG(duration_minutes), 2) AS avg_duration_minutes
FROM wifi_usage_internal
GROUP BY hotspot_id
ORDER BY avg_duration_minutes DESC;

-- 4. Total data consumption by hotspot
SELECT hotspot_id, ROUND(SUM(data_used_mb), 2) AS total_data_used_mb
FROM wifi_usage_internal
GROUP BY hotspot_id
ORDER BY total_data_used_mb DESC;

-- 5. Device-type distribution
SELECT device_type, COUNT(*) AS device_count
FROM wifi_usage_internal
GROUP BY device_type
ORDER BY device_count DESC;

-- 6. Average duration by device type
SELECT device_type, ROUND(AVG(duration_minutes), 2) AS avg_duration_minutes
FROM wifi_usage_internal
GROUP BY device_type
ORDER BY avg_duration_minutes DESC;

-- 7. Peak usage hour (hour with maximum connections)
SELECT hour_of_day, connection_count
FROM (
    SELECT CAST(SUBSTR(time, 1, 2) AS INT) AS hour_of_day,
           COUNT(*) AS connection_count
    FROM wifi_usage_internal
    GROUP BY CAST(SUBSTR(time, 1, 2) AS INT)
) q
ORDER BY connection_count DESC
LIMIT 1;

-- 8. Daily usage
SELECT date, COUNT(*) AS connection_count
FROM wifi_usage_internal
GROUP BY date
ORDER BY date;

-- 9. Hotspot-wise daily usage
SELECT hotspot_id, date, COUNT(*) AS connection_count
FROM wifi_usage_internal
GROUP BY hotspot_id, date
ORDER BY hotspot_id, date;

-- 10. Hotspot x hour analysis
SELECT hotspot_id,
       CAST(SUBSTR(time, 1, 2) AS INT) AS usage_hour,
       COUNT(*) AS connection_count
FROM wifi_usage_internal
GROUP BY hotspot_id, CAST(SUBSTR(time, 1, 2) AS INT)
ORDER BY hotspot_id, usage_hour;

-- Additional output directory export examples for R processing
INSERT OVERWRITE DIRECTORY '/wifi/output/hive/hotspot_connections'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT hotspot_id, COUNT(*) AS connection_count
FROM wifi_usage_internal
GROUP BY hotspot_id
ORDER BY connection_count DESC;

INSERT OVERWRITE DIRECTORY '/wifi/output/hive/avg_duration_by_hotspot'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT hotspot_id, ROUND(AVG(duration_minutes), 2) AS avg_duration_minutes
FROM wifi_usage_internal
GROUP BY hotspot_id
ORDER BY avg_duration_minutes DESC;

INSERT OVERWRITE DIRECTORY '/wifi/output/hive/total_data_usage_by_hotspot'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT hotspot_id, ROUND(SUM(data_used_mb), 2) AS total_data_used_mb
FROM wifi_usage_internal
GROUP BY hotspot_id
ORDER BY total_data_used_mb DESC;

INSERT OVERWRITE DIRECTORY '/wifi/output/hive/device_distribution'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT device_type, COUNT(*) AS device_count
FROM wifi_usage_internal
GROUP BY device_type
ORDER BY device_count DESC;

INSERT OVERWRITE DIRECTORY '/wifi/output/hive/hourly_usage'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT CAST(SUBSTR(time, 1, 2) AS INT) AS usage_hour, COUNT(*) AS connection_count
FROM wifi_usage_internal
GROUP BY CAST(SUBSTR(time, 1, 2) AS INT)
ORDER BY usage_hour;

INSERT OVERWRITE DIRECTORY '/wifi/output/hive/daily_usage'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT date, COUNT(*) AS connection_count
FROM wifi_usage_internal
GROUP BY date
ORDER BY date;

INSERT OVERWRITE DIRECTORY '/wifi/output/hive/hotspot_hour_matrix'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT hotspot_id,
       CAST(SUBSTR(time, 1, 2) AS INT) AS usage_hour,
       COUNT(*) AS connection_count
FROM wifi_usage_internal
GROUP BY hotspot_id, CAST(SUBSTR(time, 1, 2) AS INT)
ORDER BY hotspot_id, usage_hour;
