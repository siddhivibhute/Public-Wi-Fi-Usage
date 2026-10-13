USE wifi_analytics;

INSERT OVERWRITE TABLE wifi_usage_internal
SELECT *
FROM wifi_usage_raw;
