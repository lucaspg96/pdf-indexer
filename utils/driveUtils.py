import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .configUtils import get_config
from .elasticUtils import get_indexed_files
import io
from pathlib import Path

config = get_config("drive")

def get_or_create_credentials(
    SCOPES=['https://www.googleapis.com/auth/drive'],
    force_create=False
):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if not force_create and os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if force_create or (not creds or not creds.valid):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return creds

def download_files(new_only = False):

    folder_id = config["folderId"]
    save_folder = config.get("downloadPath", "files")

    if folder_id is None:
        raise Exception("Could not download files from Google Drive. Folder ID not informed")

    Path(save_folder).mkdir(parents=True, exist_ok=True)

    creds = get_or_create_credentials()
    downloaded_files = []
    indexed_files = get_indexed_files() if new_only else set()
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        while True:
            response = service.files()\
                                .list(q=f"'{folder_id}' in parents",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token)\
                                .execute()
            for file in response.get('files', []):
                # Process change
                file_name = file.get("name")
                if file_name in indexed_files:
                    continue
                    
                print(F'Found new file: {file_name}, {file.get("id")}')
                request = service.files().get_media(fileId=file.get("id"))
                file = io.BytesIO()
                downloader = MediaIoBaseDownload(file, request)
                done = False
                print("Starting download...", end="")
                while done is False:
                    status, done = downloader.next_chunk()
                
                save_file_name = os.path.join(save_folder,file_name)
                print("\rFile dowloaded", end="")
                with open(save_file_name,'wb') as out:
                    out.write(file.getvalue())
                print(f"\rFile saved at {save_file_name}")
                downloaded_files.append(save_file_name)

            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        print(F'An error occurred: {error}')
        files = None
        
    return downloaded_files