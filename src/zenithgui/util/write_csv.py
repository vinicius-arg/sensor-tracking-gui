import time
import pandas as pd

from pathlib import Path

def write_csv(data: dict[str, list], p: str):
    try:
        path = Path(p)
        path.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(data)
        _id = str(time.time())[-6:]

        file_path = f"{path.joinpath("Tracking_record_")}{_id}.csv"

        df.to_csv(file_path, index=False)

        return True
    except (OSError, ValueError):
        return False

def main():
    data = {"a": [1,2,3], "b": [4,5,6]}

if __name__ == "__main__":
    main()