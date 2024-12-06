from dataclasses import dataclass
from pathlib import Path
import os
import re

import threadPoolLib


pattern = "*"

class FileSearchDispatcher(threadPoolLib.Dispatcher): pass

@dataclass
class FileSearchTask(threadPoolLib.Task):
    dir : Path


class FileSearchWorker(threadPoolLib.Worker):
    boss : FileSearchDispatcher

    def run(self) -> None:
        while True:
            task : FileSearchTask = self.boss.dispatch_task()
            self.boss.add_task([item for item in Path.iterdir(task.dir) if os.path.isdir(item)])
            files = [item for item in Path.iterdir(task.dir) if os.path.isfile(item)]
            for file in files:
                if re.search(pattern,str(file)):
                    print(file)


class FileSearchDispatcher(threadPoolLib.Dispatcher):
    def create_workers(self, n_workers : int):
        self.workers.extend([FileSearchWorker(self) for _ in range(n_workers)])


if __name__ == "__main__":
    dispatcher = FileSearchDispatcher([FileSearchTask(Path("."))])
    dispatcher.start_workers()
    
