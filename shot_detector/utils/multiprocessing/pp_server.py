# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

# noinspection PyUnresolvedReferences
import pp


class GenServer(object):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    PP_SERVERS = ('127.0.0.1',)

    def __init__(self, pp_servers=None):
        """
        
        :param pp_servers: 
        """
        if not pp_servers:
            pp_servers = self.PP_SERVERS

        self.job_server = pp.Server(ppservers=pp_servers)

        self.__logger.debug("Starting pp with %s workers",
                            self.job_server.get_ncpus())

    def submit(self, func, *args, **kwargs):
        """
        
        :param func: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        job = self.job_server.submit(func, *args, **kwargs)

        # time.sleep(0.1)

        return job


gen_server = GenServer()
