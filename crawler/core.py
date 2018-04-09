from queue import Queue
from datetime import datetime
import os
import threading


class WebCrawler:
    def __init__(self, csvoutput, maxthread):
        assert(maxthread > 1)
        self._queue = Queue()
        self._maxthread = maxthread
        self._running = set()
        self._lock = threading.Lock()
        self._errors = []
        self._csv_handle = None
        self._urlpattern = None
        self._current_ids = 1
        self._statusLogPath = './log/WebCrawler.log'
        self._runtimeLogPath = "./log/WebCrawler_{}.log"
        self._csv_path = csvoutput

    def gettask(self):
        task = TaskNode(self._urlpattern.format(self._current_ids), self)
        with self._lock:
            self._current_ids += 1
        return task

    def crawl(self, mode='overwrite', output=None, runtimeLogPath=None):
        if output is None:
            output = self._csv_path
        if runtimeLogPath is None:
            runtimeLogPath = self._runtimeLogPath.format(
                datetime.now().strftime('%Y%m%d_%H%M'))
        self._createDir(output)
        # set file handle
        if mode == 'append':
            # try to get current position
            self._readlog()
            self._csv_handle = open(output, 'a', newline='')
        elif mode == 'overwrite':
            self._csv_handle = open(output, 'w', newline='')
        # make the processing pool full
        for _ in range(self._maxthread << 1):
            task = self.gettask()
            self._enqueue(task)

    def _createDir(self, path):
        path = path.rsplit('/', 1)[0]
        if not os.path.isdir(path):
            os.makedirs(path)

    def _enqueue(self, task):
        if len(self._running) < self._maxthread:
            self._running.add(task)
            task.run()
        else:
            self._queue.put(task)

    def _addthread(self):
        if len(self._running) < self._maxthread and len(self._queue) > 0:
            task = self._queue.get()
            self._running.add(task)
            task.run()

    def _readlog(self, logfile=None):
        if logfile is None:
            logfile = self._statusLogPath
        if os.path.isfile(logfile):
            print("[@_readlog]unfinished method")

    def _writelog(self, logfile=None):
        if logfile is None:
            logfile = self._statusLogPath
        self._createDir(logfile)
        print("[@_writelog]unfinished method")


class AnimeInfoCrawler(WebCrawler):
    def __init__(self, csvoutput='./data/anime.csv', maxthread=5):
        super().__init__(csvoutput, maxthread)
        self._urlpattern = "http://bangumi.tv/subject/{}"
        self._statusLogPath = './log/AnimeInfoCrawler.log'
        self._runtimeLogPath = "./log/AnimeInfoCrawler_{}.log"


if __name__ == "__main__":
    AnimeInfoCrawler().crawl()
