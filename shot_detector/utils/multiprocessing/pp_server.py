# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import pp


class GenServer(object):
    __logger = logging.getLogger(__name__)

    PPSERVERS = ('127.0.0.1',)

    def __init__(self, ppservers=None):
        if not ppservers:
            ppservers = self.PPSERVERS

        self.job_server = pp.Server(ppservers=ppservers)

        self.__logger.debug("Starting pp with %s workers",
                            self.job_server.get_ncpus())

    def submit(self, function, *args, **kwargs):
        job = self.job_server.submit(function, *args, **kwargs)

        # time.sleep(0.1)

        return job


gen_server = GenServer()
