import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import LyricSlides as ls

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
presentation = ls.create_presentation(title='Test API', slides_service=service)

# get lyrics
# TODO: code for scraping the lyrics
verse_dict = {'1': ['Wie allumfassend, Herr, Du bist!',
  'Von Gott sind wir in Dir –',
  'Was Du für uns geworden bist,',
  'So sehr genießen wir.'],
 '2': ['Die Weisheit Gottes bist Du uns,',
  'Gott rettet uns durch Dich;',
  'Der Weg zur Rettung Du nur bist,',
  'Allein und ewiglich.'],
 '3': ['Du bist für uns Gerechtigkeit,',
  'Der Gottes Recht erfüllt;',
  'Wir alle sind gerecht in Dir,',
  'Ins beste Kleid umhüllt.'],
 '4': ['Herr, Du bist unsre Heiligkeit,',
  'Umwandlung brauchen wir;',
  'In Dir Du heiligst tadellos,',
  'Uns gleichgestaltest Dir.'],
 '5': ['Erlösung bist Du auch für uns,',
  'Dein Abbild unser wird;',
  'Verklären wirst Du unsern Leib,',
  'Von Freiheit sublimiert.'],
 '6': ['Wenn wir nun sinnen über Dich,',
  'Genießen Dich, den Herrn,',
  'So nähert sich Dein Kommen mehr,',
  'Du bleibst nicht lange fern.'],
 '7': ['Wie süß der Vorgeschmack doch ist,',
  'So herrlich und so reich!',
  'Wir sehnen uns bei Dir zu sein,',
  'In Füll erfahrn Dich.']}

for k in verse_dict.keys():
    verse = f'{k}\n'
    for line in verse_dict[k]:
        verse += (line+'\n')

    # create slides
    page_id = f'Slide_{k}'
    slide = ls.Slides(presentation_id=presentation, slides_service=service, page_id=page_id)
    response = slide.create_slide(insertion_index=str(k))
    response = slide.create_textbox_with_text(lyrics_list=verse, song_numbers_str='DE123, E123, F123')
    response = slide.alter_text_format()
    response = slide.update_slide_background()

