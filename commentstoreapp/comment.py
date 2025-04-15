class Comment:
    name = ''
    visitdate = ''
    commentstr = ''

    def __init__(self, name, visitdate, commentstr):
        self.name = name
        self.visitdate = visitdate
        self.commentstr = commentstr

    def __str__(self):
        details = ''
        details += f'Name        : {self.name}\n'
        details += f'VisitDate   : {self.visitdate}\n'
        details += f'Comment     : {self.commentstr}\n'
        return details
