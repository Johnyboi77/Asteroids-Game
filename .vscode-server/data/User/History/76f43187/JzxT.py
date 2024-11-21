def main():
    book_path = "/root/workspace/github.com/Johnyboi77/bookbot/books/frankenstein.txt"
    text = get_book_text(book_path)
    words_counted = count_words(text)
    print("Number of words:", words_counted)


def get_book_text(path):
    with open(path) as f:
        return f.read()

def count_words (text):
    word_list = text.split()
    word_count = 0
    for word in word_list:
        word_count += 1
    return word_count

def count_characters (text):
    text = text.lower()
    character_counts = {}
    for character in text: 
        if character in character_count: 
            character_counts (character) += 1
        else: 
            character_counts (character) = 0
    
if __name__ == "__main__":  

    main()