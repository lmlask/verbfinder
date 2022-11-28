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
    print("--------------------------------")
    print("by/for L.M.")

    directory = '../source_docs'
    for filename in os.listdir(directory):
        if filename[-4:] != '.pdf': # Guard clause for non-PDF files
            continue
        print("--------------------------------")
        print('Processing ' + filename + '...')
        input_file = '../source_docs/' + filename
        output_file = '../output_docs/' + filename
        py_txt = import_text(input_file)
        verblist = find_verbs(py_txt)
        print("Highlighting words.")
        process_data(input_file, output_file, verblist)
    
    print("Done.")

# Import full text from PDF
def import_text(input_file: str, pages: Tuple = None):#DONE
    print('Importing text...')
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
    fulltext = ''.join(text_list)
    #remove hyphens and line breaks
    fulltext = fulltext.replace("­", "")
    fulltext = fulltext.replace("\n", "")
    fulltext = fulltext.replace("—", "")
    return(fulltext)

def find_verbs(text: str):#DONE
    print("Finding verbs...")
    py_token = nltk.word_tokenize(text) # list of words
    py_tag = nltk.pos_tag(py_token) # list of word-tag tuples
    verblist = [] # list of found verbs
    processed = 0
    for i in py_tag:
        if i[1][0] == 'V':
            verblist.append(i[0])
        processed += 1
    verblist = list(dict.fromkeys(verblist)) #remove duplicates
    punctuation = string.punctuation + '.' + '-'
    for x in range(0, len(verblist)): #remove punctuation
        verblist[x] = re.sub('[^a-zA-Z]', "", verblist[x])
    for v in verblist:    #remove single letter verbs
        if len(v) <= 1:
            verblist = [value for value in verblist if value != v]
    print(f"Found {len(verblist)} verbs.")
    # upper_list = [i.upper() for i in verblist]
    # print(", ".join(upper_list))
    return(verblist)

# Search for text within PDF
def search_for_text(text, search_str):#DONE
    results = re.findall(search_str, text, re.IGNORECASE)
    results = list(dict.fromkeys(results))
    # In case multiple matches within one line
    for result in results:
        yield result

# Highlight values within PDF
def highlight_matching_data(page, matched_values, type):#DONE
    matches_found = 0
    places = []
    for val in matched_values: # this is being called once for every time the value is in the page
        highlight = None
        places = []
        matches_found += 1
        matching_val_area = page.search_for(val)
        for i in matching_val_area:
            highlight = page.add_highlight_annot(i)
            highlight.update()
    return matches_found

def process_data(input_file: str, output_file: str, search_list, action: str = 'Highlight'):#DONE BUT MESSY
    # Open the PDF
    pdfDoc = fitz.open(input_file)
    # Save the generated PDF to memory buffer
    output_buffer = BytesIO()
    total_matches = 0
    # Iterate through words
    for wrd in search_list:
        # Iterate through pages
        for pg in range(pdfDoc.page_count): # This is working - called once, per verb, per page
            # Select the page
            page = pdfDoc[pg]
            # Split page by linesb
            page_text = page.get_text("text")
            search_word = "[^a-zA-Z]" + wrd + "[^a-zA-Z]"
            matched_values = search_for_text(page_text, search_word)
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

main()