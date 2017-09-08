# Author: Amanda House (aeh247@cornell.edu)

import csv, glob, os

os.makedirs('out')

with open('template_question.html') as infile:
    template_question = infile.read()
with open('template_base.html') as infile, open('out/temp_question.html', 'w') as outfile:
    for line in infile:
        line = line.replace('replace_main', template_question)
        outfile.write(line)

with open('template_watermark.html') as infile:
    template_watermark = infile.read()
with open('template_base.html') as infile, open('out/temp_watermark.html', 'w') as outfile:
    for line in infile:
        line = line.replace('replace_main', template_watermark)
        outfile.write(line)

print 'Folder:'
os.chdir(raw_input())

for file in glob.glob('*.csv'):

    with open(file, 'rb') as infile:
        form = list(csv.reader(infile))

    question_text = form[0][1]
    example_text = form[1][1]
    short_name = form[2][1]
    left_text = form[3][1]
    left_link = form[4][1]
    right_text = form[5][1]
    right_link = form[6][1]
    back_link = form[7][1]
    branch_name = form[8][1]
    restart_link = form[9][1]

    replacements = {
        'replace_branch_name': branch_name,
        'replace_back_link': back_link,
        'replace_restart_link': restart_link,
        'replace_question_text': question_text,
        'replace_left_link': left_link,
        'replace_left_text': left_text,
        'replace_right_link': right_link,
        'replace_right_text': right_text,
        'replace_example_text': example_text,
        'replace_image': short_name
    }

    with open('../out/temp_question.html') as infile, open('../out/' + short_name + '.html', 'w') as outfile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)

for file in glob.glob('*.txt'):

    with open(file) as infile:
        lines = infile.read().splitlines()
    watermark = lines[0]
    description = lines[1]

    replacements = {
        'replace_watermark': watermark,
        'replace_text': description,
        'replace_image': watermark
    }

    with open('../out/temp_watermark.html') as infile, open('../out/' + watermark + '.html', 'w') as outfile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)

os.remove('../out/temp_question.html')
os.remove('../out/temp_watermark.html')
