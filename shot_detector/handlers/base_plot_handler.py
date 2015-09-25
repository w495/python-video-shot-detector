# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from collections import OrderedDict
import logging

import matplotlib.pyplot as plt
from shot_detector.objects          import SmartDict


# plt.rc('text', usetex=True)
plt.rc('font', family='DejaVu Sans')



class BasePlotHandler(object):

    __logger = logging.getLogger(__name__)
    __plot_buffer = OrderedDict()
    __line_list = []

    def add_data(self, name, key, value, slyle='', *args, **kwargs):
        if not self.__plot_buffer.get(name):
            self.__plot_buffer[name] = SmartDict(
                x_list=[],
                y_list=[],
                slyle=slyle,
                options={}
            )
        self.__plot_buffer[name].x_list += [key]
        self.__plot_buffer[name].y_list += [value]
        self.__plot_buffer[name].slyle = slyle
        self.__plot_buffer[name].options = kwargs

    def plot_data(self, name=None):
        if name:
            self.plot_data_name(name)
        else:
            for name in self.__plot_buffer:
                self.plot_data_name(name)
        plt.legend(handles=self.__line_list)
        plt.show()

    def plot_data_name(self, name):
        key_value = self.__plot_buffer.get(name)
        if (key_value):
            line, = plt.plot(
                key_value.x_list,
                key_value.y_list,
                key_value.slyle,
                label=name,
                **key_value.options
            )
            self.__line_list += [line]
