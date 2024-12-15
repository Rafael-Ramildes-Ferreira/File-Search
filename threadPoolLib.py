from abc import ABC,abstractmethod
import threading
import inspect


# Will be over written, it's to make Dispatcher be defined in the Worker class
class Dispatcher: pass
class Task: pass

class Task(ABC):	
	@abstractmethod
	def exec(self) -> Task | list[Task]:
		pass

class Worker(threading.Thread):
	boss : Dispatcher
	id : int
	id_count : int = 0

	def __init__(self) -> None:
		self.id = Worker.id_count
		Worker.id_count += 1
		# looks the stack to find a reference to the Dispatcher
		# It's created in a list comprehention ([1]) in the method create_workers ([2])
		# which has an local variable called 'self'
		self.boss = inspect.stack()[2][0].f_locals['self']

		super().__init__(target=self.loop,name="worker_"+str(self.id))

	def loop(self) -> None:
		while True:
			task : Task = self.boss.dispatch_task()
			new_tasks: Task = task.exec()
			self.boss.add_task(new_tasks)

	def debug_print(self, *values, **kargs) -> None:
		print("[" + self.name + "]", *values, **kargs)

class Dispatcher:
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
	
	def create_workers(self, n_workers : int):
		self.workers.extend([Worker() for _ in range(n_workers)])

	def add_task(self, _tasks : Task | list[Task] = []) -> None:
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