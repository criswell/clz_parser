#!/usr/bin/env python

import datetime
import sys
import click
import xml.etree.ElementTree as ET


def system_breakdown(gamelist):
    systems = {}
    longest_len = 0
    for i in gamelist:
        plat = i.find("platform/displayname").text
        if len(plat) > longest_len:
            longest_len = len(plat)
        if plat in systems:
            systems[plat] += 1
        else:
            systems[plat] = 1

    sorted_keys = sorted(systems.items(), key=lambda x:x[1], reverse=True)

    print(f"\n>> Total number of games per system:")
    for k in sorted_keys:
        print(f"\t{k[0]} {'.' * (longest_len + 2 - len(k[0]))} {k[1]}")


def count_for_year(gamelist, year, flags):
    updated_list = []

    for i in gamelist:
        added = i.find("addeddate/timestamp").text
        if added:
            add_date = datetime.datetime.fromtimestamp(int(added))
            if add_date.year == year:
                updated_list.append(i)

    print(f"\n>> Total number of games in the year {year}: {len(updated_list)}")
    if flags["system"]:
        system_breakdown(updated_list)


@click.command()
@click.option('-y', '--year', type=int, default=None)
@click.option('-c', '--count', is_flag=True, default=False)
@click.option('-s', '--system', is_flag=True, default=None)
@click.option('-f', '--format', default=None)
@click.argument('filename', type=str, default=None)
def main(year, count, system, format, filename):
    if filename is None:
        filename = sys.stdin

    tree = ET.parse(filename)
    root = tree.getroot()
    gamelist = root.findall("data/gameinfo/gamelist/game")

    flags = {"system": system, "format": format}

    if count:
        print(f"\n>> Total number of games in collection: {len(gamelist)}")
        if system:
            system_breakdown(gamelist)

    if year:
        count_for_year(gamelist, year, flags)


if __name__ == "__main__":
    main()
