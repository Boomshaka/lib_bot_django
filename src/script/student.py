from .logger import Logger


class Student:

    def __init__(self, username, password):
        self.username = username
        self.email = username + "@ucsb.edu"
        self.password = password
        self.logger = Logger(name = self.username, log_file = f"../logs/{self.username}.log")
        self.log = self.logger.logger

    

    
    