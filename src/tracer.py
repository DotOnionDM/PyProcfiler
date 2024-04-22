import sys
import os
from texts.texts import TRACER_NAME
import inspect
from xes_writer import XesWriter
from types import FrameType as Frame, TracebackType as Traceback
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

class Tracer:
    def __init__(self, filename: str, verbose: bool = False, writing_mode: str = "CREATE",
                 output_file: str = "output.xes", trace_name: str = "trace") -> None:
        with open(filename, "r") as f:
            self.program = f.read()
            self.code = compile(self.program, filename, "exec")
        self.old_trace = sys.getprofile()
        self.verbose = verbose
        self.stack_len = 0
        self.tracer_filename = os.getcwd() + '/' + TRACER_NAME
        self.xes_writer = XesWriter(writing_mode=writing_mode, output_file=output_file, trace_name=trace_name)
    
    def start_tracing(self) -> None:
        self._start()
    
    def print_verbose(self, type: str, data: str) -> None:
        if self.verbose:
            print("  " * self.stack_len + f"{type}: {data}")
    
    def _trace(self, frame: Frame, event: str, arg: Any):
        if event == "call":
            self._call_callback(frame)
        elif event == "return":
            self._return_callback(frame, arg)
        elif event == "c_call":
            self._c_call_callback(frame, arg)
        elif event == "c_return":
            self._c_return_callback(frame, arg)
        return self._trace 
    
    def _call_callback(self, frame: Frame) -> None:
        info = inspect.getframeinfo(frame)
        if info.function == "<module>":
            self.print_verbose("module", info.filename)
            self.xes_writer.generate_event("module", info.filename, timestamp=datetime.now())
        else:
            self.print_verbose("call", info.function)
            self.xes_writer.generate_event("call", info.function, timestamp=datetime.now())
        self.stack_len += 1
            
    def _return_callback(self, frame: Frame, arg: Any) -> None:
        self.stack_len -= 1
        info = inspect.getframeinfo(frame)
        if info.function == "<module>":
            self.print_verbose("module_return", info.filename)
            self.xes_writer.generate_event("module_return", info.filename, timestamp=datetime.now())
        else:
            self.print_verbose("return", info.function + " " + str(arg))
            self.xes_writer.generate_event("return", info.function, timestamp=datetime.now())
    
    def _c_call_callback(self, frame: Frame, arg: Any) -> None:
        info = inspect.getframeinfo(frame)
        if info.filename != self.tracer_filename:
            self.print_verbose("c_call", str(arg))
            self.xes_writer.generate_event("c_call", arg, timestamp=datetime.now())
            self.stack_len += 1
    
    def _c_return_callback(self, frame: Frame, arg: Any) -> None:
        info = inspect.getframeinfo(frame)
        if info.filename != self.tracer_filename:
            self.stack_len -= 1
            self.print_verbose("c_return", str(arg))
            self.xes_writer.generate_event("c_return", arg, timestamp=datetime.now())
        
    def _start(self) -> None:
        try:
            sys.setprofile(self._trace)
            exec(self.code, {})
        finally:
            sys.setprofile(self.old_trace)
            self.xes_writer.write()
    
    
