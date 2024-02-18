import names
import random

for i in range(40):
    print("('"+names.get_full_name()+"', "+str(random.randint(1, 100000))+"),")
