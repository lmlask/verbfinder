import nltk, os, argparse, re, fitz, string, time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from typing import Tuple
from io import BytesIO
import requests as req
import json

INPUT_FILE = '2_Dow_331.pdf'
OUTPUT_FILE = '2_Dow_331_ANALYSED.pdf'

def main():
    print("VerbFinder 0.1")
    print("by/for L.M.")
    print("-----------")

    pdfDoc = fitz.open(INPUT_FILE)  #Create pdf file object
    output_buffer = BytesIO()       #Create buffer

    py_txt = import_text(pdfDoc)    #Import pdf text
    verblist = find_verbs(py_txt)   #Find all verbs

    for pg in range(pdfDoc.page_count):
        # Select the page
        page = pdfDoc[pg]
        highlight_matching_data(page, verblist, 'Highlight')

    # Save to output buffer
    pdfDoc.save(output_buffer)
    pdfDoc.close()
    # Save the output buffer to the output file
    with open(OUTPUT_FILE, mode='wb') as f:
        f.write(output_buffer.getbuffer())# Possible trouble

    print("Done.")

    # Problem is not in the verblist, verblist is fine

# Import full text from PDF
def import_text(input_file): # DONE
    print('Importing text.')
    text_list = []
    # Iterate through pages and append page text to a list
    for pg in range(input_file.page_count):
        page = input_file[pg]
        text = page.get_text("text")
        text_list.append(text)
    # join list into full document text
    fulltext = '\n'.join(text_list)
    #r emove hyphens and line breaks
    fulltext = fulltext.replace("­", "")
    fulltext = fulltext.replace("\n", "")
    fulltext = fulltext.replace("—", "")
    # return single string w full document text
    return(fulltext)

def find_verbs(text: str): # DONE
    print("Finding verbs.")
    print("Verbs are found contextually and may look weird in isolated form.")
    py_token = nltk.word_tokenize(text) # list of words
    py_tag = nltk.pos_tag(py_token) # list of word-tag tuples
    verblist = [] # list of found verbs

    lenght = len(py_tag) #full lenght of tags
    processed = 0

    for i in py_tag:
        if i[1][0] == 'V' and i[0].lower() != "s":
            verblist.append(i[0])
        processed += 1
    verblist = list(dict.fromkeys(verblist)) #remove duplicates
    punctuation = string.punctuation + '.' + '-'

    for x in range(0, len(verblist)): #remove punctuation
        verblist[x] = re.sub('[^a-zA-Z]', "", verblist[x])

    for v in verblist:    #remove single letter verbs
        if len(v) <= 1:
            verblist = [value for value in verblist if value != v]

    print(f"Found {len(verblist)} verbs: ")

    upper_list = [i.upper() for i in verblist]
    print(", ".join(upper_list))

    return(verblist) # DONE # DONE # DONE

# Search for text within PDF
def search_for_text(lines, search_str): # PROBLEM IS HERE.
    """
    Search for the search string within the document lines
    """
    for line in lines:
        # Find all matches within one line
        results = re.findall(search_str, line, re.IGNORECASE)
        # In case multiple matches within one line
        for result in results:
            yield result # Possible trouble

# Highlight values within PDF
def highlight_matching_data(page, wordlist, type): # DONE #Pass a customized wordlist for each page. Each word in the customized wordlist should include the char actually found in the page before and after the word.
    for val in wordlist:
        highlight = None
        matching_val_area = page.search_for(val)

        for i in matching_val_area:
            highlight = page.add_highlight_annot(i)
            highlight.update()

        # # To change the highlight colar
        # # highlight.setColors({"stroke":(0,0,1),"fill":(0.75,0.8,0.95) })
        # # highlight.setColors(stroke = fitz.utils.getColor('white'), fill = fitz.utils.getColor('red'))
        # # highlight.setColors(colors= fitz.utils.getColor('red'))

    return

main()