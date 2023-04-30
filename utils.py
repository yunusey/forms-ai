def colorful_print(text: str, r: int, g: int, b: int):
    print("\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text),
          end="")
