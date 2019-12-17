import os
import subprocess

def get_book(book):
    text_list = []
    chapter = 1
    while True:
        passage = "%s %s.txt" % (book, chapter)
        try:
            with open("data/%s" % passage) as f:
                text = f.read()
                text = replace_verse_numbers(text)
                text_list.append(text)
            chapter += 1
        except:
            break

    # Single chapter books
    if len(text_list) == 0:
        passage = "%s.txt" % book
        with open("data/%s" % passage) as f:
            text = f.read()
            text = replace_verse_numbers(text)
            text_list.append(text)
    return text_list


def replace_verse_numbers(text):
    # Mark has [[ ]] for the last part
    text = text.replace("[[", "")
    text = text.replace("]]", "")
    translated = str.maketrans('[]', '{}')
    text = text.translate(translated).replace('{', r"\textcolor{lightgrey}{\scriptsize ")
    return text

def print_book(book, header, footer):
    main = ""
    chapters = get_book(book)
    for i in range(len(chapters)):
        main += r'''\newpage
        \section*{%s}
        ''' % (book + " " + str(i+1))
        main += chapters[i] + "\n"

    content = header + main + footer

    tex_file = "%s.tex" % book
    aux_file = "%s.aux" % book
    log_file = "%s.log" % book
    pdf_file = "%s.pdf" % book
    with open(tex_file, 'w') as f:
        f.write(content)

    commandLine = subprocess.Popen(['pdflatex', tex_file])
    commandLine.communicate()
    os.unlink(aux_file)
    os.unlink(log_file)
    os.unlink(tex_file)

    # Move into output folder
    subprocess.run(['mv', pdf_file, "output/"])


if __name__ == "__main__":

    header = r'''\documentclass[12pt]{extarticle}
     \usepackage{geometry}
     \usepackage{layout}
     \usepackage{xcolor}
     \definecolor{lightgrey}{cmyk}{0,0,0,0.40}  
     \definecolor{grey}{cmyk}{0,0,0,0.95}  
     \pagenumbering{gobble}
     \renewcommand{\familydefault}{\sfdefault}
     \linespread{1.7} 
     \paperwidth = 741pt
     \paperheight = 441pt
     \voffset = -1in
     \marginparwidth = 0pt
     \marginparpush = 0pt
     \headheight = 0pt
     \headsep = 0pt
     \topmargin = 25pt
     \oddsidemargin = 100pt
     \evensidemargin = 100pt
     \textheight = 390pt
     \textwidth = 380pt
     \footskip = 10pt
     \color{grey}
     \begin{document}
     '''

    footer = r'''\end{document}'''
    with open("books.txt") as f:
        books = f.read().strip().splitlines()
    for book in books:
        print_book(book, header, footer)


