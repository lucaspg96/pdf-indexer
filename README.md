# pdf-indexer
Code to easily index pdfs into elasticsearch and query over them

## ElasticSearch

ElasticSearch and Kibana are available at a [docker-compose.yml](./elastic/docker-compose.yml) file. There is a volume being mounted to persist the created indexes at [elastic/es-index](./elastic/es-index/), **which should not be versioned**.

To do more customization at elasticsearch, it is possible to edit the [index-mappings](./index-mappings.json) and [index-settings](./index-settings.json) files to adjust the index configuration to better suit your needs. The current configuration is best suited for Brazillian texts.

## How to run

There are 4 main scripts so far:

- `index-files-from-folder.py`, which will read the files at `files.sourceFolder` and index them at elasticsearch;

- `create-index-from-drive-files.py`, which will read a Google Drive folder, retrieve the files and then index them;

- `update-index-with-drive-files.py`, which will look for files in the Google Drive folder that are not indexed yet.

- `run-search.py`, which will execute a search over the index and present the results;

## Configuration

This script uses a [config.yml](./config.yml) to enable fast modifications on the execution.
The configurations are self-explanatory. The configuration can be overwritten by using environment variables following the [Spring Boot pattern](https://www.tutorialworks.com/spring-boot-kubernetes-override-properties/#:~:text=In%20Spring%20Boot%2C%20any%20property,the%20dots%20changed%20to%20underscores.&text=This%20means%20that%20if%20we,environment%20variable%20in%20the%20container.), where a config under the path `my.db.config` can be overwritten by the environment variable `MY_DB_CONFIG`.

## Enabling Google Drive access

To communicate with Google Drive, it is needed to create a project and the credentials file as instructed on [Google Drive API Python Quickstart](https://developers.google.com/drive/api/quickstart/python). After creating the credentials file, it must be saved at `credentials.json`. 

At the first execution, it will be needed to log in on google and authorize the application to access your google drive (even for public folders). After that, a `token.json` file will be created, allowing logging in automatically on the next executions.

**DO NOT SHARE OR VERSION THOSE FILES**

## Points to improve

- Centralize the entry points in a more simple way to use;
- Upgrade the PDF parser to use some OCR strategy, allowing it to proccess PDFs with images;
- Wrap the solution inside some application to provide a more friendly search;
- Create some Docker artifacts for agile deployment;