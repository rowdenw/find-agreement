class ColorScheme:
    def __init__(self, *colors):
        self._color = {}
        for index, color in enumerate(colors):
            self._color[index] = color

    def get_color(self, type):
        return self._color.get(type, '')

    def set_color(self, type, color):
        self._color[type] = color


def GoodacreColorScheme(column_Matthew, column_Mark, column_Luke):
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


def get_agreement_type(in_passage):
    agreement_type = 0
    for passage in in_passage:
        agreement_type += 2**passage
    return agreement_type
