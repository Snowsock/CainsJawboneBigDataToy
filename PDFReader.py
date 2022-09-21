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


class Page:
    """
    class that defines a page object
    values:
        page_number: the number of the page from 1...
        words_on_page: a dictionary with the words on the page, and the number of occurences
    """

    page_number: int
    words_on_page: dict

    def __init__(self, page_number: int):
        self.page_number = page_number
        self.words_on_page = dict()

    def word_count(self, text):
        words = text.split()
        words_on_page = dict()
        for word in words:
            if word in words_on_page:
                words_on_page[word] += 1
            else:
                words_on_page[word] = 1
        return words_on_page

    def make_data_frame(self, page_number):
        print(pd.DataFrame(self.word_count(
            pytesseract.image_to_string(PIL.Image.open(rf'page{page_number}.jpg').rotate(-90, expand=True))).items()),
              columns=['Word', 'Freq'])


if __name__ == "__main__":
    # pdf_to_img("test.pdf")
    p = Page(1)
    print(p.word_count(pytesseract.image_to_string(PIL.Image.open(r'page1.jpg').rotate(-90, expand=True))))
