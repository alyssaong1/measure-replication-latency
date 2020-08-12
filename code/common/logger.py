from datetime import datetime
from pathlib import Path

class Logger():

    def __init__(self, path, fileName):
        Path(path).mkdir(parents=True, exist_ok=True) # Create folder if not exists
        open(f"{path}/{fileName}", 'w+') # Create file
        self.filepath = f"{path}/{fileName}"
        
    def log(self, line):
        with open(self.filepath, "a") as file:
            file.write(line)

    def logWithNewLine(self, line):
        with open(self.filepath, "a") as file:
            file.write(line)
            file.write("\n")

    def logBalance(self, runId, operation, region, result):
        formatted_result = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{runId},{result['updated_at']},{result['timestamp']},{result['userId']}"
        self.logWithNewLine(formatted_result)