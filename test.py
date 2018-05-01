import io
import re
import os
import sys
import codecs
import roman
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import TextTiling as tt
import warun as tt2
from nltk.tokenize.texttiling import TextTilingTokenizer
import readless.Segmentation



def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def get_abstract(content):
    start = content.find('abstract')
    start = re.search(r'\babstract\b', content)
    if start == None:
        start = re.search(r'\ba b s t r a c t\b', content)
        if start:
            start = start.regs[0][1]
    else:
        start = start.regs[0][1]

    stop = re.search(r'\bintroduction\b', content)
    if stop == None:
        stop = re.search(r'\b. introduction \b', content)
    return content[start:stop.regs[0][0]]


def get_intro_conclusion(content):
    content_split = content.split('\n')

    to_process = ''
    abstract_count = 0
    intro_count = 0
    roman_numeral_headers = False
    conclusion_flag = False
    newline_count = 0

    intro_index = 0

    for idx, line in enumerate(content_split):
        if len(re.findall('\\babstract\\b', line)) > 0 or len(re.findall('\\ba b s t r a c t\\b', line)) > 0 and abstract_count == 0:
            abstract_count += 1
            continue
        # elif ((abstract_count >= 1) or (intro_count >= 1)) and len(line.strip()) == 0:
        #     to_process += '\n\n'
        #     newline_count += 1
        elif abstract_count == 1 and line.strip().find('introduction') > -1 and (intro_count == 0) and len(line) < 30:
            abstract_count += 1
            intro_count += 1
            period_separator = line.strip().find('.')

            if period_separator == -1:
                period_separator = line.strip().find(' ')

            if period_separator > -1:
                # handling roman numerals in some papers
                try:
                    intro_index = int(line[:period_separator])
                except ValueError:
                    roman_numeral_headers = not roman_numeral_headers
                    intro_index = roman.fromRoman(line[:period_separator].upper())
            else:
                # some papers' indexes were coming on separate lines
                index = content_split[idx-2].strip().replace('.', '')
                try:
                    intro_index = int(index)
                except ValueError:
                    roman_numeral_headers = not roman_numeral_headers
                    intro_index = roman.fromRoman(index.upper())
            intro_index += 1
        elif (not roman_numeral_headers and line.startswith(str(intro_index)+'.') and len(line) < 30 and len(line) > 5) or \
                (not roman_numeral_headers and line.startswith(str(intro_index)) and len(line) < 30 and len(line) > 5) and intro_count == 1 or \
                (roman_numeral_headers and line.startswith((roman.toRoman(intro_index)).lower()+'.')) or \
                (roman_numeral_headers and line.startswith((roman.toRoman(intro_index)).upper() + '.')):
            intro_count += 1
            # break
        elif (line.strip().find('conclusions') > -1 or
              (line.strip().find('final remarks') > -1) and (line.strip().find('final remarks') < 10))\
                and intro_count >= 1:
            period_separator = line.strip().find('.')

            if period_separator == -1:
                period_separator = line.strip().find(' ')

            if period_separator < 4:
                if period_separator == -1:
                    index = content_split[idx - 2].strip()
                    if index.find('.') > -1:
                        index = content_split[idx - 2].strip().replace('.', '')
                        try:
                            intro_index = int(index)
                        except ValueError:
                            roman_numeral_headers = not roman_numeral_headers
                            intro_index = roman.fromRoman(index.upper())
                        conclusion_flag = not conclusion_flag
                else:
                    conclusion_flag = not conclusion_flag
        elif (line.strip().find('acknowledgment') > -1
              or line.strip().find('acknowledgement') > -1
              or line.strip().find('references') > -1
              or line.strip().find('bibliograph') > -1) \
                and conclusion_flag:
            conclusion_flag = not conclusion_flag
            break
        elif (abstract_count == 1) or (intro_count == 1) or conclusion_flag:
            if len(content_split[idx].strip()) > 0:
                if len(line.strip().split(' ')) > 2:
                    to_process += line.strip() + ' '
                    newline_count = 0
            elif newline_count <= 2:
                # to_process += ' ' + line.strip() + '\n\n'
                # if len(line.strip().split(' ')) > 3:
                to_process += '\n\n' + line.strip() + ' '
                newline_count += 1
    to_process = to_process.replace('\n\n', '\n')
    return to_process

text_tiles = {}

def run():
    for idx, filename in enumerate(os.listdir(os.getcwd()+'/papers')):
        paper_path = os.getcwd() + '/papers/' + filename

        content = (convert_pdf_to_txt(paper_path))\
            .lower()\
            .replace('.   ', '. ')\
            .replace('.  ', '. ')\
            # .replace('\n\n', '\n')\
            # .replace('\f', '')
            # .replace('\n', ' ')\
            # .replace('-', ' ')\

        relevant_text = get_intro_conclusion(content)

        relevant_text = relevant_text\
            .replace('.   ', '. ')\
            .replace('.  ', '. ')\
            .replace('- ', '')

        # Utilising NLTK Text Tiling with default params
        # seg_2 = TextTilingTokenizer().tokenize(relevant_text)

        # Utilising NLTK Text Tiling with custom params(pseudosentence size, block comparison size)
        tt = TextTilingTokenizer(w=10, k=4)
        paper_tiles = tt.tokenize(relevant_text)

        text_tiles[idx] = paper_tiles

    return text_tiles



    # summaries = open(os.getcwd() + '/' + 'summaries.txt', 'a')
    # summaries.write('\nAbstract ' + str(idx+1)+'\n')
    # abstract = get_abstract(content)
    # summaries.write(abstract)
    # summaries.write('\n-----------------------------\n')
    # summaries.close()
