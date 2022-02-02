from src.parsers import AC_Import

a = AC_Import()
b = "test" + a.__str__()
print(b)