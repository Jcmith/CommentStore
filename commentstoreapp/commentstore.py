from queue import Queue
from .comment import Comment


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class CommentStore:
    commentlist = Queue()

    def insertcomment(self, name, visitdate, commentstr):
        cmt = Comment(name, visitdate, commentstr)
        self.commentlist.put(cmt)
