# Author: Amanda House (aeh247@cornell.edu)

import os, sys, csv, graphviz as gv, textwrap

OUT = "out/"
HTML = ".html"
INDEX = "index"
INDEXH = INDEX + HTML

def try_makedir(name):
    try:
        os.makedirs(name)
    except OSError:
        pass

def wrap_readlines(filepath):
    lines = []
    with open(filepath, "rb") as file:
        lines = file.readlines()
    return lines

def get_idx_indent(string, lst):
    idx = 0
    indent = "  "
    counter = 0
    for line in lst:
        counter += 1
        if string in line:
            indent += line.split(string)[0]
            idx = counter
            break
    return idx, indent

def wrap_listdir(path, html=False):
    if html:
        return [f for f in os.listdir(path) if f != ".DS_Store" and f.endswith(HTML)]
    else:
        return [f for f in os.listdir(path) if f != ".DS_Store"]

def interweave_files(file1, file2, idx, indent):
    newfile = []
    for line in file1[:idx]:
        newfile.append(line)
    for line in file2:
        newfile.append(indent + line)
    for line in file1[idx:]:
        newfile.append(line)
    return newfile

def interweave_files2(file1, idx1a, idx1b, file2, idx2, indent2a, indent2b):
    newfile = []
    for line in file1[:idx1a]:
        newfile.append(line)
    for line in file2[:idx2]:
        newfile.append(indent2a + line)
    for line in file1[idx1a:idx1b]:
        newfile.append(line)
    for line in file2[idx2:]:
        newfile.append(indent2b + line)
    for line in file1[idx1b:]:
        newfile.append(line)
    return newfile

def wrap_writefile(filepath, lst):
    with open(filepath, "w") as file:
        for line in lst:
            file.write(line)

def wrap_csvreader(filepath):
    lst = []
    with open(filepath, "rb") as file:
        lst = list(csv.reader(file))
    return lst

def wrap_replace(replacements, template):
    newfile = []
    for line in template:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
        newfile.append(line)
    return newfile

# 1  Setup.

try_makedir(OUT)

base_template = wrap_readlines("components/base_template.html")
main_idx, main_indent = get_idx_indent('<div class="main">', base_template)
script_idx, script_indent = get_idx_indent("</body>", base_template)
script_idx -= 1

folder = sys.argv[1]

if folder == "pages":
    # 2  Handle site/text pages in the model.

    pages = {}
    pages_dir = "model/pages/"
    for filename in wrap_listdir(pages_dir):
        pages[filename] = wrap_readlines(pages_dir + filename)

    for filename, contents in pages.iteritems():
        outname = ""
        if filename == INDEXH:
            outname = OUT + filename
        else:
            outdir = OUT + filename.split(".")[0] + "/"
            try_makedir(outdir)
            outname =  outdir + INDEXH

        outfile = interweave_files(base_template, contents, main_idx, main_indent)
        if filename == INDEXH:
            outfile = [s.replace("../", "") for s in outfile]
        wrap_writefile(outname, outfile)

else:
    # 3  Handle a whole branch.

    # 3.1  Handle non-question and non-watermark branch pages, i.e., index and diagram .html.

    branch = {}
    branch_dir = "model/" + folder + "/"
    for filename in wrap_listdir(branch_dir, html=True):
        branch[filename] = [wrap_readlines(branch_dir + filename)]

    for filename, lst in branch.iteritems():
        split_idx, throwaway = get_idx_indent("<script>", lst[0])
        split_idx -= 1
        branch[filename].append(split_idx)

    for filename, lst in branch.iteritems():
        outname = OUT + filename
        contents = lst[0]
        split_idx = lst[1]

        outfile = interweave_files2(base_template, main_idx, script_idx, contents, split_idx, main_indent, script_indent)
        wrap_writefile(outname, outfile)

    # 3.2  Handle question and watermark pages.

    # 3.2.1  Set up templates.

    branch_template = wrap_readlines("components/branch_template.html")
    split_idx, throwaway = get_idx_indent("<script>", branch_template)
    split_idx -= 1

    temp_template = interweave_files2(base_template, main_idx, script_idx, branch_template, split_idx, main_indent, script_indent)
    insert_idx, inner_indent = get_idx_indent("insert_here", temp_template)
    insert_idx -= 1
    inner_indent = inner_indent[2:]
    temp_template.pop(insert_idx)

    temp_question_template = wrap_readlines("components/question_template.html")
    temp_watermark_template = wrap_readlines("components/watermark_template.html")

    question_template = interweave_files(temp_template, temp_question_template, insert_idx, inner_indent)
    watermark_template = interweave_files(temp_template, temp_watermark_template, insert_idx, inner_indent)

    # 3.2.2  Make a model of the branch.

    branch_textname = ""

    tree = {}
    NAME = "name"
    TEXT = "text"
    BACK = "back"
    TYPE = "type"
    WM   = "wm"
    QU   = "qu"
    YES  = "yes"
    NO   = "no"

    tree_list = wrap_csvreader(branch_dir + "tree.csv")

    branch_textname = tree_list[1][0]
    for row in tree_list[3:]:
        tree[row[0]] = {YES: row[1], NO: row[2]}

    watermark_dir = branch_dir + "watermarks/"
    question_dir = branch_dir + "questions/"

    for filename in wrap_listdir(watermark_dir):
        lst = wrap_csvreader(watermark_dir + filename)
        tree[lst[0][1]] = {NAME: lst[1][1], TEXT: lst[2][1], TYPE: WM}

    for filename in wrap_listdir(question_dir):
        lst = wrap_csvreader(question_dir + filename)
        d = tree[lst[0][1]]
        d[TYPE] = QU
        d[NAME] = lst[1][1]
        d[TEXT] = lst[2][1]

    for node, d in tree.iteritems():
        if d[TYPE] == QU:
            tree[d[YES]][BACK] = node
            tree[d[NO]][BACK] = node

    # 3.2.3  Generate HTML for question and watermark pages.

    for node, d in tree.iteritems():

        outname = OUT + node + HTML

        replacements = {}
        replacements = {"replace_branch_textname": branch_textname,
                        "replace_this_shortname": node}
        if BACK in d:
            replacements["replace_back_shortname"] = d[BACK]
        else:
            replacements["replace_back_shortname"] = INDEX

        if d[TYPE] == QU:
            replacements["replace_question_textname"] = d[NAME]
            replacements["replace_left_shortname"] = d[YES]
            replacements["replace_right_shortname"] = d[NO]
            replacements["replace_question_additional_text"] = d[TEXT]

            outfile = wrap_replace(replacements, question_template)

            wrap_writefile(outname, outfile)

        elif d[TYPE] == WM:
            replacements["replace_watermark_textname"] = d[NAME]
            replacements["replace_watermark_additional_text"] = d[TEXT]

            outfile = wrap_replace(replacements, watermark_template)
            wrap_writefile(outname, outfile)

    # 3.2.4  Make pdf diagram.

    diagram = gv.Digraph(format="pdf")

    def clean_str(s):
        s = unicode(s, "utf-8")
        s = textwrap.wrap(s, width=20)
        s = '\n'.join(s)
        return s

    for node, d in tree.iteritems():
        if d[TYPE] == QU:
            diagram.edge(clean_str(d[NAME]), clean_str(tree[d[YES]][NAME]), YES)
            diagram.edge(clean_str(d[NAME]), clean_str(tree[d[NO]][NAME]), NO)

    diagram.render("out_gv/" + folder, cleanup=True)
