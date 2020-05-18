# -*- coding: utf-8 -*-
from lb import make_io_app


application, io = make_io_app('dev')


if __name__ == '__main__':
    io.run(application)
