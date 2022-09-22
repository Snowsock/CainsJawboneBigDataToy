import pandas as pd
import PIL.Image
import pytesseract
import multiprocessing

from pdf2image import convert_from_path


def pdf_to_img(pdf):
    image = convert_from_path(pdf)

    for i in range(len(image)):
        # Save pages as images in the pdf
        image[i].save('page' + str(i + 1) + '.jpg', 'JPEG')


def word_count(text) -> dict:
    words = text.split()
    words_on_page = dict()
    word: str
    for word in words:
        word.strip()
        if word in words_on_page:
            words_on_page[word] += 1
        else:
            words_on_page[word] = 1
    return words_on_page


def extract_text_from_doc(page_number: int) -> dict:
    return pytesseract.image_to_string(PIL.Image.open(rf'page{page_number}.jpg').rotate(-90, expand=True))


def make_data_frame(page_number: int) -> pd.DataFrame:
    return pd.DataFrame(word_count(
        extract_text_from_doc(page_number)).items(), columns=['Word', 'Freq'])


def menu():
    print("This is a menu:\n1: Read in files\n2: analyse pages\nQ: Quit the program")
    str_input: str = input()
    if str_input == "1":
        print("Which file do you want to make into pictures?\n")
        pdf_to_img(f"{input()}.pdf")
        print("DONE!")
        menu()
    elif str_input == "2":
        print("How many pages do you want to analyze today?")
        processes = []
        for x in (n + 1 for n in range(int(input()))):
            processes.append(multiprocessing.Process(target=Page, args=(x,)))
            processes[x-1].start()
        print("DONE!")
        menu()
    elif str_input == "Q" or str_input == "q":
        exit(0)


class Page:
    """
    class that defines a page object
    values:
        page_number: the number of the page from 1...
        words_on_page: a dictionary with the words on the page, and the number of occurrences
        page_data_frame: a pandas dataframe representing the page
    """

    def __init__(self, page_number: int):
        self.words_on_page = extract_text_from_doc(page_number)
        self.page_data_frame = make_data_frame(page_number)
        print(self.page_data_frame)

    def get_words_on_page(self):
        return self.words_on_page

    def get_page_data_frame(self):
        return self.page_data_frame


if __name__ == "__main__":
    print(
        """
       _..._                                                                                                            .---.                               .-'''-.                                    
    .-'_..._''.                                                          _______                                        |   |                              '   _    \                                  
  .' .'      '.\         .--.   _..._                .                   \  ___ `'.                                     '---'                   /|       /   /` '.   \    _..._         __.....__      
 / .'                    |__| .'     '.            .'|                    ' |--.\  \                                    .---.            _     _||      .   |     \  '  .'     '.   .-''         '.    
. '                      .--..   .-.   .          <  |                    | |    \  '                                   |   |      /\    \\   //||      |   '      |  '.   .-.   . /     .-''"'-.  `.  
| |                 __   |  ||  '   '  |           | |             __     | |     |  '              __                  |   |    __`\\  //\\ // ||  __  \    \     / / |  '   '  |/     /________\   \ 
| |              .:--.'. |  ||  |   |  |           | | .'''-.   .:--.'.   | |     |  |           .:--.'.                |   | .:--.'.\`//  \'/  ||/'__ '.`.   ` ..' /  |  |   |  ||                  | 
. '             / |   \ ||  ||  |   |  |           | |/.'''. \ / |   \ |  | |     ' .'          / |   \ |               |   |/ |   \ |\|   |/   |:/`  '. '  '-...-'`   |  |   |  |\    .-------------' 
 \ '.          .`" __ | ||  ||  |   |  |           |  /    | | `" __ | |  | |___.' /'           `" __ | |               |   |`" __ | | '        ||     | |             |  |   |  | \    '-.____...---. 
  '. `._____.-'/ .'.''| ||__||  |   |  |           | |     | |  .'.''| | /_______.'/             .'.''| |               |   | .'.''| |          ||\    / '             |  |   |  |  `.             .'  
    `-.______ / / /   | |_   |  |   |  |           | |     | | / /   | |_\_______|/             / /   | |_           __.'   '/ /   | |_         |/\'..' /              |  |   |  |    `''-...... -'    
             `  \ \._,\ '/   |  |   |  |           | '.    | '.\ \._,\ '/                       \ \._,\ '/          |      ' \ \._,\ '/         '  `'-'`               |  |   |  |                     
                 `--'  `"    '--'   '--'           '---'   '---'`--'  `"                         `--'  `"           |____.'   `--'  `"                                 '--'   '--'                     
        """
    )
    menu()
