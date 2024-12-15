from dataclasses import dataclass
from pathlib import Path
import inspect
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



if __name__ == "__main__":
    dispatcher = threadPoolLib.Dispatcher([FileSearchTask(r".py",Path("."))])
    dispatcher.start_workers()
    
