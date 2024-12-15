import threading

class Terminal:
	mutex = threading.Lock()

	@staticmethod
	def print(*args, **kargs) -> None:
		Terminal.mutex.acquire()
		print(*args,**kargs)
		Terminal.mutex.release()