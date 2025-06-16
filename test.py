import os

root = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
print(root)