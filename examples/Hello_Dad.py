from Person import Person

class Dad(Person):
    def __init__(self):
        super().__init__()
        self.name = "Dad"

def hello_dad():
    dad = Dad()
    print(f"Hello, {dad.get_name()}!")