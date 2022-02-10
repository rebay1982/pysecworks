from threading import Thread
import Queue

class LookupQueue(Queue.Queue):
    def __init__(self, nb_workers = 1):
        Queue.Queue.__init__(self)
        self.nb_workers = nb_workers
        self.start_workers()

    def add_lookup(self, ips)
        self.put(ips)

    def start_workers(self):
        for i in range(self.nb_workers):
            t = Thread(target = self.worker)
            t.daemon = True
            t.start()

    def worker(self):
        while True:
            ips = self.get()
            lookup_worker(ips)
            self.task_done()

