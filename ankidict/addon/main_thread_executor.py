"""Helper module delivering function decorator 'executes_in_main_thread'.

Functions decorated with this decorators may be called from any thread except
the main thread (in which case the main thread blocks forever). The calling
thread DON'T HAVE TO be a QThread, can be a vanilla python thread.

Any function decorated with this decorator will behave as follows:
1. send its code and arguments to main thread with event loop
2. block on thread-safe queue until the result appears
3. in main thread: execute function code, if it throws exception,
    post exception info to result queue, otherwise post function result
4. in calling thread: read result from queue and if it is exception info,
    re-raise it, otherwise return result
"""
import functools
try:
    from Queue import Queue
except ImportError:
    from queue import Queue # python 3.x

from aqt.qt import *
import aqt.qt as QtGui
import aqt
from PyQt4 import QtCore

from PyQt4.QtCore import pyqtSlot, pyqtSignal


class ExceptionInfo(object):
    def __init__(self):
        self.info = sys.exc_info()

    def re_raise(self):
        raise self.info[0], self.info[1], self.info[2]


class ProxyThread(QThread):
    callback_arrived = pyqtSignal(object)
    def __init__(self, queue):
        self.queue = queue
        super(ProxyThread, self).__init__()

    def run(self):
        while True:
            callback = self.queue.get()
            self.callback_arrived.emit(callback)


class ProxyObject(QObject):
    @pyqtSlot(object)
    def on_callback_arrived(self, callback):
        callback()


class MainThreadExecutor(object):
    def __init__(self):
        self.proxy_queue = Queue()
        self.proxy_thread = ProxyThread(self.proxy_queue)
        self.proxy_object = ProxyObject()
        self.proxy_thread.callback_arrived.connect(
            self.proxy_object.on_callback_arrived
        )
        aqt.mw.app.aboutToQuit.connect(self.proxy_thread.terminate)
        self.proxy_thread.start()


_executor = MainThreadExecutor()


def function_executes_in_main_thread(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        # one-element queue to pass function result
        result_queue = Queue()
        # callback to be executed in Qt main loop
        def callback_to_send():
            try:
                direct_result = func(*args, **kwargs)
            except:
                direct_result = ExceptionInfo()
            result_queue.put(direct_result)
        # send the callback to qt main loop
        _executor.proxy_queue.put(callback_to_send)
        # wait for the callback to finish
        indirect_result = result_queue.get()
        # in case an error occured, re-raise the exception
        if isinstance(indirect_result, ExceptionInfo):
            indirect_result.re_raise()
        else:
            return indirect_result
    return newfunc


def class_executes_in_main_thread(cls):
    raise Exception("This is only a function decorator by now.")


def executes_in_main_thread(thing):
    if isinstance(thing, type):
        return class_executes_in_main_thread(thing)
    elif callable(thing):
        return function_executes_in_main_thread(thing)
    else:
        raise Exception(
            "Invalid argument: not a class and not callable."
            "'executes_in_main_thread' should be used as a decorator."
        )
