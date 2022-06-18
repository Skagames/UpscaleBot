import datetime

class log():
    def __init__(self,message) -> None:
        with open("log.txt", "a") as log:
            log.write(f"{datetime.datetime.now()} - {message}\n")

