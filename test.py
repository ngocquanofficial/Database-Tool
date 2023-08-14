class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        print(self.name)
        print(other.name)
        print("!!!")
        if isinstance(other, Person):
            return self.name == other.name and self.age == other.age
        return False


# Testing the custom __eq__ method
person1 = Person("Alice", 30)
person2 = Person("Alice", 30)
person3 = Person("Bob", 25)

print(person1 == person2)  # Output: True
print(person1 == person3)  # Output: False
print(12)
