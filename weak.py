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
        print ' Loaded {} entries from "{}"...'.format(len(doc), cat)

# Process input
file_total = 0
all_total = 0
bad_total = 0
for root, dirs, files in walk(work):
    for f in files:
        if not f.endswith('.' + ext):
            continue
        f_path = join(root, f)
        s_path = f_path.replace(work + sep, '')
        all_count = 0
        bad_count = 0
        file_total += 1
        for number, line in enumerate(open(f_path, mode='rU')):
            words = line.split()
            all_count += len(words)
            all_total += len(words)
            for index, word in enumerate(words):
                is_bad = False
                for category, bad_words in categories.iteritems():
                    for bad_word in bad_words:
                        if word.lower() == bad_word.lower():
                            cat_name = category.upper()
                            start = index - env
                            short_line = ' '.join(words[start if start >= 0 else 0:index + env + 1])
                            w_index = index + 1
                            l_nr = number + 1
                            is_bad = True
                            print '{} [{}:{}] {} ({}) => {}'.format(s_path, l_nr, w_index, cat_name,
                                                                    bad_word, short_line)
                if is_bad:
                    bad_count += 1
        bad_total += bad_count
        bad_perf = int((bad_count * 1.0 / all_count * 1.0) * 100 * 100) / 100.0
        print ' Found {} from {} words harmful ({} %) in "{}"!'.format(bad_count, all_count,
                                                                       bad_perf, s_path)
total_perf = int((bad_total * 1.0 / all_total * 1.0) * 100 * 100) / 100.0
print ' Found {} from {} words in {} files harmful ({} %)'.format(bad_total, all_total,
                                                                  file_total, total_perf)

# Go out
exit(0)
