import logging


class Logger:

    def __init__(self,name,log_file='sample.log', level=logging.INFO):
        self.formatter = logging.Formatter('{:<28}   :   {:<35}   :   {:<70}'.format('Time logged = %(asctime)s','Function name = %(funcName)s','message= %(message)s'))
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setFormatter(self.formatter)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(self.file_handler)
