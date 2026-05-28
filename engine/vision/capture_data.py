# script encargado de ordenar los datos leídos de la pantalla

from pprint import pprint
from engine.logic.objects import Item, Stat

COLS = [
    "minStat",
    "maxStat",
    "statValue",
    "statName",
    "modificationState",
    "runeTier1",
    "runeTier2",
    "runeTier3"
]

current_data = {}


def save_capture_data(row, row_name):
    global current_data

    stat_value, stat_name = parse_current_stat(row[2])

    new_row = [
        row[0],              # minStat
        row[1],              # maxStat
        stat_value,          # statValue
        stat_name,           # statName
        row[3],              # modificationState
        row[4],              # smallRune
        row[5],              # mediumRune
        row[6]               # bigRune
    ]

    row_with_labels = dict(zip(COLS, new_row))
    current_data[row_name] = row_with_labels

    if row_name == "ROW13":
        print("\n=== save_capture_data ===")
        pprint(current_data, sort_dicts=False)

        map_data(current_data)


def parse_current_stat(text):

    if text == "":
        return "", ""

    i = 0
    if text[i] in "+-":
        i += 1

    while i < len(text) and text[i].isdigit():
        i += 1

    stat_value = text[:i]
    stat_name = text[i:].strip()

    return stat_value, stat_name


def map_data(capture_data):

    item = Item(
        item_type="Botas",
        mage_type="Zapateromago",
        sink=0
    )

    for row_name, data in capture_data.items():

        stat_name = data["statName"]

        existing_stat = next(
            (
                stat
                for stat in item.stats
                if stat.stat_name == stat_name
            ),
            None
        )

        if existing_stat:

            existing_stat.min_stat = int(data["minStat"] or 0)
            existing_stat.max_stat = int(data["maxStat"] or 0)
            existing_stat.stat_value = int(data["statValue"] or 0)

            existing_stat.modification_state = data["modificationState"]

            existing_stat.rune_tier1 = int(data["runeTier1"] or 0)
            existing_stat.rune_tier2 = int(data["runeTier2"] or 0)
            existing_stat.rune_tier3 = int(data["runeTier3"] or 0)

            existing_stat.row_name = row_name

        else:
            item.stats.append(
                Stat(
                    stat_name=stat_name,

                    min_stat=int(data["minStat"] or 0),
                    max_stat=int(data["maxStat"] or 0),
                    stat_value=int(data["statValue"] or 0),

                    modification_state=data["modificationState"],

                    rune_tier1=int(data["runeTier1"] or 0),
                    rune_tier2=int(data["runeTier2"] or 0),
                    rune_tier3=int(data["runeTier3"] or 0),

                    row_name=row_name
                )
            )

    print(f"Mapeo: {item}")

    return item