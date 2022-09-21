import pandas as pd
import PIL.Image
import pytesseract
import advertools as adv

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
    print("How many pages do you want to analyze today?")
    for x in (n + 1 for n in range(int(input()))):
        Page(x)


class Page:
    """
    class that defines a page object
    values:
        page_number: the number of the page from 1...
        words_on_page: a dictionary with the words on the page, and the number of occurrences
    """
    def __init__(self, page_number: int):
        words_on_page = extract_text_from_doc(page_number)
        page_data_frame = make_data_frame(page_number)
        print(page_data_frame)


if __name__ == "__main__":
    # pdf_to_img("test.pdf")
    menu()
