"""This file is used to store all user facing text,
where Starwort then transcribes it into katakana."""


class menu:
    class unhelpful:
        name = "ウンヘルプフル メニュー"  # u n he ru pu fu ru   me nyu- | Unhelpful Menu
        nothing = "ヅー ノシング"  # do-   no shi n gu | Do nothing
        save = "セイヴ プロセソル タイム"
        # se i vu   pu ro se so ru   ta i mu | Save Processor Time
        close = "Close"

    class fileselect:
        file = " 【ファイル】"  # [fa i ru] | [FILE]
        folder = " 【フォルデル】"  # [fo ru de ru] | [FOLDER]
        new = "ニュー ファイル"  # nyu-   fa i ru | New File
        saveas = "セイヴ アズ…"  # se i vu   a zu … | Save As...

        class button:
            default = "セイヴ ヒル"  # se i vu   hi ru | Save Here
            special = "セイヴ ヒル\n【ファイルナム カッノト ビー エムプテイー オル ア スペシアル パス】"
            # se i vu   hi ru \n [fa i ru na mu   ka nno to   bi-   e mu pu te i-   o ru   a
            # su pe shi a ru   pa su]
            # Save Here [Filename cannot be empty or a special path]
            invalid = 'セイヴ ヒル\n【ファイルナム カッノト コンテイヌ エニー オヴ: \\/:*?"<>|】'
            # se i vu   hi ru \n [fa i ru na mu   ka nno to   ko n te i nu   e ni-   o vu:
            # \/:*?"<>|]
            # Save Here [Filename cannot contain any of: \/:*?"<>|]
            cancel = "カンセル"  # ka n se ru | Cancel

    class entry:
        x = "エクズ"  # e ku zu | X
        y = "ワイ"  # wa i | Y
        colour = "コロー"  # ko ro- | Colour
        confirm = "コンファーム"  # ko n fa- mu | Confirm
        colour_error = "コロー ムスト ビー ベトイーン 0 アンヅ 16777215"
        # ko ro-   mu su to   bi-   be to i- n   0   a n du   16777215
        # Colour must be between 0 and 16777215
        x_error = "X must be between 1 and {}"
        y_error = "Y must be between 1 and {}"


class general:
    title = "フレイムド"  # fu re i mu do | Framed
