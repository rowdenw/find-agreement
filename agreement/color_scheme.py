from typing import List, Dict, NamedTuple, KeysView, Optional

class ColorScheme:
    def __init__(self, *colors: Optional[str]):
        self._color: Dict[int, Optional[str]] = {index: colors[index] for index in range(len(colors))}

    def get_color(self, type) -> Optional[str]:
        return self._color.get(type, '')

    def set_color(self, type, color) -> None:
        self._color[type] = color


# List of allowed Rich colors here
# https://rich.readthedocs.io/en/stable/appendix/colors.html

class GoodacreColorScheme(ColorScheme):
    def __init__(self, column_Matthew: int, column_Mark: int, column_Luke: int, use_CSS_colors: bool = False):
        super().__init__()
        # https://markgoodacre.org/maze/synopses.htm
        super().set_color(get_agreement_type([column_Matthew]), "blue")
        super().set_color(get_agreement_type([column_Mark]), "red")
        super().set_color(get_agreement_type([column_Luke]), "yellow")
        super().set_color(get_agreement_type([column_Matthew, column_Mark]),
                            "purple")
        super().set_color(get_agreement_type([column_Matthew, column_Luke]),
                            "green")

        orange_name = "orange" if use_CSS_colors else "orange"
        super().set_color(get_agreement_type([column_Mark, column_Luke]),
                            orange_name)

        brown_name = "sienna" if use_CSS_colors else "brown"
        super().set_color(get_agreement_type([column_Matthew, column_Mark,
                                                column_Luke]), brown_name)


def get_agreement_type(in_passage):
    agreement_type = 0
    for passage in in_passage:
        agreement_type += 2**passage
    return agreement_type
