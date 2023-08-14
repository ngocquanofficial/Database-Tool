# From NgocQuan, a sophomore at HUST
# ngocquan.com
# github.com/ngocquanofficial
class Dependency:
    def __init__(self, input):
        if type(input) == str:
            input = input.split("-")
            string_A = input[0]
            string_B = input[-1]
            string_A = string_A.replace(" ", "")
            string_B = string_B.replace(" ", "")

            self.A = set(list(string_A))
            self.B = set(list(string_B))
        else:
            self.A = input[0]
            self.B = input[1]

    def __eq__(self, other):
        if not isinstance(other, Dependency):
            return False
        # The case other is also a DependencySet object
        return self.A == other.A and self.B == other.B

    def __str__(self):
        return self.string_form()

    def copy(self):
        setA = {i for i in self.A}
        setB = {i for i in self.B}
        return Dependency(input=[setA, setB])

    def string_form(self):
        deter = sorted(list(self.A))
        depend = sorted(list(self.B))
        stringA = "".join(deter)
        stringB = "".join(depend)
        string_repre = f"FD: {stringA} --> {stringB}"
        return string_repre

    def split(self):
        return self.A, self.B


class DependencySet:
    def __init__(self, dependencies=[]):
        self.dependencies = dependencies

    def __str__(self):
        string_represent = [i.string_form() for i in self.dependencies]
        return str(string_represent)

    def copy(self):
        copy_dependencies = [i for i in self.dependencies]
        copy_version = DependencySet(dependencies=copy_dependencies)
        return copy_version

    def add(self, dependency):
        self.dependencies.append(dependency)

    def remove(self, dependency):
        self.dependencies.remove(dependency)

    def merge(self, other):
        new_dependencies = list(set(self.dependencies + other.dependencies))
        return DependencySet(dependencies=new_dependencies)

    def contain(self, other):
        if not isinstance(other, DependencySet):
            return False
        # The case other is also a DependencySet object
        for dependency in other.dependencies:
            ans = self.infer(dependency)
            if ans == False:
                return False
        # When every dependency in other can be infered from self
        return True

    def __eq__(self, other):
        if not isinstance(other, DependencySet):
            return False
        # The case other is also a DependencySet object
        return self.contain(other) and other.contain(self)

    def equivalent(self, other):
        if not isinstance(other, DependencySet):
            return False
        return all(i in other.dependencies for i in self.dependencies) and all(
            a in self.dependencies for a in other.dependencies
        )

    def get_relation(self):
        relation = set()
        for dependency in self.dependencies:
            determinant = dependency.A
            dependent = dependency.B
            for i in determinant:
                relation.add(i)
            for i in dependent:
                relation.add(i)
        return relation

    def split(self):
        # dependencies contain list of Dependency() object
        determinants = []
        dependents = []
        for dependency in self.dependencies:
            determinant = dependency.A
            dependent = dependency.B
            determinants.extend(determinant)
            dependents.extend(dependent)

        # remove redundent
        determinants = set(determinants)
        dependents = set(dependents)

        return determinants, dependents

    def find_closure(self, attributes):
        X_prev = set(attributes)
        X_new = set(attributes)
        while True:
            for dependency in self.dependencies:
                # check whether attri_set contains all element in dependency.A
                # condition = True if ...
                condition = all(item in X_new for item in dependency.A)
                if not condition:
                    continue
                # Here is the case condition = True
                # Add element in dependency.B to attri_set
                for i in dependency.B:
                    X_new.add(i)

            if X_new == X_prev:
                return X_new
            X_prev = X_new.copy()

    def infer(self, dependency):
        determinant, dependent = dependency.split()
        X_closure = self.find_closure(determinant)
        return all(item in X_closure for item in dependent)

    def minimal_key(self, relation=set()):
        relation = self.get_relation()
        determinants, dependents = self.split()
        determinants = set(determinants)
        dependents = set(dependents)

        # Note: relation \ dependents is the set of attributes that must be in minimal key
        must_in = relation - dependents

        # dependents \ determinants is the set of attributes that must NOT be in minimal key
        not_in = dependents - determinants

        # determinants ^ dependents is the set of attributes that MAY be in minimal key
        maybe_in = determinants.intersection(dependents)

        key = must_in.union(maybe_in)
        # So, we only check the existance in minimal key only for element in maybe_in
        for element in maybe_in:
            new_key = key.copy()
            new_key.discard(element)
            closure_set = self.find_closure(new_key)
            if closure_set == relation:
                key = new_key

        return key

    def extract(self):
        # Copy self to a new object to avoid changing on self
        other = self.copy()
        for dependency in other.dependencies:
            if len(dependency.B) == 1:
                continue
            # When dependent contains more than 1 element
            for element in dependency.B:
                new_dependency = Dependency(input=[dependency.A, {element}])
                other.add(new_dependency)

            # Then remove the original dependency
            other.remove(dependency)
        return other

    def minimal_cover(self):
        extracted_obj = self.extract()
        for dependency in extracted_obj.dependencies:
            if len(dependency.A) == 1:
                continue

            # Remove redundant element in dependency.A
            prev_dependencies = self.copy()
            new_dependencies = self.copy()
            current_dependencies = self.copy()
            while True:
                for attribute in dependency.A:
                    new_determinant = {i for i in dependency.A}
                    new_determinant.remove(attribute)
                    adding_path = Dependency(input=[new_determinant, dependency.B])
                    current_dependencies.add(adding_path)
                    current_dependencies.remove(dependency)

                    # If current_dependencies+ = prev_dependencies+,
                    # then assign new_dependencies by current_...
                    if current_dependencies == prev_dependencies:
                        new_dependencies = current_dependencies.copy()
                        # Replace dependency by adding_path
                        dependency = adding_path
                    else:
                        # That means current_dependencies loose some information
                        # when compare to prev_dependencies, so change it to
                        # new_dependencies and continue consider next attribute in for loop
                        # For simplicity, NOTHING CHANGE, continue for loop
                        current_dependencies = new_dependencies.copy()

                if new_dependencies.equivalent(prev_dependencies):
                    # After for loop, there are not any changing, then break While loop
                    break

                # ELSE
                prev_dependencies = new_dependencies.copy()

            extracted_obj = new_dependencies.copy()

        for dependency in extracted_obj.dependencies:
            new_dependencies = extracted_obj.copy()
            new_dependencies.remove(dependency)

            if new_dependencies == extracted_obj:
                extracted_obj = new_dependencies

        return extracted_obj


