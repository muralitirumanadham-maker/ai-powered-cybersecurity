from pathlib import Path
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
OUT = Path("data/demo_network_traffic.csv")


def make_rows(n_each=250):
    rows = []

    def add(label, n, protocol="TCP"):
        for _ in range(n):
            if label == "BENIGN":
                duration = RNG.uniform(1, 30)
                src = RNG.uniform(100, 5000)
                dst = RNG.uniform(100, 12000)
                packets = RNG.integers(5, 100)
                syn = RNG.integers(0, 4)
                ack = RNG.integers(1, 60)
                failed = RNG.integers(0, 2)
                ports = RNG.integers(1, 5)
                dport = int(RNG.choice([53, 80, 443, 22, 123]))
            elif label == "PORT_SCAN":
                duration = RNG.uniform(0.1, 5)
                src = RNG.uniform(50, 1000)
                dst = RNG.uniform(20, 500)
                packets = RNG.integers(30, 250)
                syn = RNG.integers(20, 180)
                ack = RNG.integers(0, 15)
                failed = RNG.integers(0, 3)
                ports = RNG.integers(15, 80)
                dport = int(RNG.integers(1, 65535))
            elif label == "BRUTE_FORCE":
                duration = RNG.uniform(10, 90)
                src = RNG.uniform(500, 5000)
                dst = RNG.uniform(100, 3000)
                packets = RNG.integers(50, 500)
                syn = RNG.integers(1, 15)
                ack = RNG.integers(20, 200)
                failed = RNG.integers(8, 60)
                ports = RNG.integers(1, 4)
                dport = int(RNG.choice([21, 22, 23, 3389]))
            elif label == "DOS":
                duration = RNG.uniform(0.05, 4)
                src = RNG.uniform(5000, 50000)
                dst = RNG.uniform(100, 5000)
                packets = RNG.integers(500, 5000)
                syn = RNG.integers(100, 3000)
                ack = RNG.integers(0, 300)
                failed = RNG.integers(0, 5)
                ports = RNG.integers(1, 8)
                dport = int(RNG.choice([80, 443, 53]))
            else:  # DATA_EXFILTRATION
                duration = RNG.uniform(20, 180)
                src = RNG.uniform(100000, 1000000)
                dst = RNG.uniform(500, 10000)
                packets = RNG.integers(500, 10000)
                syn = RNG.integers(0, 10)
                ack = RNG.integers(100, 5000)
                failed = RNG.integers(0, 3)
                ports = RNG.integers(1, 3)
                dport = int(RNG.choice([443, 8443, 22]))

            total = src + dst
            bpp = total / max(packets, 1)
            rate = packets / max(duration, 0.1)

            rows.append({
                "duration": round(duration, 3),
                "protocol": protocol,
                "src_bytes": round(src, 2),
                "dst_bytes": round(dst, 2),
                "packets": int(packets),
                "bytes_per_packet": round(bpp, 2),
                "syn_count": int(syn),
                "ack_count": int(ack),
                "failed_logins": int(failed),
                "unique_dst_ports": int(ports),
                "dst_port": dport,
                "flow_rate": round(rate, 2),
                "threat": label,
            })

    for label in ["BENIGN", "PORT_SCAN", "BRUTE_FORCE", "DOS", "DATA_EXFILTRATION"]:
        add(label, n_each)

    return pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df = make_rows()
    df.to_csv(OUT, index=False)
    print(f"Wrote {len(df)} rows to {OUT}")
