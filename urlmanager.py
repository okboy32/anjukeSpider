class UrlManager(object):

    def __init__(self):
        self.url = set()
        self.old_url = set()

    def add_new_url(self, urls):
        if urls is None:
            return
        if not isinstance(urls,list):
            self.url.add(urls)
            self.old_url.add(urls)
            return
        for url in urls:
            if url in self.old_url:
                continue
            self.url.add(url)
            self.old_url.add(url)

    def get_url(self):
        if not self.size:
            return
        return self.url.pop()

    @property
    def size(self):
        return len(self.url)

    def has_url(self):
        return self.size