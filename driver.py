#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Web Driver
"""

from time import sleep

class DriverWrapper(object):
    """
    Wrapped driver. Insert sleep operation for loading page.
    """
    def __init__(self, driver):
        self.driver = driver

    def __getattr__(self, attr):
        orig_attr = self.driver.__getattribute__(attr)
        if callable(orig_attr):
            def _hooked(*args, **kwargs):
                result = orig_attr(*args, **kwargs)
                # prevent driver from becoming unwrapped
                if result == self.driver:
                    return self
                self.__post(attr)
                return result
            return _hooked
        else:
            return orig_attr

    def __post(self, attr):
        if attr == 'get':
            sleep(5)
        elif attr == 'find_element_by_xpath':
            sleep(1)
