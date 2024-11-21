def main():
    workspace/github.com/Johnyboi77/bookbot/books = "books/frankenstein.txt"
    text = get_book_text(workspace/github.com/Johnyboi77/bookbot/books)
    print(text)


def get_book_text(path):
    with open(path) as f:
        return f.read()
    
main()