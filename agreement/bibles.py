from agreement.bible_api import get_bibles


def main():
    bibles = get_bibles()
    print(
        bibles.loc[bibles["id"].str.startswith("grc"),
                   "version"].to_string(index=False)
    )


if __name__ == "__main__":
    main()
