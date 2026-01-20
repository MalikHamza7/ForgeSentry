import argparse
import json
import pandas as pd
from elasticsearch import Elasticsearch
import os
from datetime import datetime

def fetch_from_es(es_host='localhost', index_pattern='honeypot-logs-*', size=10000):
    """Fetch logs from Elasticsearch."""
    es = Elasticsearch([{'host': es_host, 'port': 9200, 'scheme': 'http'}])
    
    if not es.ping():
        print(f"Error: Could not connect to Elasticsearch at {es_host}:9200")
        return pd.DataFrame()

    # Query to get all documents
    query = {
        "query": {
            "match_all": {}
        }
    }

    try:
        res = es.search(index=index_pattern, body=query, size=size)
        hits = res['hits']['hits']
        data = [hit['_source'] for hit in hits]
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def load_json_log(filepath):
    """Load logs directly from a cowrie.json file (offline mode)."""
    data = []
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return pd.DataFrame()
        
    with open(filepath, 'r') as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return pd.DataFrame(data)

def process_logs(df):
    """Extract relevant features for ML."""
    if df.empty:
        return df

    # Normalize fields (some might be missing in different events)
    cols = ['timestamp', 'src_ip', 'session', 'eventid', 'message', 'input', 'sensor_type']
    
    # Ensure columns exist
    for col in cols:
        if col not in df.columns:
            df[col] = None
            
    # Filter for interesting events (commands, logins)
    # Cowrie typical event IDs: cowrie.command.input, cowrie.login.success, cowrie.login.failed
    
    return df[cols]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Honeypot Logs")
    parser.add_argument('--source', type=str, choices=['es', 'file'], default='file', help="Source: 'es' (Elasticsearch) or 'file' (JSON log)")
    parser.add_argument('--path', type=str, default='deployment/cowrie/var/log/cowrie/cowrie.json', help="Path to JSON log file")
    parser.add_argument('--host', type=str, default='localhost', help="Elasticsearch host")
    parser.add_argument('--output', type=str, default='honey_data.csv', help="Output CSV filename")
    
    args = parser.parse_args()
    
    print(f"Fetching data from {args.source}...")
    
    if args.source == 'es':
        df = fetch_from_es(es_host=args.host)
    else:
        df = load_json_log(args.path)
        
    print(f"Raw data shape: {df.shape}")
    
    clean_df = process_logs(df)
    
    if not clean_df.empty:
        clean_df.to_csv(args.output, index=False)
        print(f"Saved processed data to {args.output}")
    else:
        print("No data found or extracted.")
