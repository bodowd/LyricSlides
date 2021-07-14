"""
Following: https://github.com/googleworkspace/python-samples/blob/master/slides/snippets/slides_snippets.py
Google Slides API: https://developers.google.com/slides/reference/rest/v1/presentations.pages/text#Page.ParagraphStyle
"""
from typing import List


def create_presentation(title: str, slides_service):
    service = slides_service
    body = {
        'title': title
    }
    presentation = service.presentations().create(body=body).execute()
    presentation_id = presentation.get('presentationId')
    print(f'Created presentation with ID: {presentation_id}')
    return presentation_id


class Slides(object):
    def __init__(self, presentation_id: str, slides_service: str, page_id: str):
        self.presentation_id = presentation_id
        self.slides_service = slides_service
        self.page_id = page_id
        self.left_box_id = 'Left_box_'+self.page_id
        self.right_box_id = 'Right_box_'+self.page_id
        self.song_numbers_box_id = 'Song_number_box_'+self.page_id
        self.FONT_SIZE = 21
        self.TITLE_FONT_SIZE = 40
        self.bold = False

    def create_slide(self, insertion_index: str):
        service = self.slides_service
        requests = [
            {
                'createSlide': {
                    'objectId': self.page_id,
                    'insertionIndex': insertion_index
                }
            }
        ]
        body = {
            'requests': requests
        }
        response = service.presentations().batchUpdate(presentationId=self.presentation_id, body=body).execute()
        create_slide_response = response.get('replies')[0].get('createSlide')
        obj_id = create_slide_response.get('objectId')
        print(f'Created slide with ID: {obj_id}')
        return response

    def create_textbox_with_text(self, lyrics_list: List, english_lyrics_list: List,
                                 song_numbers_str: str = 'DE123, E123, F123'):
        """
        add lyrics into a text box
        :param lyrics_list:
        :param song_numbers_str:
        :return:
        """

        service = self.slides_service

        songNumbersBoxHeight = {
            'magnitude': 50,
            'unit': 'PT'
        }
        songNumbersBoxWidth = {
            'magnitude': 680,
            'unit': 'PT'
        }

        lyricsBoxSize = {
            'magnitude': 300,
            'unit': 'PT'
        }

        requests = [
            # create the right text box
            {
                'createShape': {
                    'objectId': self.right_box_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': self.page_id,
                        'size': {
                            'height': lyricsBoxSize,
                            'width': lyricsBoxSize
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 380,
                            'translateY': 50,
                            'unit': 'PT'
                        }
                    }
                }
            },
            # create left text box
            {
                'createShape': {
                    'objectId': self.left_box_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': self.page_id,
                        'size': {
                            'height': lyricsBoxSize,
                            'width': lyricsBoxSize
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 20,
                            'translateY': 50,
                            'unit': 'PT'
                        }
                    }
                }
            },
            # create the title text box with song numbers
            {
                'createShape': {
                    'objectId': self.song_numbers_box_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': self.page_id,
                        'size': {
                            'height': songNumbersBoxHeight,
                            'width': songNumbersBoxWidth
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 20,
                            'translateY': 5,
                            'unit': 'PT'
                        }
                    }
                }
            },
            # insert text into the box
            {
                'insertText': {
                    'objectId': self.song_numbers_box_id,
                    'insertionIndex': 0,
                    'text': song_numbers_str
                }
            },
            {
                'insertText': {
                    'objectId': self.left_box_id,
                    'insertionIndex': 0,
                    'text': lyrics_list,
                }
            },
            {
                'insertText': {
                    'objectId': self.right_box_id,
                    'insertionIndex': 0,
                    'text': english_lyrics_list
                }
            }
        ]
        body = {
            'requests': requests
        }
        response = service.presentations().batchUpdate(presentationId=self.presentation_id, body=body).execute()
        create_shape_response = response.get('replies')[0].get('createShape')
        obj_id = create_shape_response.get('objectId')
        print(f'Created textbox with ID: {obj_id}')

    def alter_text_format(self):
        """
        Alters the text format (fonts, centering...) in the text boxes, id for the boxes are already in the class from
        instantiation
        """
        service = self.slides_service
        requests = [
            {
                'updateParagraphStyle': {
                    'objectId': self.song_numbers_box_id,
                    'style': {
                        'alignment': 'CENTER'
                    },
                    'fields': 'alignment'
                }
            },
            {
                'updateTextStyle': {
                    'objectId': self.song_numbers_box_id,
                    'style': {
                        'bold': self.bold,
                        'fontFamily': 'Arial',
                        'fontSize': {
                            'magnitude': self.TITLE_FONT_SIZE,  # numbers slightly larger than lyrics
                            'unit': 'PT'
                        },
                        'foregroundColor': {
                            'opaqueColor': {
                                'rgbColor': {
                                    'blue': 1.0,
                                    'green': 1.0,
                                    'red': 1.0
                                }
                            }
                        }
                    },
                    'fields': 'bold,foregroundColor,fontFamily,fontSize'
                }
            },
            {
                'updateTextStyle': {
                    'objectId': self.left_box_id,
                    'style': {
                        'bold': self.bold,
                        'fontFamily': 'Arial',
                        'fontSize': {
                            'magnitude': self.FONT_SIZE,
                            'unit': 'PT'
                        },
                        'foregroundColor': {
                            'opaqueColor': {
                                'rgbColor': {
                                    'blue': 1.0,
                                    'green': 1.0,
                                    'red': 1.0
                                }
                            }
                        }
                    },
                    'fields': 'bold,foregroundColor,fontFamily,fontSize'
                }
            },
            {
                'updateTextStyle': {
                    'objectId': self.right_box_id,
                    'style': {
                        'bold': self.bold,
                        'fontFamily': 'Arial',
                        'fontSize': {
                            'magnitude': self.FONT_SIZE,
                            'unit': 'PT'
                        },
                        'foregroundColor': {
                            'opaqueColor': {
                                'rgbColor': {
                                    'blue': 1.0,
                                    'green': 1.0,
                                    'red': 1.0
                                }
                            }
                        }
                    },
                    'fields': 'bold,foregroundColor,fontFamily,fontSize'
                }
            }
        ]
        body = {
            'requests': requests
        }
        response = service.presentations().batchUpdate(presentationId=self.presentation_id, body=body).execute()
        print(f'Updated the text style for shape with ID: {self.left_box_id}')
        return response

    def update_slide_background(self):
        """
        Make the background blue
        :return:
        """
        service = self.slides_service
        requests = [
            {
                'updatePageProperties': {
                    'objectId': self.page_id,
                    'pageProperties': {
                        'pageBackgroundFill': {
                            'solidFill': {
                                'color': {
                                    'rgbColor': {
                                        'red': 0.0,
                                        'green': 0.0,
                                        'blue': 1.0
                                    }
                                }
                            }
                        }
                    },
                    'fields': 'pageBackgroundFill'
                }
            }
        ]
        body = {
            'requests': requests
        }
        response = service.presentations().batchUpdate(presentationId=self.presentation_id,
                                                       body=body).execute()
        print(f'Updated the background for shape with ID: {self.left_box_id}')
        return response
