import sys
import inspect
from types import FrameType as Frame, TracebackType as Traceback
from typing import Any, Dict, List, Optional, Tuple

class Tracer:
    def __init__(self, filename: str, args: List[str] = [], show_dunders: bool = False) -> None:
        with open(filename, "r") as f:
            self.program = f.read()
            self.code = compile(self.program, filename, "exec")
        self.old_trace = sys.gettrace()
        self.show_dunders = show_dunders
    
    def start_tracing(self) -> None:
        self._start()
    
    def _trace(self, frame: Frame, event: str, arg: Any):
        if event == "call":
            self._call_callback(frame)
        elif event == "return":
            self._return_callback(frame, arg)          
        return self._trace 
    
    def _call_callback(self, frame: Frame) -> None:
        info = inspect.getframeinfo(frame)
        if info.function == "<module>":
            print(f"module: {info.filename}")
        else:
            print(f"call: {info.function}")
            
    def _return_callback(self, frame: Frame, arg: Any) -> None:
        info = inspect.getframeinfo(frame)
        if info.function == "<module>":
            print(f"module: {info.filename}")
        else:
            print(f"return: {info.function} {arg!r}")
    
    def _start(self) -> None:
        try:
            sys.settrace(self._trace)
            exec(self.code, {})
        finally:
            sys.settrace(self.old_trace)
    
    
