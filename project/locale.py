"""This file is used to store all user facing text,
where Starwort then transcribes it into katakana."""


class kata:
    class menu:
        class unhelpful:
            name = "ウンヘルプフル メニュー"
            # u n he ru pu fu ru   me nyu- | Unhelpful Menu
            nothing = "ヅー ノシング"  # do-   no shi n gu | Do nothing
            save = "セイヴ プロセソル タイム"
            # se i vu   pu ro se so ru   ta i mu | Save Processor Time
            close = "クロス"  # ku ro su | Close

        class new:
            name = "ニュー ファイル"  # nyu-   fa i ru | New File
            height = "ハイト"  # ha i to | Height
            width = "ウイヅ"  # u i dzu | Width
            create = "クリーエイト カンヴァス"
            # ku ri- e i to   ka n va su | Create Canvas

        class edit:
            name = "エッデト"  # e dde to | Edit
            undo = "ウンドウー"  # u n do u- | Undo
            redo = "リードブー"  # ri- do u- | Redo

        class fileselect:
            file = " 【ファイル】"  # [fa i ru] | [FILE]
            folder = " 【フォルダー】"  # [fo ru da-] | [FOLDER]
            new = "ニュー ファイル"  # nyu-   fa i ru | New File
            saveas = "セイヴ アズ…"  # se i vu   a zu … | Save As...
            open = "オーペヌ ファイル"  # o- pe nu   fa i ru | Open File

            class button:
                default = "セイヴ ヒール"  # se i vu   hi- ru | Save Here
                special = "セイヴ ヒール\n\
    【ファイルナム カッノト ビー エムプテイー オル ア スペシアル パス】"
                # se i vu   hi- ru \n [fa i ru na mu   ka nno to   bi-
                # e mu pu te i-   o ru   a   su pe shi a ru   pa su]
                # Save Here\n[Filename cannot be empty or a special path]
                invalid = 'セイヴ ヒール\n\
    【ファイルナム カッノト コンテイヌ エニー オヴ: \\/:*?"<>|】'
                # se i vu   hi- ru \n [fa i ru na mu   ka nno to
                # ko n te i nu   e ni-   o vu: \/:*?"<>|]
                # Save Here\n[Filename cannot contain any of: \/:*?"<>|]
                cancel = "カンセル"  # ka n se ru | Cancel

        class entry:
            x = "エクズ"  # e ku zu | X
            y = "ワイ"  # wa i | Y
            colour = "コラー"  # ko ra- | Colour
            confirm = "コンファーム"  # ko n fa- mu | Confirm
            colour_error = "コラー ムスト ビー ベトイーン 0 アンド 16777215"
            # ko ra-   mu su to   bi-   be to i- n   0   a n do   16777215
            # Colour must be between 0 and 16777215
            x_error = "エクズ ムスト ビー ベトイーン 1 アンド {}"
            # e ku zu   mu su to   bi-   be to i- n   1   a n do   {}
            # X must be between 1 and {}
            y_error = "ワイ ムスト ビー ベトイーン 1 アンド {}"
            # wa i   mu su to   bi-   be to i- n   1   a n do   {}
            # Y must be between 1 and {}

    class general:
        title = "フレイムド"  # fu re i mu do | Framed

        class corruptions:
            altercolour = "シュッフリング コラース…"  # shu ffu ri n gu   ko ra- su …
            # Shuffling Colours...
            pixelate = "ピクゼレイチング イマジュ…"  # pi ku ze re i chi n gu   i ma ju …
            # Pixelating Image...
            alterpixel = "シュッフリング ピクズルス…"  # shu ffu ri n gu   pi ku zu ru su…
            # Shuffling Pixels...


class eng:
    class menu:
        class unhelpful:
            name = "Unhelpful Menu"
            nothing = "Do Nothing"
            save = "Save Processor Time"
            close = "Close"

        class new:
            name = "New File"
            height = "Height"
            width = "Width"
            create = "Create Canvas"

        class edit:
            name = "Edit"
            undo = "Undo"
            redo = "Redo"

        class fileselect:
            file = " [FILE]"
            folder = " [FOLDER]"
            new = "New File"
            saveas = "Save As..."
            open = "Open File"

            class button:
                default = "Save Here"
                special = "Save Here\n\
[Filename cannot be a empty or a special path]"
                invalid = 'Save Here\n\
[Filename cannot contain any of: \\/:*?"<>|]'
                cancel = "Cancel"

        class entry:
            x = "X"
            y = "Y"
            colour = "Colour"
            confirm = "Confirm"
            colour_error = "Colour must be between 0 and 16777215"
            x_error = "X must be between 1 and {}"
            y_error = "Y must be between 1 and {}"

    class general:
        title = "Framed"

        class corruptions:
            altercolour = "Shuffling Colours..."
            pixelate = "Pixelating Image..."
            alterpixel = "Shuffling Pixels..."
