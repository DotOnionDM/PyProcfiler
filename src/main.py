import sys
import json
from argparser import Parser
from tracer import Tracer

def invoke_tracer(parser: Parser) -> Tracer:
    writing_mode = "CREATE"
    output_file = "output.xes"
    trace_name = "trace"
    ignore_builtins = False
    verbose = False
    if parser.options.config_file is not None:
        with open(parser.options.config_file, "r") as f:
            config = json.load(f)
            if "verbose" in config:
                verbose = config["verbose"]
            if "writing_mode" in config:
                writing_mode = config["writing_mode"]
            if "output_file" in config:
                output_file = config["output_file"]
            if "trace_name" in config:
                trace_name = config["trace_name"]
            if "ignore_builtins" in config:
                ignore_builtins = config["ignore_builtins"]

    ignore_builtins = parser.options.ignore_builtins if parser.options.ignore_builtins else ignore_builtins
    verbose = parser.options.verbose if parser.options.verbose else verbose
    writing_mode = parser.options.writing_mode.upper() if parser.options.writing_mode is not None else writing_mode
    output_file = parser.options.output_file if parser.options.output_file is not None else output_file
    trace_name = parser.options.trace_name if parser.options.trace_name is not None else trace_name
    tracer = Tracer(parser.options.file, verbose=verbose, writing_mode=writing_mode, 
                    output_file=output_file, trace_name=trace_name, ignore_builtins=ignore_builtins)
    return tracer

if __name__ == "__main__":
    parser = Parser()
    parser.parse(sys.argv)
    tracer = invoke_tracer(parser)
    tracer.start_tracing()
    