class Config:
    presentation_title = 'Test API'
    # English hymn numbers
    e_hymn_numbers = [279]
    # German hymn numbers
    de_hymn_numbers = [135]
    # russian
    r_hymn_numbers = [215]
    # farsi
    f_hymn_numbers = []
    # chinese
    c_hymn_numbers = [227]
    # if hymn is really long, add sleep so that you don't go over a limit of API calls per minute
    sleep = False
