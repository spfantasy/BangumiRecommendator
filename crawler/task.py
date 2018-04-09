from errors import IndexExceedError, SubjectBlockedError
import requests
import re


class TaskNode:
    def __init__(self, url, crawler):
        self.url = url
        self.status = "Q"
        self.crawler = crawler
        '''
        Status in (
            Queueing,
            Running,
            Finished,
        )
        '''

    def run(self):
        self.status = "R"
        try:
            res = requests.get(self.url, timeout=10)
            res.encoding = 'utf-8'
        except Exception as e:
            self.fail(e)
        else:
            self._recorder(res.text)
        return self

    def done(self):
        self.status = "D"
        return self

    def fail(self, e):
        self.status = "F"
        self.crawler._errors.append(e)
        return self

    def _recorder(self, text):
        print("This is a method that need to be overwrite")

    def _saver(self, page):
        print("This is a method that need to be overwrite")

    def __repr__(self):
        return "[{}]{}".format(self.status, self.url)


class AnimeTaskNode(TaskNode):
    def __init__(self, url, crawler):
        super().__init__(self, url, crawler)

    def _recorder(self, text):
        if self.indexExceeded(text):
            self.crawler._errors.append(IndexExceededError(self.url))
        elif self.subjectBlocked(text):
            self.crawler._errors.append(SubjectBlockedError(self.url))
            self.crawler._enqueue(self.crawler.gettask())
        else:
            page = self.getcontent(text)
            self._saver(page)
            self.crawler._enqueue(self.crawler.gettask())

    def getcontent(text):
        page = {}
        soup = BeautifulSoup(text, "html5lib")
        infobox = soup.find('div', {"id": "bangumiInfo"}).find(
            'div', {"class": "infobox"}).find_all('li')

        def remove_tag_a(lst):
            ret_val = []
            for itm in lst:
                try:
                    itm = itm.contents[0].strip(" :：、")
                except:
                    pass
                if len(itm) > 0:
                    ret_val.append(itm)

            return ret_val if len(ret_val) > 1 else ret_val[0]

        page = {}
        for row in infobox:
            key = row.find("span").contents[0].strip(" :：、")
            val = row.contents[1:]
            val = remove_tag_a(val)
            page[key] = val

        page["id"] = self.url
        page["nameJP"] = soup.find('title').contents[0].split('|')[
            0].strip(" :：、")
        page["averageRating"] = soup.find(
            'span', {"property": "v:average"}).contents[0].strip(" :：、")
        page["imageURL"] = soup.find(
            'a', {"class": "thickbox cover"}).contents[0]['src'].strip(' /')
        return page

    def indexExceeded(self, text):
        if re.search('<h2>呜咕，出错了</h2>', text):
            return True
        else:
            return False

    def subjectBlocked(self, text):
        if re.search('<h3>条目已锁定</h3>', text):
            return True
        else:
            return False

    def _saver(self, page):
        print("This is a method that need to be overwrite")
