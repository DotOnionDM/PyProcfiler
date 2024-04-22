import sys
from argparser import Parser
from tracer import Tracer



if __name__ == "__main__":
    parser = Parser()
    parser.parse(sys.argv)
    tracer = Tracer(parser.options.file, verbose=parser.options.verbose)
    tracer.start_tracing()
    
    