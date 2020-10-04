from bs4 import BeautifulSoup as soup
import requests
import sys
import re

# get CLI args
args = sys.argv

if args is None:
    sys.exit("Please provide a url as an argument when running this script")


def build_url(current_url, chapter_num):
    new_url = re.sub(r'(\d+/)(\d+)(/.+$)', r'\g<1>' + str(chapter_num) + '\g<3>', current_url)
    print(new_url)
    return new_url


# -- Scrapping webpage --
# Specify URL
first_page = args[0]
current_page = first_page
current_chapter_number = 1
# default start
num_chapters = 0

while current_page is not None:
    # query the website and return the html response
    response = requests.get(current_page)
    # parse the html using beautiful soup and store as page
    page = soup(response.content, "html.parser")

    main_text = page.find('div', attrs={'class': 'storytextp'})
    paragraphs = main_text.find('p')

    # Extract Number of Chapters
    # Only run the first time
    if num_chapters == 0:
        chapter_select = page.find('select', attrs={'id': 'chap_select'})
        num_chapters = len(chapter_select.find_all('option'))
        print("Chapters found: " + str(num_chapters))

    # Get Title and Chapter number
    temp = main_text.find('p', attrs={'style': 'text-align:center;'})
    chapter_num = temp[0].get_text()
    chapter_title = temp[1].get_text()

    file_name = chapter_title
    file_name.replace(" ", "_")

    file = open(file_name + ".tex", 'a', encoding="utf-8")
    file.write('\\documentclass[../main.tex]{subfiles}\n\n\\begin{document}\n')

    # -- Extract each paragraph --
    for par in paragraphs:
        for par_em in par.find_all('em'):
            if par_em is not None:
                new_text = page.new_string('\\textit{' + par_em.text + '}')
                par_em.replace_with(new_text)
        for par_br in par.find_all('br'):
            if par_br is not None:
                new_text = page.new_string(par_br.text + '\n')
                par_br.replace_with(new_text)
        # Add support for Strong/Bold support
        for par_bold in par.find_all('strong'):
            if par_bold is not None:
                new_text = page.new_string('\\textbf{' + par_bold.text + '}')
                par_bold.replace_with(new_text)

        par_text = par.text.strip()

        # Replace incorrect whitespacing
        # TODO Add more whitespacing detection
        par_text = par_text.replace("  ", " ")
        par_text = par_text.replace("  ", " ")

        # Extract incorrect characters here:
        # Replace ■ with:
        # \begin{center}
        # ---
        # \end{center}
        par_text = par_text.replace("■", "\\begin{center}\n---\n\\end{center}")

        file.write(par_text + '\n\\par\n')

        print(par_text)

    file.write('\\end{document}')
    file.close()

    if current_chapter_number < num_chapters:
        current_chapter_number = current_chapter_number + 1
        current_page = build_url(current_page, current_chapter_number)
    else:
        current_page = None
