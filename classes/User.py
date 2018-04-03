class User:
    name = "guest"
    firstName = "Guest"
    lastName = None

    def __str__(self):
        return '@%s' % self.name

    def __init__(self, *args, **kwargs):
        for key in kwargs:
            if key == 'name':
                self.name = kwargs[key]
            elif key == 'firstName':
                self.firstName = kwargs[key]
            elif key == 'lastName':
                self.lastName = kwargs[key]
