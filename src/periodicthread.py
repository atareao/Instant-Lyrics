#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import threading


class PeriodicThread(object):
    """
    Python periodic Thread using Timer with instant cancellation
    """

    def __init__(self, callback=None, period=1, name=None, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.callback = callback
        self.period = period
        self.stop = False
        self.current_timer = None
        self.schedule_lock = threading.Lock()
        self.first_thread = None

    def start(self):
        """
        Mimics Thread standard start method
        """
        # self.first_thread = threading.Thread(None, self._first_run,
        # self.name, *self.args, **self.kwargs)
        # self.first_thread.start()
        self.schedule_timer()

    def run(self):
        """
        By default run callback. Override it if you want to use inheritance
        """
        if self.callback is not None:
            self.callback()

    def _run(self):
        """
        Run desired callback and then reschedule Timer
        (if thread is not stopped)
        """
        try:
            self.run()
        except Exception as e:
            print(e)
            logging.exception("Exception in running periodic thread")
        finally:
            with self.schedule_lock:
                if not self.stop:
                    self.schedule_timer()

    def schedule_timer(self):
        """
        Schedules next Timer run
        """
        self.current_timer = threading.Timer(
            self.period, self._run, *self.args, **self.kwargs)
        if self.name:
            self.current_timer.name = self.name

        self.current_timer.start()

    def _first_run(self):
        self._run()
        self.schedule_timer()

    def cancel(self):
        """
        Mimics Timer standard cancel method
        """
        with self.schedule_lock:
            self.stop = True
            if self.current_timer is not None:
                self.current_timer.cancel()

    def join(self):
        """
        Mimics Thread standard join method
        """
        self.current_timer.join()

    def isAlive(self):
        return (self.first_thread is not None and
                self.first_thread.isAlive()) or (
                    self.current_timer is not None and
                    self.current_timer.isAlive())
