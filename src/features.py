FEATURE_COLUMNS = [
    "duration",
    "protocol",
    "src_bytes",
    "dst_bytes",
    "packets",
    "bytes_per_packet",
    "syn_count",
    "ack_count",
    "failed_logins",
    "unique_dst_ports",
    "dst_port",
    "flow_rate",
]

NUMERIC_COLUMNS = [
    "duration",
    "src_bytes",
    "dst_bytes",
    "packets",
    "bytes_per_packet",
    "syn_count",
    "ack_count",
    "failed_logins",
    "unique_dst_ports",
    "dst_port",
    "flow_rate",
]


def prepare_features(df):
    result = df.copy()
    result["protocol"] = result["protocol"].astype(str).str.upper()
    for col in NUMERIC_COLUMNS:
        result[col] = result[col].astype(float)
    return result[FEATURE_COLUMNS]
