import sys
import traceback
from types import FrameType as Frame, TracebackType as Traceback
from typing import Any, Dict, List, Optional, Tuple

class Tracer:
    def __init__(self, filename: str, args: List[str] = [], show_dunders: bool = False) -> None:
        with open(filename, "r") as f:
            self.program = f.read()
            self.code = compile(self.program)
    
    def trace(self):
        pass
    
    def _start(self):
        pass
    
    def _end(self):
        pass
    
    