#################################################################################

# Input from user
# print("Press quit to stop input process")
# while True :
#     input_str = input("Type dependency: ")
#     if input_str == 'quit' :
#         break
#     obj = Dependency(input_str)
#     print(obj.A, "A")
#     print(obj.B, "B")
#     dependencies.append(obj)

# x1 = "AB - C"
# x2 = "AC - B"
# x3 = "BC - DE"
# x4 = "AD - C"

# x1 = "AD - B"
# x2 = "A-E"
# x3 = "C-E"
# x4 = "DEF-A"
# x5 = "F-D"

# x1 = "BC-GH"
# x2 = "AD - E"
# x3 = "A-H"
# x4 = "E - BCF"
# x5 = "G -H"

# x1 = "B-D"
# x2 = "E-F"
# x3 = 'D-E'
# x4 = 'D-B'
# x5 = 'F-BD'

x1 = "B-A"
x2 = "D-A"
x3 = "AB - D"

y1 = Dependency("A- C")
y2 = Dependency("AC - D")
y3 = Dependency("E-AD")
y4 = Dependency("E-H")

z1 = Dependency("A - CD")
z2 = Dependency("E-AH")

# first_obj = DependencySet(dependencies=[])
# first_obj.add(y1)
# first_obj.add(y2)
# first_obj.add(y3)
# first_obj.add(y4)

# second_obj = DependencySet(dependencies=[])
# second_obj.add(z1)
# second_obj.add(z2)

# print(first_obj)
# print(second_obj)
# print(first_obj == second_obj)

print(1111111111)
obj = DependencySet(dependencies=[])
obj.add(Dependency(x1))
obj.add(Dependency(x2))
obj.add(Dependency(x3))

print(obj)
new_obj = obj.extract()
print(obj)
print("After extracting: ", new_obj)
print(obj.minimal_cover())

# attributes = input("Type list of attribute: ")
# attributes = list(attributes.replace(" ", ""))

# print("DONE")
# print(obj.find_closure(attributes))

# print(obj.minimal_key())


# first_obj = DependencySet(dependencies=[])
# second_obj = DependencySet(dependencies=[])
# while True:
#     line = input()
#     if line == "quit":
#         break
#     first_obj.add(Dependency(line))

# print("SECOND")
# while True:
#     line = input()
#     if line == "quit":
#         break
#     second_obj.add(Dependency(line))
# print(f"First obj: {first_obj}")
# print(f"Second obj: {second_obj}")
# print(first_obj == second_obj)
