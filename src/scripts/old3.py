import nltk, os, argparse, re, fitz, string, time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from typing import Tuple
from io import BytesIO

INPUT_FILE = '2_Dow_331.pdf'
OUTPUT_FILE = '2_Dow_331_ANALYSED.pdf'

def main():
    print("VerbFinder 0.1")
    print("by/for L.M.")
    print("-----------")
    
    py_txt = import_text(INPUT_FILE)
    verblist = find_verbs(py_txt)
    process_data(INPUT_FILE, OUTPUT_FILE, verblist)
    
    print("Done.")

# Import full text from PDF
def import_text(input_file: str, pages: Tuple = None):
    print('Importing text.')
    # Open the PDF
    pdfDoc = fitz.open(input_file)
    # Save the generated PDF to memory buffer
    output_buffer = BytesIO()
    text_list = []
    # Iterate through pages
    for pg in range(pdfDoc.page_count):
            if pages:
                if str(pg) not in pages:
                    continue
            # Select the page
            page = pdfDoc[pg]
            # Get text
            text = page.get_text("text")
            text_list.append(text)
    pdfDoc.close()
    fulltext = ' '.join(text_list)
    #remove hyphens and line breaks
    fulltext = fulltext.replace("­", "")
    fulltext = fulltext.replace("\n", "")
    fulltext = fulltext.replace("—", "")
    return(fulltext)

# Search for text within PDF
def search_for_text(lines, search_str):
    for line in lines:
        # Find all matches within one line
        results = re.findall(search_str, line, re.IGNORECASE)
        # In case multiple matches within one line
        for result in results:
            yield result

# Highlight values within PDF
def highlight_matching_data(page, matched_values, type):
    matches_found = 0
    places = []
    for val in matched_values:
        highlight = None
        places = []
        matches_found += 1
        matching_val_area = page.search_for(val)
        for i in matching_val_area:
            highlight = page.add_highlight_annot(i)
            highlight.update()
    return matches_found

def process_data(input_file: str, output_file: str, search_list, action: str = 'Highlight'):
    # Open the PDF
    pdfDoc = fitz.open(input_file)
    # Save the generated PDF to memory buffer
    output_buffer = BytesIO()
    total_matches = 0
    # Iterate through words
    for wrd in search_list:
        # Iterate through pages
        for pg in range(pdfDoc.page_count):
            # Select the page
            page = pdfDoc[pg]
            # Split page by linesb
            page_lines = page.get_text("text").split('\n')
            search_word = "[^a-zA-Z]" + wrd + "[^a-zA-Z]"
            matched_values = search_for_text(page_lines, search_word)
            if matched_values:
                matches_found = highlight_matching_data(page, matched_values, 'Highlight')
                total_matches += matches_found
    print(f"{total_matches} words highlighted in: {input_file}")
    # Save to output
    pdfDoc.save(output_buffer)
    pdfDoc.close()
    # Save the output buffer to the output file
    with open(output_file, mode='wb') as f:
        f.write(output_buffer.getbuffer())

def find_verbs(text: str):
    print("Finding verbs.")
    py_token = nltk.word_tokenize(text) # list of words
    py_tag = nltk.pos_tag(py_token) # list of word-tag tuples
    verblist = [] # list of found verbs
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

    return(verblist)

main()