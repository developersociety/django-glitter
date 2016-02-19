# -*- coding: utf-8 -*-


class Column(object):

    creation_counter = 0

    def __init__(self, verbose_name=None, width=0):
        self.verbose_name = verbose_name
        self.width = width

        self.creation_counter = Column.creation_counter
        Column.creation_counter += 1
