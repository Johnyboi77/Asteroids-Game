def main():
    book_path = "/root/workspace/github.com/Johnyboi77/bookbot/books/frankenstein.txt"
    text = get_book_text(book_path)
    words_counted = count_words(text)
    character_counted = count_characters(text)
    print("--- Begin report of books/frankenstein.txt ---
        (words_counted) words found in the document

        The 'e' character was found (character_count) times
        The 't' character was found  times
        The 'a' character was found  times
        The 'o' character was found  times
        The 'i' character was found  times
        The 'n' character was found  times
        The 's' character was found  times
        The 'r' character was found  times
        The 'h' character was found  times
        The 'd' character was found  times
        The 'l' character was found  times
        The 'm' character was found  times
        The 'u' character was found  times
        The 'c' character was found  times
        The 'f' character was found  times
        The 'y' character was found  times
        The 'w' character was found  times
        The 'p' character was found  times
        The 'g' character was found  times
        The 'b' character was found  times
        The 'v' character was found  times
        The 'k' character was found  times
        The 'x' character was found  times
        The 'j' character was found  times
        The 'q' character was found  times
        The 'z' character was found  times
        --- End report ---")


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
