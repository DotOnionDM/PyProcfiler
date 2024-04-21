import sys
from argparser import *
from tracer import Tracer



if __name__ == "__main__":
    parser = Parser()
    parser.parse(sys.argv)
    tracer = Tracer(parser.options.file, show_dunders=parser.data["show_dunders"])
    tracer.start_tracing()
    
    