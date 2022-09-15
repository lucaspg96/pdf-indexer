from utils import driveUtils, elasticUtils, pdfUtils
from tqdm import tqdm
from os import listdir
from os.path import isfile, join

new_files = driveUtils.download_files(new_only=True)

if len(new_files) == 0:
    print("")

for file in tqdm(new_files):
    pages = pdfUtils.process_file(file)
    elasticUtils.insert_document_pages(pages)