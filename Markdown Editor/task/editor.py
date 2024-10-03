import string

INVALID_LEVEL = "The level should be within the range of 1 to 6"
INVALID_INPUT = "Unknown formatting type or command"
INVALID_ROWS = "The number of rows should be greater than zero"
COMMANDS = ("!help", "!done")
FORMATTERS = {
    "header": string.Template("$level $text\n"),
    "plain": string.Template("$text"),
    "bold": string.Template("**$text**"),
    "italic": string.Template("*$text*"),
    "inline-code": string.Template("`$text`"),
    "new-line": "\n",
    "link": string.Template("[$label]($url)"),
    "ordered-list": string.Template("$row $text\n"),
    "unordered-list": string.Template("* $text\n"),
}


def print_help():
    print("Available formatters:", *FORMATTERS.keys())
    print("Available commands:", *COMMANDS)


def done(output_text):
    with open("output.md", "w") as f:
        f.write(output_text)
    print("Session saved to output.md")
    exit()


def get_valid_input(prompt, error_message, validation_fn):
    while True:
        try:
            value = int(input(prompt))
            if validation_fn(value):
                return value
            else:
                print(error_message)
        except ValueError:
            print(error_message)


def header():
    user_header_level = get_valid_input("Level: ", INVALID_LEVEL, lambda x: 1 <= x <= 6)
    user_text = input("Text: ")
    return FORMATTERS["header"].substitute(level='#' * user_header_level, text=user_text)


def emphasis(user_emphasis):
    user_text = input("Text: ")
    return FORMATTERS[user_emphasis].substitute(text=user_text)


def formatted_list(user_list):
    user_list_rows = get_valid_input("Number of rows: ", INVALID_ROWS, lambda x: x > 0)
    user_text = ''
    for row in range(1, user_list_rows + 1):
        item_text = input(f"Row #{row}: ")
        if user_list == "ordered-list":
            user_text += FORMATTERS[user_list].substitute(row=f"{row}.", text=item_text)
        else:
            user_text += FORMATTERS[user_list].substitute(text=item_text)

    return user_text


def link():
    user_label = input("Label: ")
    user_url = input("URL: ")
    return FORMATTERS["link"].substitute(label=user_label, url=user_url)


def main():
    output_text = ""
    while True:
        user_input = input("Choose a formatter: ").strip()

        if user_input in COMMANDS:
            if user_input == "!help":
                print_help()
            elif user_input == "!done":
                done(output_text)  # Save the result and exit
        elif user_input in FORMATTERS:
            if user_input == "header":
                output_text += header()
            elif user_input in ["plain", "bold", "italic", "inline-code"]:
                output_text += emphasis(user_input)
            elif user_input == "link":
                output_text += link()
            elif user_input in ["ordered-list", "unordered-list"]:
                output_text += formatted_list(user_input)
            else:
                output_text += FORMATTERS["new-line"]

            print(output_text)
        else:
            print(INVALID_INPUT)


if __name__ == "__main__":
    main()
