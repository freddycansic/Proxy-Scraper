#!/bin/python3

import requests
import random
import argparse 
import os
import sys

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
END = "\033[0m"
BOLD = "\033[1m"
ORANGE = "\033[48:2:255:165:0m"

ERROR = RED + "[!]" + END
FATAL = ORANGE + BOLD + "[FATAL]" + END
OK = GREEN + "[+]" + END
ALERT = YELLOW + "[#]" + END
VERBOSE = BLUE + BOLD + "[V]" + END
OUTPUT = "[*]"

parser = argparse.ArgumentParser(description="Automatically scrapes socks5 proxies from www.freeproxy.world then selects 10 (default) to add to your proxychains config.", epilog="Author: Freddy Cansick 2/2/2022")
parser.add_argument("-p", "--proxies", metavar="NUM_PROXIES", type=int, default=10, help="the number of proxies to add to your config file. (default = 10)")
parser.add_argument("-f", "--file-path", default="/etc/proxychains4.conf", help="the file path of your proxychains config file. (default = /etc/proxychains.conf)")
parser.add_argument("-mR", "--min-response", type=int, default=3000, help="specify the minimum response time of proxies in milliseconds. (default = 5000)")
parser.add_argument("-v", "--verbose", action="store_true", help="run this program in verbose mode.")
args = parser.parse_args()

if os.geteuid() != 0:
    print(f"{FATAL} Please run this file as root!")
    sys.exit()

if not os.path.exists("/etc/proxychains4.conf"):
    print(f"{FATAL} Proxychains config file not located at default location of \"/etc/proxychains4.conf\"!")
    print(f"{OUTPUT} Specify the location of the config using -f or --file-path")
    sys.exit()

proxylist = []
pagenum = 0
while True: # get first 15 pages
    pagenum += 1

    res = requests.get(f"https://www.freeproxy.world/?type=socks5&anonymity=&country=&speed={args.min_response}&port=&page={pagenum}", timeout=5)
    if not res:
        print(f"{ERROR} Request to https://www.freeproxy.world/?type=socks5&anonymity=&country=&speed={args.min_response}&port=&page={pagenum} resulted in a timeout after 5 seconds of get requests...")
        continue # try the next page

    page = res.text.split("\n")

    containsProxy = False
    for index, line in enumerate(page):
        if len(line) and line[0].isdigit(): # if the line length != 0 and is a digit
            containsProxy = True
            portline = page[index + 3]
            port = portline[portline.find("=", 15)+1:portline.find("\"", 15)]

            proxy = "socks5 " + line + " " + port

            proxylist.append(proxy)
    
    if not containsProxy: # if page doesnt contain a proxy = end scraping
        break

    print(f"{OK} Proxies successfully scraped from https://www.freeproxy.world/?type=socks5&anonymity=&country=&speed={args.min_response}&port=&page={pagenum}")

proxylist = list(set(proxylist)) # remove duplicates then conv back to list
print(f"{OUTPUT} {len(proxylist)} socks5 proxies scraped from www.freeproxy.world.\n")

print(f"{OUTPUT} Randomly selecting {args.proxies} proxies to add to config...")
if args.proxies > len(proxylist):
    print(f"{FATAL} Cannot select more proxies ({args.proxies}) than number of scraped proxies ({len(proxylist)})")
    sys.exit()

randomsample = random.sample(proxylist, args.proxies) 

if args.verbose:
    for proxy in randomsample:
        print(f"{VERBOSE} {proxy}")

with open(args.file_path, "r+") as file:
    lines = file.readlines()

    # add proxyscraper tag
    lines.append("# [PROXYSCRAPER PROXIES]\n")

    lines = lines[:lines.index("# [PROXYSCRAPER PROXIES]\n")+1]

    # add proxies to the end of the file
    for proxy in randomsample:
        lines.append(proxy + "\n")

    # overwrite new contents
    file.seek(0)
    file.writelines(lines)
    file.truncate()