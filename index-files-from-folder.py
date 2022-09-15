from utils import configUtils, elasticUtils, pdfUtils
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
config = configUtils.get_config("files")

files_dir = config.get("sourceFolder", "files/")
files = [join(files_dir, f) for f in listdir(files_dir) if isfile(join(files_dir, f))]

print(f"Found {len(files)} to index. Starting...")
elasticUtils.create_index()
for file in tqdm(files):
    pages = pdfUtils.process_file(file)
    elasticUtils.insert_document_pages(pages)