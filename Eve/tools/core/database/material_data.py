class MaterialData:
    def __init__(self, SQL_FILE_PATH):
        # Load database
        self.SQL_FILE_PATH = SQL_FILE_PATH

        # Data attributes
        self.material = None