from texts.texts import *
import argparse
from typing import Any, Dict, List, Optional, Tuple

class Parser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(prog="python3 main.py")
        self.parser.add_argument("--version", action="store_true", default=False, help="show version of PyProcfiler")
        self.parser.add_argument("--show_dunders", action="store_true", default=False, help="show variables which start with two underscores")
        self.parser.add_argument("file", help="the file to trace")
        
    def parse(self, argv: List[str]) -> List[str]:
        self.options = self.parser.parse_args(argv[1:])
        self.data = {}
        if self.options.version:
            print(VERSION_INFO)
            exit(0)
        self.data["show_dunders"] = self.options.show_dunders

