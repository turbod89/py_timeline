class Card():

    name = None
    year = None
    description = None
    
    def __init__(self, *args, **kwargs):
        for key in kwargs:
            if key == 'name':
                self.name = kwargs[key]
            elif key == 'year':
                self.year = kwargs[key]
            elif key == 'description':
                self.description = kwargs[key]

    def __str__(self):
        return '%i - \'%s\'' % (self.year, self.name)

    def __lt__(self, other):
        if isinstance(other,Card):
            return self.year < other.year
        elif type(other) == int:
            return self.year < other
        else:
            return True

    def __le__(self, other):
        if isinstance(other, Card):
            return self.year <= other.year
        elif type(other) == int:
            return self.year <= other
        else:
            return True
