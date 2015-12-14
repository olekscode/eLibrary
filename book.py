class Book:
    def __init__(self, author, title, year, publ):
        self.author = author
        self.title = title
        self.year = year
        self.publ = publ

    def __getitem__(self, item):
        return {
            'author': self.author,
            'title' : self.title,
            'year': self.year,
            'publ': self.publ
        }[item]
        
    def __str__(self):
        string = ("Author:    {0}\n"
                  "Title:     {1}\n"
                  "Year:      {2}\n"
                  "Publisher: {3}\n")
        return string.format(self.author,
                             self.title,
                             self.year,
                             self.publ)

