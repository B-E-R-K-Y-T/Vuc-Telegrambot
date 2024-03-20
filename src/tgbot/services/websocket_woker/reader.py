class DataReader:
    def __init__(self, raw_data: str):
        self.__data: dict = self.build_data(raw_data)

    @staticmethod
    def build_data(raw_data: str) -> dict:
        res: dict = {}

        for item in raw_data.split(","):
            k, v = item.split("=")
            if v.isnumeric():
                res[k] = int(v)

            res[k] = v

        return res

    def get_data(self) -> dict:
        return self.__data
