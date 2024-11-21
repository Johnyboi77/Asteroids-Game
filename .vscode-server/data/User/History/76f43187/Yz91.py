def main():
    book_path = "/root/workspace/github.com/Johnyboi77/bookbot/books/frankenstein.txt"
    text = get_book_text(book_path)
    words_counted = count_words(text)
    character_counted = count_character(text)
    print("Number of words:", words_counted)
    print("character counted", character_counted)

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
    character_count = {}
    for character in text: 
        if character in character_count: 
            character_count [character]+= 1
        else: 
            character_count [character] = 1
    return character_count

if __name__ == "__main__":  

    main()
