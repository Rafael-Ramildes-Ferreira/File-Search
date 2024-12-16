from dataclasses import dataclass
from pathlib import Path
import inspect
import sys
import os
import re

from terminalController import Terminal
import threadPoolLib


class FileSearchTask(threadPoolLib.Task): pass

class FileSearchTask(threadPoolLib.Task):
    dir : Path
    pattern : str

    def __init__(self, _pattern : str, path : Path) -> None:
        self.dir = path
        self.pattern = _pattern

    def exec(self) -> FileSearchTask | list[FileSearchTask]:
		# looks the stack to find a reference to the Worker
		# a worker method is one layer above in thye stack ([1])
		# and has an local variable called 'self'
        worker : threadPoolLib.Worker = inspect.stack()[1][0].f_locals['self']
        files = [item for item in Path.iterdir(self.dir) if os.path.isfile(item)]
        for file in files:
            if re.search(self.pattern,str(file)):
                worker.debug_print(file)
                # Terminal.print(file)

        return [FileSearchTask(self.pattern,item) for item in Path.iterdir(self.dir) if os.path.isdir(item)]


class FileSearchCLI:
    @staticmethod
    def get_inital_task() -> FileSearchTask:
        pattern : str
        path = Path(".")

        match len(sys.argv):
            case 1:
                Terminal.print("At least one positional argument is required:")
                Terminal.print("\tpython[3] FileSearch.py <pattern> [<base directory>]")
                exit()
            case 2:
                pattern = FileSearchCLI.read_pattern()
            case 3:
                pattern = FileSearchCLI.read_pattern()
                path = FileSearchCLI.read_base_path()
            case _:
                Terminal.print("Unexpected number of arguments")
                path = FileSearchCLI.print_help()

        return FileSearchTask(pattern,path)

    @staticmethod
    def print_help() -> None:
        Terminal.print("Usage:")
        Terminal.print("\tpython[3] FileSearch.py <pattern> [<base directory>]")
        Terminal.print("Existing flags:")
        Terminal.print("\t-h --help:\t Display how to use the program")

    @staticmethod
    def read_pattern() -> str:
        match sys.argv[1]:
            case "--help" | "-h":
                Terminal.print("Prints every occurence of a given pattern in evey subdirectory")
                FileSearchCLI.print_help()
                exit()
            case str() if sys.argv[1].startswith("-"):
                Terminal.print(f"Unknown flag or argument {sys.argv[1]}")
                FileSearchCLI.print_help()
                exit()
            case _:
                return sys.argv[1]
            
    @staticmethod
    def read_base_path() -> Path:
        return Path(sys.argv[2]).expanduser()


if __name__ == "__main__":
    task = FileSearchCLI.get_inital_task()
            
    dispatcher = threadPoolLib.Dispatcher([task])
    dispatcher.start_workers()
    
