# -*- coding: utf-8 -*-

# Imports
from sys import argv, exit
from os.path import abspath, join
from json import load

# Hit exit if not parametrized
if not len(argv) == 4:
    print 'Usage:', '[folder] [extension] [language]'
    exit(-1)

# Parse options
lang = argv[-1]
ext = argv[-2]
root = argv[-3]

# Settings
baseDir = abspath('.')
langDir = join(baseDir, lang)

# Read JSON files
with open('de-de/nichtPassiv.json', mode='r') as f:
    doc = load(f)
    print doc

print ext, root, langDir

# Go out
exit(0)
