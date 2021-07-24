from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
from typing import Dict


class Hymn(object):
    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def get_lyrics(self, hymn_number: int, language='DE') -> Dict:
        """
        :param hymn_number:
        :return: Dict. verse_dict
        """
        if language == 'DE':
            self.driver.get(f"https://songbase.life/german_hymnal/{hymn_number}")
        elif language == 'E':
            self.driver.get(f"https://songbase.life/english_hymnal/{hymn_number}")
        else:
            raise ("Language not supported.")

        soup = bs(self.driver.page_source, "html.parser")
        # get all divs with either class line or verse-number
        verses = soup.findAll("div", {'class': ['line', 'verse-number', 'chorus']})
        verse_dict = {}

        # some songs are only one verse long and songbase.life doesn't display a verse number. In this case make a
        # verse_number 1
        HAS_VERSES = False
        for i in verses:
            if i['class'] == ['verse-number']:
                HAS_VERSES = True
        if not HAS_VERSES:
            verse_number = '1'
            verse_dict[verse_number] = []

        for i in verses:
            if i['class'] == ['verse-number']:
                verse_number = i['data-uncopyable-text']
                verse_dict[verse_number] = []
            elif i['class'] == ['line']:
                # check if it is an empty line used for spacing
                # or this weird extra line that appears before verse number is ever defined
                if i.text == '' or i.text == 'Hohelied':
                    pass
                else:
                    verse_dict[verse_number].append(i.text)
            # may not handle hymns with two choruses
            elif i['class'] == ['chorus']:
                if i.text == '':
                    pass
                else:
                    verse_dict['chorus'] = i.text.split('\n')
            else:
                print('Unrecognized div class')
        return verse_dict

# test
if __name__ == "__main__":
    hymn = Hymn()
    print(hymn.get_lyrics(hymn_number=546, language='E'))
    hymn.driver.quit()
