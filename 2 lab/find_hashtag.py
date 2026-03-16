def find_hashtag(string_with_hashtag: str) -> str:
    words = string_with_hashtag.split()

    result = ""

    for word in words:
        if word[0] == "#":
            result = word[1:]
            break
    
    return result.upper()


def main():
    string_with_hashtag = input()

    print(find_hashtag(string_with_hashtag))


if __name__ == "__main__":
    main()