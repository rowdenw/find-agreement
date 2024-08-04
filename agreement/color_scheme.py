from typing import List, Dict, Optional

class ColorScheme:
    def __init__(self, *colors: Optional[str]):
        self._color_map: Dict[int, Optional[str]] = {index: colors[index] for index in range(len(colors))}

    def get_color(self, type: int) -> Optional[str]:
        return self._color_map.get(type, '')

    def set_color(self, type: int, color: str) -> None:
        self._color_map[type] = color


def GoodacreColorScheme(column_Matthew: int, column_Mark: int, column_Luke: int) -> ColorScheme:
    colorScheme = ColorScheme()
    # https://markgoodacre.org/maze/synopses.htm
    colorScheme.set_color(get_agreement_type([column_Matthew]), "blue")
    colorScheme.set_color(get_agreement_type([column_Mark]), "red")
    colorScheme.set_color(get_agreement_type([column_Luke]), "yellow")
    colorScheme.set_color(get_agreement_type([column_Matthew, column_Mark]),
                          "purple")
    colorScheme.set_color(get_agreement_type([column_Matthew, column_Luke]),
                          "green")
    colorScheme.set_color(get_agreement_type([column_Mark, column_Luke]),
                          "orange")
    colorScheme.set_color(get_agreement_type([column_Matthew, column_Mark,
                                              column_Luke]), "brown")
    return colorScheme


def get_agreement_type(in_passage: List[int]) -> int:
    agreement_type = 0
    for passage in in_passage:
        agreement_type += 2**passage
    return agreement_type
