#!/usr/bin/env python

import datetime
import sys
import click
import xml.etree.ElementTree as ET


def count_for_year(gamelist, year):
    count = 0

    for i in gamelist:
        added = i.find("addeddate/timestamp").text
        if added:
            add_date = datetime.datetime.fromtimestamp(int(added))
            if add_date.year == year:
                count += 1

    print(f"\n>> Total number of games in the year {year}: {count}")


@click.command()
@click.option('-y', '--year', type=int, default=None)
@click.option('-c', '--count', is_flag=True, default=False)
@click.argument('filename', type=str, default=None)
def main(year, count, filename):
    if filename is None:
        filename = sys.stdin

    tree = ET.parse(filename)
    root = tree.getroot()
    gamelist = root.findall("data/gameinfo/gamelist/game")

    if count:
        print(f"\n>> Total number of games in collection: {len(gamelist)}")

    if year:
        count_for_year(gamelist, year)


if __name__ == "__main__":
    main()
