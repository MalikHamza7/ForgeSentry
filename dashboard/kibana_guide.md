# Threat Intelligence Dashboard Guide (Kibana)

Since the dashboard needs to be created in the Kibana UI, follow these steps once your honeypot is live.

## 1. Access Kibana
- URL: `http://<VPS_IP>:5601`
- Navigate to **Stack Management > Index Patterns**.
- Create a new index pattern for `honeypot-logs-*`.
- Select `@timestamp` as the time field.

## 2. Visualize Attacks in "Lens"
Go to **Visualize Library > Create new virtualization > Lens**.

### Widget A: Attack Map (GeoIP)
*Note: Requires Logstash GeoIP plugin enabled (default in many setups).*
- **Visualization Type**: Maps.
- **Layer**: Documents.
- **Index**: `honeypot-logs-*`.
- **Field**: `geoip.location`.
- **Metric**: Count.
- **Description**: Shows where attacks are originating worldwide.

### Widget B: Top Attack Commands
- **Visualization Type**: Data Table.
- **Rows**: `input.keyword` (Top 10).
- **Metric**: Count.
- **Description**: Shows the most frequent commands commands typed by attackers.

### Widget C: Attacks Over Time
- **Visualization Type**: Area Chart.
- **X-axis**: `@timestamp`.
- **Y-axis**: Count.
- **Break down by**: `sensor_type` (Top 5).
- **Description**: Visualizes attack spikes against Cowrie vs Conpot.

## 3. Create Dashboard
- Go to **Dashboard > Create new dashboard**.
- Click **Add from library** and select the visualizations created above.
- Save as "Global Threat Overview".
