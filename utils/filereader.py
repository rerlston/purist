class FileReader:
    def read(self, filename: str) -> str:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
