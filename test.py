import os

root = os.getcwd()

os.system(f"git add {root}/README.md")
os.system('git commit -am "tesReadMe"')

os.system(f"git add {root}/test.py")
os.system('git commit -am "tesTest"')

os.system("git push")
