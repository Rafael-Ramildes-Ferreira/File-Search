from dataclasses import dataclass
from pathlib import Path
import os
import re

import threadPoolLib


pattern = "*"

class FileSearchDispatcher(threadPoolLib.Dispatcher): pass
class FileSearchTask(threadPoolLib.Task): pass

class FileSearchTask(threadPoolLib.Task):
    dir : Path
    pattern : str

    def __init__(self, _pattern : str, path : Path) -> None:
        self.dir = path
        self.pattern = _pattern

    def exec(self) -> FileSearchTask | list[FileSearchTask]:
        files = [item for item in Path.iterdir(self.dir) if os.path.isfile(item)]
        for file in files:
            if re.search(self.pattern,str(file)):
                print(file)

        return [FileSearchTask(self.pattern,item) for item in Path.iterdir(self.dir) if os.path.isdir(item)]



if __name__ == "__main__":
    dispatcher = threadPoolLib.Dispatcher([FileSearchTask(r".py",Path("."))])
    dispatcher.start_workers()
    
