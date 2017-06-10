import logging


def make_logger(logname):
    l = logging.getLogger(logname)
    formater = logging.Formatter('%(relativeCreated)6d %(threadName)s %(message)s')
    fileHandler = logging.FileHandler(logname)
    fileHandler.setFormatter(formater)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formater)

    l.setLevel(logging.DEBUG)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)
    return l
