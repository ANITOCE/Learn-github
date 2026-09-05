from Person import Person

class Mom(Person):
    def __init__(self):
        super().__init__()
        self.name = "Mom"

def hello_mom():
    mom = Mom()
    print(f"Hello, {mom.get_name()}!")
