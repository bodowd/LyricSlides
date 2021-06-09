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

    def get_lyrics(self, hymn_number: int) -> Dict:
        """
        :param hymn_number:
        :return: Dict. verse_dict
        """
        self.driver.get(f"https://songbase.life/german_hymnal/{hymn_number}")

        soup = bs(self.driver.page_source, "html.parser")
        # get all divs with either class line or verse-number
        verses = soup.findAll("div", {'class': ['line', 'verse-number']})
        verse_dict = {}
        for i in verses:
            if i['class'] == ['verse-number']:
                verse_number = i['data-uncopyable-text']
                verse_dict[verse_number] = []
            elif i['class'] == ['line']:
                # check if it is an empty line used for spacing
                if i.text == '':
                    pass
                else:
                    verse_dict[verse_number].append(i.text)
            else:
                print('Unrecognized div class')
        return verse_dict

# test
if __name__ == "__main__":
    hymn = Hymn()
    print(hymn.get_lyrics(hymn_number=93))
    hymn.driver.quit()