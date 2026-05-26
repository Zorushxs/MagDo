# script encargado de ordenar los datos leídos de la pantalla

from pprint import pprint

COLS = [
    "minStat",
    "maxStat",
    "statNumber",
    "statName",
    "modificationState",
    "runeTier1",
    "runeTier2",
    "runeTier3"
]

current_data = {}


def save_capture_data(row, row_name):
    global current_data

    stat_number, stat_name = parse_current_stat(row[2])

    new_row = [
        row[0],              # minStat
        row[1],              # maxStat
        stat_number,         # statNumber
        stat_name,           # statName
        row[3],              # modificationState
        row[4],              # smallRune
        row[5],              # mediumRune
        row[6]               # bigRune
    ]

    row_with_labels = dict(zip(COLS, new_row))
    current_data[row_name] = row_with_labels

    if row_name == "ROW12":
        print("\n=== save_capture_data ===")
        pprint(current_data, sort_dicts=False)


def parse_current_stat(text):

    if text == "":
        return "", ""

    i = 0
    if text[i] in "+-":
        i += 1

    while i < len(text) and text[i].isdigit():
        i += 1

    stat_number = text[:i]
    stat_name = text[i:].strip()

    return stat_number, stat_name