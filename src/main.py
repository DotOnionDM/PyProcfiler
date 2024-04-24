import sys
import json
from argparser import Parser
from tracer import Tracer
import tracemalloc

def invoke_tracer(parser: Parser) -> Tracer:
    writing_mode = "CREATE"
    output_file = "output.xes"
    trace_name = "trace"
    ignore_builtins = False
    verbose = False
    alloc_step = 1024
    ignore_alloc = False
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
            if "set_alloc_step" in config:
                alloc_step = int(config["set_alloc_step"])
            if "ignore_alloc" in config:
                ignore_alloc = config["ignore_alloc"]
                
    ignore_builtins = parser.options.ignore_builtins if parser.options.ignore_builtins is not None else ignore_builtins
    verbose = parser.options.verbose if parser.options.verbose is not None else verbose
    writing_mode = parser.options.writing_mode.upper() if parser.options.writing_mode is not None else writing_mode
    output_file = parser.options.output_file if parser.options.output_file is not None else output_file
    trace_name = parser.options.trace_name if parser.options.trace_name is not None else trace_name
    alloc_step = int(parser.options.set_alloc_step) if parser.options.set_alloc_step is not None else alloc_step
    ignore_alloc = parser.options.ignore_alloc if parser.options.ignore_alloc is not None else ignore_alloc
    if alloc_step < 0:
        raise Exception("alloc_step must be greater than or equal to 0")
    tracer = Tracer(parser.options.file, verbose=verbose, writing_mode=writing_mode, 
                    output_file=output_file, trace_name=trace_name, ignore_builtins=ignore_builtins,
                    alloc_step=alloc_step, ignore_alloc=ignore_alloc, command=parser.command)
    return tracer

if __name__ == "__main__":
    parser = Parser()
    parser.parse(sys.argv)
    tracer = invoke_tracer(parser)
    tracemalloc.start()
    tracer.start_tracing()
    