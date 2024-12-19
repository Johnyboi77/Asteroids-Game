from enum import Enum

class TextType(Enum):
    normal_text = *
    bold_text = ** **
    italic_text = * *
    code_text = ``` ```
    links = [link]()
    images =![alt text for image]()

class TextNode(self):