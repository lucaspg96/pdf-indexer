from utils import driveUtils, elasticUtils, pdfUtils
from tqdm import tqdm

downloaded_files = driveUtils.download_files()

print(f"Downloaded {len(downloaded_files)} files. Starting indexing...")
elasticUtils.create_index()

for file in tqdm(downloaded_files):
    pages = pdfUtils.process_file(file)
    elasticUtils.insert_document_pages(pages)