from texts.texts import VERSION_INFO, HELP
import argparse
from patterns.singleton import Singleton
from typing import Any, Dict, List, Optional, Tuple

class Parser(metaclass=Singleton):
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(prog="python3 main.py")
        self.parser.add_argument("--version", action="store_true", default=None, help=HELP["version"])
        self.parser.add_argument("--verbose", action="store_true", default=None, help=HELP["verbose"])
        self.parser.add_argument("--output_file", nargs="?", default=None, help=HELP["output_file"])
        self.parser.add_argument("--writing_mode", nargs="?", default=None, help=HELP["writing_mode"])
        self.parser.add_argument("--trace_name", nargs="?", default=None, help=HELP["trace_name"])
        self.parser.add_argument("--ignore_builtins", action="store_true", default=None, help=HELP["ignore_builtins"])
        self.parser.add_argument("--config_file", nargs="?", default=None, help=HELP["config_file"])
        self.parser.add_argument("--set_alloc_step", nargs="?", default=None, help=HELP["set_alloc_step"])
        self.parser.add_argument("--ignore_alloc", action="store_true", default=None, help=HELP["ignore_alloc"])
        self.parser.add_argument("file", help=HELP["file"])
        
    def parse(self, argv: List[str]) -> None:
        self.options = self.parser.parse_args(argv[1:])
        self.data = {}
        if self.options.version:
            print(VERSION_INFO)
            exit(0)
            

