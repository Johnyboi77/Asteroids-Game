def main():
    book_path = /github.com/Johnyboi77/bookbot/books
    text = get_book_text(/github.com/Johnyboi77/bookbot/books/frankenstein.txt)
    print(text)


def get_book_text(/github.com/Johnyboi77/bookbot/books):
    with open(/github.com/Johnyboi77/bookbot/books/frankenstein.txt) as f:
        return f.read()


main()