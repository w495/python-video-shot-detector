# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
from collections import OrderedDict

import matplotlib.pyplot as plt

from shot_detector.utils.collections import SmartDict

# plt.rc('text', usetex=True)
plt.rc('font', family='DejaVu Sans')


class BasePlotHandler(object):
    __logger = logging.getLogger(__name__)
    __plot_buffer = OrderedDict()
    __line_list = []

    xlabel = '$t$'
    ylabel = '$L_1$'

    def add_data(self, name, key, value, style='', **kwargs):

        if not self.__plot_buffer.get(name):
            self.__plot_buffer[name] = SmartDict(
                x_list=[],
                y_list=[],
                style=style,
                options={}
            )
        self.__plot_buffer[name].x_list += [key]
        self.__plot_buffer[name].y_list += [value]
        self.__plot_buffer[name].style = style
        self.__plot_buffer[name].options = kwargs

    def plot_data(self, name=None):
        if name:
            self.plot_data_name(name)
        else:
            for name in self.__plot_buffer:
                self.plot_data_name(name)
        plt.legend(handles=self.__line_list)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        plt.show()
        # plt.savefig('foo.pdf')

    def plot_data_name(self, name):
        key_value = self.__plot_buffer.get(name)
        if key_value:
            if key_value.options.pop('axvline', False):
                for x in key_value.x_list:
                    plt.axvline(x, label=name, **key_value.options)
            else:
                line, = plt.plot(
                    key_value.x_list,
                    key_value.y_list,
                    key_value.style,
                    label=name,
                    **key_value.options
                )
                self.__line_list += [line]
