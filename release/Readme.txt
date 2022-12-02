Much greeting

What this does:
----------------------------------------------------------------------------
- Searches PDFs with text; runs all text through a natural language
processing AI; finds all words contextually identified as verbs; highlights
those words in the PDF. 
- The module used to find verbs is NTLK Perceptron. It's experimentally the
best part-of-speech tagger in language processing; some revision will still
be needed, but if the text is clean it'll correctly identify the part-of-speech
of 85-90% of words. So you'll get much verb.

How to run:
----------------------------------------------------------------------------
1. Put all PDF files you want to analyse in the source_docs folder.
2. Click the crow.
3. If it doesn't work - run 'failsafe.bat'.
4. The files with highlighted verbs will be in the output_docs folder.
----------------------------------------------------------------------------

Important:
----------------------------------------------------------------------------
- If possible, avoid using scanned PDFs. If using decisions from BAILII,
instead of opening the pdf go to the decision page, where the decision text
is pre-cleaned. Right click and print page as pdf.
- If you MUST run a scanned PDF through the program, it must have recognized
text.
- Rename source files before running the program. Filenames longer than 200
chars will break the app :(
- Remember to eat and stay hydrated
- Don't rename or move the folders.
- If you run the program with files still in the output_docs folder, it'll
overwrite them.
----------------------------------------------------------------------------

Have a good night
