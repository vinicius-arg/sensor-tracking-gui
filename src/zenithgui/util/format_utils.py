class FormatUtils:
    @staticmethod
    def get_fancy_name(raw_name, dictionary: dict[str, str]):
        for key, value in dictionary.items():
            if raw_name not in key:
                continue

            return value if (raw_name in key) else raw_name