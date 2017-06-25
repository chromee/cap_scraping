import csv
import pandas
import re
import os
import requests
import struct
import urllib.request
import sys
import difflib
from scripts.html_manager import HtmlManager
from mdfmonitor import FileModificationMonitor

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


files = os.listdir(".") # >>> ['sample.txt', 'sample.py']

# create Watcher instnce
monitor = FileModificationMonitor()

# append file to mdfmonitor instance
monitor.add_file("sample.txt")

# or
# append files to mdfmonitor instance
monitor.add_files(os.listdir("."))

for mdf in monitor.monitor():
    print(mdf.file.center(30, "="))
    print(  "Catch the Modification!!")
    print("Old timestamp: %s" % mdf.old_mtime)
    print("New timestamp: %s" % mdf.new_mtime)
    print("manager: %s" % str(mdf.manager.o_repository))
    print("Diff".center(30,"="))
    print(mdf.diff)
