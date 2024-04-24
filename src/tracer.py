import sys
import os
from texts.texts import TRACER_NAME
import inspect
from xes_writer import XesWriter
from types import FrameType as Frame, TracebackType as Traceback
import types
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import tracemalloc

class Tracer:
    def __init__(self, filename: str, verbose: bool = False, writing_mode: str = "CREATE",
                 output_file: str = "output.xes", trace_name: str = "trace", ignore_builtins: bool = False,
                 alloc_step: int = 1024, ignore_alloc: bool = False, command: List[str] = []) -> None:
        with open(filename, "r") as f:
            self.program = f.read()
            self.code = compile(self.program, filename, "exec")
        self.filename = filename
        self.old_trace = sys.getprofile()
        self.old_alloc_trace = sys.gettrace()
        self.verbose = verbose
        self.stack_len = 0
        self.tracer_filename = os.getcwd() + '/' + TRACER_NAME
        self.xes_writer = XesWriter(writing_mode=writing_mode, output_file=output_file, trace_name=trace_name)
        self.ignore_builtins = ignore_builtins
        self.memory_usage = 0
        self.alloc_step = alloc_step
        self.ignore_alloc = ignore_alloc
        self.command = command
    
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
        elif event == "c_call" and not self.ignore_builtins:
            self._c_call_callback(frame, arg)
        elif event == "c_return" and not self.ignore_builtins:
            self._c_return_callback(frame, arg)
        return self._trace 
    
    def _call_callback(self, frame: Frame) -> None:
        info = inspect.getframeinfo(frame)
        if info.function == "<module>":
            self.print_verbose("module", info.filename)
            self.xes_writer.generate_event("module", info.filename, info.lineno, timestamp=datetime.now())
        else:
            self.print_verbose("call", info.function)
            self.xes_writer.generate_event("call", info.function, info.lineno, timestamp=datetime.now())
        self.stack_len += 1
            
    def _return_callback(self, frame: Frame, arg: Any) -> None:
        self.stack_len -= 1
        info = inspect.getframeinfo(frame)
        if info.function == "<module>":
            self.print_verbose("module_return", info.filename)
            self.xes_writer.generate_event("module_return", info.filename, info.lineno, timestamp=datetime.now())
        else:
            self.print_verbose("return", info.function)
            self.xes_writer.generate_event("return", info.function, info.lineno, timestamp=datetime.now())
    
    def _c_call_callback(self, frame: Frame, arg: Any) -> None:
        info = inspect.getframeinfo(frame)
        if info.filename != self.tracer_filename:
            self.print_verbose("c_call", str(arg))
            self.xes_writer.generate_event("c_call", arg, info.lineno, timestamp=datetime.now())
            self.stack_len += 1
    
    def _c_return_callback(self, frame: Frame, arg: Any) -> None:
        info = inspect.getframeinfo(frame)
        if info.filename != self.tracer_filename:
            self.stack_len -= 1
            self.print_verbose("c_return", str(arg))
            self.xes_writer.generate_event("c_return", arg, info.lineno, timestamp=datetime.now())
    
    def _alloc_trace(self, frame: Frame, event: str, arg: Any):
        if event == 'line' and not self.ignore_alloc:
            # Смотрим на использование памяти
            snapshot = tracemalloc.take_snapshot()
            snapshot = snapshot.filter_traces([tracemalloc.Filter(True, self.filename)])
            stats = snapshot.statistics("filename")
            sum_ = sum([stat.size for stat in stats])
            # Проверка на объём изменения количества используемой памяти, чтобы не записывать лишнее
            if abs(self.memory_usage - sum_) > self.alloc_step:
                if self.memory_usage > sum_:
                    self.print_verbose("free", f"{self.memory_usage - sum_} in line {frame.f_lineno}")
                    self.xes_writer.generate_event(f"free", f"{self.memory_usage - sum_}",
                                                   frame.f_lineno, timestamp=datetime.now())
                else:
                    self.print_verbose("alloc", f"{sum_ - self.memory_usage} in line {frame.f_lineno}")
                    self.xes_writer.generate_event(f"alloc", f"{sum_ - self.memory_usage}",
                                                   frame.f_lineno, timestamp=datetime.now())
                self.memory_usage = sum_
        if event == 'exception':
            self.print_verbose("exception", arg[0])
            self.xes_writer.generate_event("exception", arg[0], frame.f_lineno, timestamp=datetime.now())
        return self._alloc_trace
        
    def _start(self) -> None:
        # Настраиваем глобальные переменные перед выполнением exec
        main_mod = types.ModuleType("__main__")
        setattr(main_mod, "__file__", os.path.abspath(self.filename))
        setattr(main_mod, "__builtins__", globals()["__builtins__"])
        # Следующая строка нужна для корректной работы pickle
        sys.modules["__main__"] = sys.modules["__mp_main__"] = main_mod
        sys.path.insert(0, os.path.dirname(self.filename))
        sys.argv = [self.filename] + self.command
        try:
            sys.setprofile(self._trace)
            sys.settrace(self._alloc_trace)
            exec(self.code, main_mod.__dict__)
        finally:
            sys.settrace(self.old_alloc_trace)
            sys.setprofile(self.old_trace)
            self.xes_writer.write()
