# R visualization script for the Wi-Fi analytics project
# This script expects processed CSV outputs under output/hive and output/mapreduce
# It creates charts under output/charts and a summary report under output/reports

ensure_package <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg, repos = "https://cloud.r-project.org")
  }
}

ensure_package("ggplot2")
ensure_package("reshape2")

library(ggplot2)
library(reshape2)

project_root <- getwd()
if (!dir.exists(file.path(project_root, "output"))) {
  stop("Project root not detected. Run this script from the project root directory.")
}

charts_dir <- file.path(project_root, "output", "charts")
reports_dir <- file.path(project_root, "output", "reports")
dir.create(charts_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(reports_dir, recursive = TRUE, showWarnings = FALSE)

read_csv_or_stop <- function(relative_path, expected_cols = NULL) {
  full_path <- file.path(project_root, relative_path)
  if (!file.exists(full_path)) {
    stop(paste("Required file not found:", full_path))
  }

  data <- read.csv(full_path, header = FALSE, stringsAsFactors = FALSE)
  if (!is.null(expected_cols) && ncol(data) >= length(expected_cols)) {
    colnames(data) <- expected_cols
  }
  data
}

create_hotspot_connections_chart <- function() {
  hotspot_data <- read_csv_or_stop("output/hive/hotspot_connections", c("hotspot_id", "connection_count"))
  hotspot_data <- hotspot_data[order(hotspot_data$connection_count, decreasing = TRUE), ]
  hotspot_data$hotspot_id <- factor(hotspot_data$hotspot_id, levels = hotspot_data$hotspot_id)

  g <- ggplot(hotspot_data, aes(x = hotspot_id, y = connection_count)) +
    geom_bar(stat = "identity", fill = "steelblue") +
    labs(title = "Wi-Fi Connections by Hotspot", x = "Hotspot ID", y = "Connection Count") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

  ggsave(file.path(charts_dir, "hotspot_connections.png"), plot = g, width = 10, height = 6)
}

create_usage_line_chart <- function() {
  hourly_data <- read_csv_or_stop("output/hive/hourly_usage", c("usage_hour", "connection_count"))
  hourly_data <- hourly_data[order(hourly_data$usage_hour), ]
  hourly_data$usage_hour <- as.integer(hourly_data$usage_hour)

  g <- ggplot(hourly_data, aes(x = usage_hour, y = connection_count)) +
    geom_line(color = "darkgreen", linewidth = 1.2) +
    geom_point(color = "darkgreen", size = 2) +
    labs(title = "Wi-Fi Usage Over Time", x = "Hour of Day", y = "Number of Connections") +
    theme_minimal()

  ggsave(file.path(charts_dir, "usage_over_time.png"), plot = g, width = 10, height = 6)
}

create_data_usage_chart <- function() {
  usage_data <- read_csv_or_stop("output/hive/total_data_usage_by_hotspot", c("hotspot_id", "total_data_used_mb"))
  usage_data <- usage_data[order(usage_data$total_data_used_mb, decreasing = TRUE), ]
  usage_data$hotspot_id <- factor(usage_data$hotspot_id, levels = usage_data$hotspot_id)

  g <- ggplot(usage_data, aes(x = hotspot_id, y = total_data_used_mb)) +
    geom_bar(stat = "identity", fill = "tomato") +
    labs(title = "Total Data Consumption by Hotspot", x = "Hotspot ID", y = "Data Used (MB)") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

  ggsave(file.path(charts_dir, "data_usage_by_hotspot.png"), plot = g, width = 10, height = 6)
}

create_device_distribution_chart <- function() {
  device_data <- read_csv_or_stop("output/hive/device_distribution", c("device_type", "device_count"))
  device_data <- device_data[order(device_data$device_count, decreasing = TRUE), ]
  device_data$device_type <- factor(device_data$device_type, levels = device_data$device_type)

  g <- ggplot(device_data, aes(x = "", y = device_count, fill = device_type)) +
    geom_bar(stat = "identity", width = 1) +
    coord_polar("y", start = 0) +
    labs(title = "Device Type Distribution", fill = "Device Type") +
    theme_minimal() +
    theme(axis.title.x = element_blank(), axis.title.y = element_blank(), axis.text = element_blank())

  ggsave(file.path(charts_dir, "device_type_distribution.png"), plot = g, width = 8, height = 8)
}

create_duration_histogram <- function() {
  duration_data <- read_csv_or_stop("output/mapreduce/duration_analysis", c("hotspot_id", "avg_duration"))
  duration_values <- as.numeric(duration_data$avg_duration)

  g <- ggplot(data.frame(duration = duration_values), aes(x = duration)) +
    geom_histogram(binwidth = 5, fill = "purple", color = "white") +
    labs(title = "Histogram of Average Connection Duration", x = "Average Duration (Minutes)", y = "Frequency") +
    theme_minimal()

  ggsave(file.path(charts_dir, "duration_histogram.png"), plot = g, width = 10, height = 6)
}

create_hotspot_hour_heatmap <- function() {
  heatmap_data <- read_csv_or_stop("output/hive/hotspot_hour_matrix", c("hotspot_id", "usage_hour", "connection_count"))
  heatmap_matrix <- dcast(heatmap_data, hotspot_id ~ usage_hour, value.var = "connection_count", fill = 0)
  rownames(heatmap_matrix) <- heatmap_matrix$hotspot_id
  heatmap_matrix$hotspot_id <- NULL
  heatmap_matrix <- as.matrix(heatmap_matrix)

  png(file.path(charts_dir, "hotspot_hour_heatmap.png"), width = 1000, height = 700)
  heatmap(heatmap_matrix, main = "Hotspot x Hour Usage Heatmap", col = heat.colors(20), scale = "none")
  dev.off()
}

create_avg_duration_by_hotspot_chart <- function() {
  avg_duration_data <- read_csv_or_stop("output/hive/avg_duration_by_hotspot", c("hotspot_id", "avg_duration_minutes"))
  avg_duration_data <- avg_duration_data[order(avg_duration_data$avg_duration_minutes, decreasing = TRUE), ]
  avg_duration_data$hotspot_id <- factor(avg_duration_data$hotspot_id, levels = avg_duration_data$hotspot_id)

  g <- ggplot(avg_duration_data, aes(x = hotspot_id, y = avg_duration_minutes)) +
    geom_bar(stat = "identity", fill = "darkorange") +
    labs(title = "Average Duration by Hotspot", x = "Hotspot ID", y = "Average Duration (Minutes)") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

  ggsave(file.path(charts_dir, "avg_duration_by_hotspot.png"), plot = g, width = 10, height = 6)
}

create_summary_report <- function() {
  hotspot_data <- read_csv_or_stop("output/hive/hotspot_connections", c("hotspot_id", "connection_count"))
  device_data <- read_csv_or_stop("output/hive/device_distribution", c("device_type", "device_count"))
  hourly_data <- read_csv_or_stop("output/hive/hourly_usage", c("usage_hour", "connection_count"))
  if (nrow(hourly_data) > 0) {
    peak_hour <- hourly_data[which.max(hourly_data$connection_count), ]
  } else {
    peak_hour <- data.frame(usage_hour = NA, connection_count = NA)
  }

  most_used_hotspot <- hotspot_data[which.max(hotspot_data$connection_count), ]
  total_connections <- sum(hotspot_data$connection_count)
  total_hotspots <- nrow(hotspot_data)
  avg_device_count <- mean(device_data$device_count)

  report <- data.frame(
    metric = c(
      "total_connections",
      "total_hotspots",
      "avg_device_count",
      "peak_usage_hour",
      "peak_usage_count",
      "most_used_hotspot",
      "most_used_hotspot_connections"
    ),
    value = c(
      total_connections,
      total_hotspots,
      avg_device_count,
      if (is.na(peak_hour$usage_hour)) "N/A" else peak_hour$usage_hour,
      if (is.na(peak_hour$connection_count)) "N/A" else peak_hour$connection_count,
      if (nrow(most_used_hotspot) == 0) "N/A" else as.character(most_used_hotspot$hotspot_id),
      if (nrow(most_used_hotspot) == 0) "N/A" else most_used_hotspot$connection_count
    ),
    stringsAsFactors = FALSE
  )

  write.csv(report, file.path(reports_dir, "wifi_summary_report.csv"), row.names = FALSE)
}

run_wifi_visual_analysis <- function() {
  create_hotspot_connections_chart()
  create_usage_line_chart()
  create_data_usage_chart()
  create_device_distribution_chart()
  create_duration_histogram()
  create_hotspot_hour_heatmap()
  create_avg_duration_by_hotspot_chart()
  create_summary_report()
  message("Charts saved to: ", charts_dir)
  message("Summary report saved to: ", reports_dir)
}

run_wifi_visual_analysis()
