from datetime import datetime
import json
import os
import re
import sys
import subprocess
from Naked.toolshed.shell import execute_js, muterun_js

def callFunc(name):
    result = execute_js('drone.js')
    if result:
        print(result)
    else:
        print("err")

def caller():
    import center

def callFunc2():
    result = execute_js('emer.js')
    if result:
        print(result)
    else:
        print("err")

def callFunc3(nm):
    result = execute_js('png.js')
    if result:
        print(result)
    else:
        print("err")
