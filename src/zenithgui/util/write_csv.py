import pandas as pd

def write_csv(data: dict[str, list], path: str):
    df = pd.DataFrame(data)
    df.to_csv(f"{path}.csv")

def main():
    data = {"a": [1,2,3], "b": [4,5,6]}

if __name__ == "__main__":
    main()