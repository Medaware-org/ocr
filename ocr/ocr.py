import easyocr

# https://pypi.org/project/easyocr/

lang_list = ['de', 'en']
reader = easyocr.Reader(lang_list, gpu=True)  # this needs to run only once to load the model into memory


def read(image, detail=False) -> list[tuple[list[list[int]]], str, float] | list[str]:
    """
    Reads the text of an image using easyocr.
    :param image: file path or numpy-array or a byte stream object
    :param detail: False | True -> False = text; Ture = bounding box, detected text and confident level
    :return:
    """
    return reader.readtext(image, detail=detail)  # , rotation_info=[90, 180, 270])


if __name__ == '__main__':
    text: list[str] = read("./images/text_01.png", detail=False)
    print(text)
