#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import sys, time


class ProgressBar(object):
    def __init__(self, count=0, total=0, width=50):
        self.count = count
        self.total = total
        self.width = width

    def move(self, size):
        self.count += size

    def log(self):
        sys.stdout.write(' ' * (self.width + 20) + '\r')
        sys.stdout.flush()
        # print(s)
        progress = int(self.width * self.count / self.total)
        sys.stdout.write('{0}%: '.format(int(100*self.count/self.total)))
        sys.stdout.write('#' * progress + '-' * (self.width - progress) + '\r')
        sys.stdout.flush()
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()


if __name__ == '__main__':
    b = ProgressBar(total=20)
    for i in range(20):
        b.move(1)
        # b.log('We have arrived at: ' + str(i + 1))
        time.sleep(1)