from queue import Queue
from datetime import datetime
import os
import threading
from task import AnimeTaskNode
import time


class WebCrawler:
    def __init__(self, csvoutput, maxthread):
        assert(maxthread > 1)
        self._queue = Queue()
        self._maxthread = maxthread
        self._running = set()
        self._lock = threading.Lock()
        self._errors = []
        self._urlpattern = None
        self._current_ids = 1
        self._statusLogPath = './log/WebCrawler.log'
        self._runtimeLogPath = "./log/WebCrawler_{}.log"
        self._csv_path = csvoutput
        self._csv_handle = None

    def gettask(self):
        pass

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

        while self._queue.qsize() > 0 or len(self._running) > 0:
            try:
                time.sleep(1)
                print("Working on {} threads with id = {}, qsize = {}, errors = {}".format(
                    len(self._running), self._current_ids, self._queue.qsize(), len(self._errors)))
            except KeyboardInterrupt:
                with self._lock:
                    self._errors.append(KeyboardInterrupt(
                        "@id = {}".format(self._current_ids)))
                break

        self._csv_handle.close()
        print("\n\ndone!")

        if len(self._errors) == 0:
            print("No errors found!")
        else:
            print("Here are all the complaints found:")
            for error in self._errors[:5]:
                print(error.__repr__())
            if len(self._errors) > 5:
                print("Other errors could be found in {}".format(runtimeLogPath))

        # dump log file

    def _createDir(self, path):
        path = path.rsplit('/', 1)[0]
        if not os.path.isdir(path):
            os.makedirs(path)

    def _enqueue(self, task):
        if len(self._running) < self._maxthread:
            with self._lock:
                self._running.add(task)
            threading.Thread(target=task.run).start()
        else:
            self._queue.put(task)

    def _addthread(self):
        if len(self._running) < self._maxthread and self._queue.qsize() > 0:
            task = self._queue.get()
            with self._lock:
                self._running.add(task)
            threading.Thread(target=task.run).start()

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

    def gettask(self):
        with self._lock:
            task = AnimeTaskNode(
                self._urlpattern.format(self._current_ids), self)
            self._current_ids += 1
        return task


if __name__ == "__main__":
    AnimeInfoCrawler().crawl()
