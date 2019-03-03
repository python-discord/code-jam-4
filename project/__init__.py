from project.spelling import correction, is_correct, misspell
import traceback

while True:
    word = input('Enter word: ').strip()
    if word:
        try:
            if not is_correct(word):
                word = correction(word)

            print(f"Correct word: {word}")

            misspelled = misspell(word)

            print(f"Misspelled word: {misspelled}")
        except:
            traceback.print_exc()
    else:
        break