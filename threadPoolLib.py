from abc import ABC,abstractmethod
import threading


# Will be over written, it's to make Dispatcher be defined in the Worker class
class Dispatcher: pass

class Task(ABC):
    pass

class Worker(ABC):
    boss : Dispatcher

    def __init__(self, _boss : Dispatcher) -> None:
        self.boss = _boss

    @abstractmethod
    def run(self, *args, **kwargs) -> any:
        pass

class Dispatcher(ABC):
	tasks : list[Task]
	workers : list[Worker]
	semaphore : threading.Semaphore
	mutex : threading.Lock

	def __init__(self, _tasks : list[Task] = [], n_workers : int = 5) -> None:
		self.semaphore = threading.Semaphore(0)
		self.mutex = threading.Lock()
		self.tasks = _tasks
		self.semaphore.release(len(self.tasks))
		self.workers = []
		self.create_workers(n_workers)
		
	@abstractmethod
	def create_workers(self, n_workers : int):
		self.workers.extend([Worker(self) for _ in range(n_workers)])

	def add_task(self, _tasks : list[Task] = []) -> None:
		if(len(_tasks) == 0):
			return
		
		self.mutex.acquire()
		
		self.tasks.extend(_tasks)
		self.semaphore.release(len(_tasks))
		
		self.mutex.release()
		
	def start_workers(self) -> None:
		for worker in self.workers:
			worker.run()

	def dispatch_task(self) -> Task:
		self.mutex.acquire()
		
		self.semaphore.acquire()
		task : Task = self.tasks.pop(0)
		
		self.mutex.release()

		return task