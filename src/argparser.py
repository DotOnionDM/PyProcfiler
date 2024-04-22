from texts.texts import VERSION_INFO
import argparse
from typing import Any, Dict, List, Optional, Tuple

class Parser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(prog="python3 main.py")
        self.parser.add_argument("--version", action="store_true", default=False, help="show version of PyProcfiler")
        self.parser.add_argument("--verbose", action="store_true", default=False, help="show console log")
        self.parser.add_argument("--output_file", nargs="?", default=None, help="output file")
        self.parser.add_argument("--writing_mode", nargs="?", default=None, help="mode of writing (CREATE|APPEND)")
        self.parser.add_argument("--trace_name", nargs="?", default=None, help="id of the trace")
        self.parser.add_argument("file", help="the file to trace")
        
    def parse(self, argv: List[str]) -> None:
        self.options = self.parser.parse_args(argv[1:])
        self.data = {}
        if self.options.version:
            print(VERSION_INFO)
            exit(0)
            

