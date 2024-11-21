def main():
    book_path = "books/frankenstein.txt"
    text = get_book_text(book_path)
    print(text)


def get_book_text(path):
    with open(path) as f:
        return f.read()

if __name__ == "__main__":  

def count_words (text):
        word_list = text.split()
        word_count = 0
        for word in word_list:
            word_count += 1
        return word_count


    main()
