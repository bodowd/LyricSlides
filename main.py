from typing import List, Dict
import time
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import LyricSlides as ls
import Hymn
import config

config = config.Config()


def replace_with_hyphen(config_hymn_numbers: List, i: int):
    """
    If there is no hymn number for the language, replace the empty list with a '-'
    :param config_hymn_numbers:
    :param i:
    :return:
    """
    if len(config_hymn_numbers) == 0:
        num = '-'
    else:
        num = config_hymn_numbers[i]
    return num


def print_verse(verse_dict: Dict, k: int):
    """
    Helper function print the verses onto the slide to keep it DRY
    :param verse_dict:
    :param k:
    :return:
    """
    verse = f'{k}\n'
    for line in verse_dict[k]:
        verse += (line + '\n')
    return verse


### google API code

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations',
          'https://www.googleapis.com/auth/drive']

#### Authentication code from google
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('slides', 'v1', credentials=creds)

# create presentation
presentation = ls.create_presentation(title=config.presentation_title, slides_service=service)

def extract_lyrics(verse_dict: Dict, k: str):
    # extract the lyrics from verse_dict which will be the text that goes into the slide
    if 'chorus' in verse_dict:
        # add chorus to the end of each verse except for first verse, which already has it in
        if k != '1' and k != 'chorus':
            # print the verse as normal, then print the chorus
            verse = print_verse(verse_dict, k)
            for count, line in enumerate(verse_dict['chorus']):
                # add empty line between the verse and the chorus
                if count == 0:
                    verse += ('\n')
                verse += (line + '\n')
        # otherwise k == '1' or it's chorus but that is handled in the loop below and will be skipped
        else:
            verse = print_verse(verse_dict, k)
    else:
        verse = print_verse(verse_dict, k)
    return verse


slide_count = 0
for i in range(len(config.de_hymn_numbers)):
    # for each hymn number, get lyrics
    de_num = replace_with_hyphen(config.de_hymn_numbers, i)
    e_num = replace_with_hyphen(config.e_hymn_numbers, i)
    c_num = replace_with_hyphen(config.c_hymn_numbers, i)
    r_num = replace_with_hyphen(config.r_hymn_numbers, i)
    f_num = replace_with_hyphen(config.f_hymn_numbers, i)

    # get lyrics
    hymn = Hymn.Hymn()
    de_verse_dict = hymn.get_lyrics(hymn_number=de_num, language='DE')
    e_verse_dict = hymn.get_lyrics(hymn_number=e_num, language='E')

    # make slide for each verse
    for k in de_verse_dict.keys():
        if k == 'chorus':
            continue
        de_verse = extract_lyrics(verse_dict=de_verse_dict, k=k)
        e_verse = extract_lyrics(verse_dict=e_verse_dict, k=k)
        # create slides
        page_id = f'Slide_{slide_count}'
        slide = ls.Slides(presentation_id=presentation, slides_service=service, page_id=page_id)
        response = slide.create_slide(insertion_index=str(slide_count))
        if config.sleep:
            time.sleep(5)
        response = slide.create_textbox_with_text(lyrics_list=de_verse, english_lyrics_list=e_verse,
                                                  song_numbers_str=f'DE{de_num}, E{e_num}, C{c_num}, R{r_num}, F{f_num}')
        response = slide.alter_text_format()
        response = slide.update_slide_background()
        slide_count += 1

    # close the selenium session after each iteration because a new one will start again on the next
    hymn.driver.quit()