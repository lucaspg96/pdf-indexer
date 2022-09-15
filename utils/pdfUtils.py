import PyPDF2 
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

def text_fix(text):
    return text\
            .replace(" -\n","")\
            .replace("-\n","")\
            .replace("\n", " ")

def process_file(file):
    pdfFileObj = open(file, 'rb') 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

    num_pages = pdfReader.numPages
    pages = []
    for i in range(num_pages):
        
        pageObj = pdfReader.getPage(i) 

        # extracting text from page 
        pages.append({
                "file": file,
                "page": i+1,
                "totalPages": num_pages,
                "content": text_fix(pageObj.extractText())
            })

    pdfFileObj.close() 

    return pages
    