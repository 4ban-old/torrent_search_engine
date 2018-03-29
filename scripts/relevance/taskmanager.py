# coding: utf-8

# No threads and no processes multitasks
# Written using coroutines.
# Original idea:"Python Essential
# Reference (4th Edition)" (D.Beazley)

import select
import types
import collections
import time


class Task(object):
    """ Task Wrapper. """

    def __init__(self, target):
        """
            :param target: Coroutine
            :return: None

            :sendval: Value sending on continuation
            :stack: Stack of calls
        """
        self.target = target
        self.sendval = None
        self.stack = []

    def run(self):
        try:
            result = self.target.send(self.sendval)
            if isinstance(result, SystemCall):
                return result
            if isinstance(result, types.GeneratorType):
                self.stack.append(self.target)
                self.sendval = None
                self.target = result
            else:
                if not self.stack:
                    return
                self.sendval = result
                self.target = self.stack.pop()
        except StopIteration:
            if not self.stack:
                raise
            self.sendval = None
            self.target = self.stack.pop()


class Scheduler(object):
    """ Task Manager object """
    def __init__(self):
        self.task_queue = collections.deque()
        self.read_waiting = {}
        self.write_waiting = {}
        self.time_waiting = {}
        self.numtasks = 0

    def new(self, target):
        """ Create new target from program """
        newtask = Task(target)
        self.schedule(newtask)
        self.numtasks += 1

    def schedule(self, task):
        """ Add new task to queue """
        self.task_queue.append(task)

    def readwait(self, task, fd):
        """ Stop task while file descriptor
            unable to read
        """
        self.read_waiting[fd] = task

    def writewait(self, task, fd):
        """ Stop task until file descriptor
            unable to write
        """
        self.write_waiting[fd] = task

    def timewait(self, task, times):
        """ Stop task for some time
            :param time: Tuple (time1, time2)
                time1 - time, when TimeWait was called
                time2 - time, when we must run task again
        """
        now = time.time()
        self.time_waiting[times] = task

    def mainloop(self, count=-1, timeout=None):

        while self.numtasks:
            # Check input/output event
            if self.read_waiting or self.write_waiting:
                wait = 0 if self.task_queue else timeout
                r, w, e = select.select(self.read_waiting, self.write_waiting,
                                            [], wait)
                for fileno in r:
                    self.schedule(self.read_waiting.pop(fileno))
                for fileno in w:
                    self.schedule(self.write_waiting.pop(fileno))
            if self.time_waiting:
                t = filter(lambda x: x[1]>time.time(), self.time_waiting)
                for item in t:
                    self.schedule(self.time_waiting.pop(item))

            # Run all tasks in queue, which is ready
            while self.task_queue:
                task = self.task_queue.popleft()
                try:
                    result = task.run()
                    if isinstance(result, SystemCall):
                        result.handle(self, task)
                    else:
                        self.schedule(task)
                except StopIteration:
                    self.numtasks -= 1

            # If no tasks ready to run,
            # must decide to continue or exit
            else:
                if count > 0: count -= 1
                if count == 0: return


# System Calls

class SystemCall(object):
    def handle(self, sched, task):
        pass


class ReadWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self, sched, task):
        fileno = self.f.fileno()
        sched.readwait(task, fileno)


class WriteWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self, sched, task):
        fileno = self.f.fileno()
        sched.readwait(task, fileno)


class TimeWait(SystemCall):
    def __init__(self, period):
        now = time.time()
        self.times = (now, now + period/1000.0)


class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handle(self, sched, task):
        sched.new(self.target)
        sched.schedule(task)


if __name__ == '__main__':
    from socket import socket, AF_INET, SOCK_STREAM

    def time_server(address):
        import time
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(address)
        s.listen(5)
        while True:
            yield ReadWait(s)
            conn, addr = s.accept()
            print ("Connection from %s:%s" % addr)
            yield WriteWait(conn)
            resp = time.ctime() + "\r\n"
            conn.send(resp.encode('latin-1'))
            conn.close()

    sched = Scheduler()
    sched.new(time_server(('', 15002)))
    sched.new(time_server(('', 15003)))
    sched.mainloop()
