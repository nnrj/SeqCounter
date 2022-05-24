#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from SeqCounter import SeqCounter

if __name__ == "__main__":
    seqCounter = SeqCounter()
    seqCounter.get_args(sys.argv[1:])
    seqCounter.run()
