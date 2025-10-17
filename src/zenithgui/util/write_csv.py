import time
import pandas as pd

from pathlib import Path

def write_csv(data: dict[str, list], p: str):
    path = Path(p)
    df = pd.DataFrame(data)
    _id = str(time.time())[-6:]
    df.to_csv(f"{path.joinpath("Tracking_record_")}{_id}.csv")

def main():
    data = {"a": [1,2,3], "b": [4,5,6]}

if __name__ == "__main__":
    main()