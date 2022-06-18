import datetime

class logging():
    Logname = 'log.txt'
    def __init__(self) -> None:
       self.log = open(self.Logname, 'a')
    
    def log(self, message: str) -> None:
        self.log.write(f"{datetime.datetime.now()} - {message}\n")
