# -*- coding: utf-8 -*-

# Imports
from sys import argv, exit
from os import listdir, walk, sep
from os.path import abspath, join, splitext, basename
from codecs import open
from json import load

# Hit exit if not parametrized
if not len(argv) == 4:
    print 'Usage:', '[folder] [extension] [language]'
    exit(-1)

# Parse options
lang = argv[-1]
ext = argv[-2]
work = argv[-3]

# Settings
baseDir = abspath('.')
langDir = join(baseDir, lang)
code = 'utf-8'
env = 4

# Read JSON files
categories = dict()
for jsonFile in [join(langDir, name) for name in listdir(langDir)]:
    if not jsonFile.endswith('.json'):
        continue
    with open(jsonFile, mode='rU', encoding=code) as f:
        doc = load(f)
        cat, j_ext = splitext(basename(jsonFile))
        categories[cat] = doc

# Process input
for root, dirs, files in walk(work):
    for f in files:
        if not f.endswith('.' + ext):
            continue
        f_path = join(root, f)
        s_path = f_path.replace(work + sep, '')
        for number, line in enumerate(open(f_path, mode='rU')):
            words = line.split()
            for index, word in enumerate(words):
                for category, bad_words in categories.iteritems():
                    for bad_word in bad_words:
                        if word.lower() == bad_word.lower():
                            cat_name = category.upper()
                            start = index - env
                            short_line = ' '.join(words[start if start >= 0 else 0:index + env])
                            print '{} [{}:{}] {} ({}) => {}'.format(s_path, number, index, cat_name,
                                                                    bad_word, short_line)

# Go out
exit(0)
