#!/usr/bin/env python

import datetime
import sys
import click
import xml.etree.ElementTree as ET


def system_breakdown(gamelist):
    systems = {}
    for i in gamelist:
        plat = i.find("platform/displayname").text
        if plat in systems:
            systems[plat] += 1
        else:
            systems[plat] = 1

    print(f"\n>> Total number of games per system:")
    for k in systems.keys():
        print(f"\t{k}\t\t{systems[k]}")


def count_for_year(gamelist, year, system):
    updated_list = []

    for i in gamelist:
        added = i.find("addeddate/timestamp").text
        if added:
            add_date = datetime.datetime.fromtimestamp(int(added))
            if add_date.year == year:
                updated_list.append(i)

    print(f"\n>> Total number of games in the year {year}: {len(updated_list)}")
    if system:
        system_breakdown(updated_list)


@click.command()
@click.option('-y', '--year', type=int, default=None)
@click.option('-c', '--count', is_flag=True, default=False)
@click.option('-s', '--system', is_flag=True, default=None)
@click.argument('filename', type=str, default=None)
def main(year, count, system, filename):
    if filename is None:
        filename = sys.stdin

    tree = ET.parse(filename)
    root = tree.getroot()
    gamelist = root.findall("data/gameinfo/gamelist/game")

    if count:
        print(f"\n>> Total number of games in collection: {len(gamelist)}")
        if system:
            system_breakdown(gamelist)

    if year:
        count_for_year(gamelist, year, system)


if __name__ == "__main__":
    main()
