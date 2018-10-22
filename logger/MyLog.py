import logging
import os
import types
from functools import wraps


class MyLog:
    def __init__(self, func):
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        logging.info('*************** pid=%d, %s is begin **************' % (os.getpid(), self.__wrapped__.__name__))
        res = self.__wrapped__(*args, **kwargs)
        logging.info('############### pid=%d, %s is end ###############' % (os.getpid(), self.__wrapped__.__name__))
        return res

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)