import sys
from argparser import Parser
from tracer import Tracer



if __name__ == "__main__":
    parser = Parser()
    parser.parse(sys.argv)
    writing_mode = parser.options.writing_mode.upper() if parser.options.writing_mode is not None else "CREATE"
    output_file = parser.options.output_file if parser.options.output_file is not None else "output.xes"
    trace_name = parser.options.trace_name if parser.options.trace_name is not None else "trace"
    tracer = Tracer(parser.options.file, verbose=parser.options.verbose, writing_mode=writing_mode, 
                    output_file=output_file, trace_name=trace_name)
    tracer.start_tracing()
    