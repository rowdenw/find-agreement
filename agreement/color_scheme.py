from typing import List, Dict, KeysView, Optional

class ColorScheme:
    """
    A class to map integer "agreement type" codes to display color descriptors.

    Attributes:
    -----------
    _color : Dict[int, str]
        A dictionary mapping integer keys (1 to 7) to string color values.

    Methods:
    --------
    __init__(colors: Dict[int, str] = None):
        Initializes the ColorScheme with a dictionary of colors, where keys are integers (1 to 7) 
        and values are color strings.
    
    get_color(type: int) -> Optional[str]:
        Returns the color associated with the given type key. If the key does not exist, returns an empty string.
    
    set_color(type: int, color: str) -> None:
        Sets the color for the given type key. If the key already exists, it updates the value.
    
    keys() -> KeysView[int]:
        Returns a view of all the keys in the color scheme.
    """
    def __init__(self, colors: Dict[int, str] = None):
        """
        Validates parameters and initializes the internal dictionary.

        Parameters:
        -----------
        colors : Dict[int, str], optional
            A dictionary mapping integers (1 to 7) to color strings. Defaults to an empty dictionary.

        Raises:
        -------
        ValueError if keys are out of range or values are not strings.
        """
        self._color: Dict[int, str]
        if colors:
            for key, value in colors.items():
                if not isinstance(key, int) or not 1 <= key <= 7:
                    raise ValueError("Keys must be integers between 1 and 7")
                if not isinstance(value, str):
                    raise ValueError("Values must be strings representing colors")
            self._color = colors
        else:
            self._color = {}

    def get_color(self, type) -> Optional[str]:
        return self._color.get(type, '')

    def set_color(self, type, color) -> None:
        self._color[type] = color

    @property
    def keys(self) -> KeysView[int]:
        return self._color.keys()


# List of allowed Rich colors here
# https://rich.readthedocs.io/en/stable/appendix/colors.html

class GoodacreColorScheme(ColorScheme):
    def __init__(self, column_Matthew: int, column_Mark: int, column_Luke: int, use_CSS_colors: bool = False):
        """
        Initializes a color map according to the Goodacre color scheme, based on the positions of the columns.

        Parameters:
        -----------
        column_Matthew:
        column_Mark:
        column_Luke:
            The positions of the respective books in the synoptic table, i.e. 0 == left, 1 == middle, 2 == right

        use_CSS_colors:
            if True, switch to using color descriptors that are friendly to CSS styles.
        
        Raises:
        -------
        ValueError if keys are out of range or values are not strings.
        """
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
