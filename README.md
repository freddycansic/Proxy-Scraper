# Proxy-Scraper

Pulls proxies from www.freeproxy.world and adds them to your proxychains config.

## Usage

    ./proxyscraper -h

    usage: proxyscraper.py [-h] [-p NUM_PROXIES] [-f FILE_PATH] [-mR MIN_RESPONSE] [-v]

    Automatically scrapes socks5 proxies from www.freeproxy.world then selects 10 (default) to add to your proxychains
    config.

    optional arguments:
        -h, --help          show this help message and exit
        -p NUM_PROXIES, --proxies NUM_PROXIES
                            the number of proxies to add to your config file. (default = 10)
        -f FILE_PATH, --file-path FILE_PATH
                            the file path of your proxychains config file. (default = /etc/proxychains.conf)
        -mR IN_RESPONSE, --min-response MIN_RESPONSE
                        specify the minimum response time of proxies in milliseconds. (default = 5000)
        -v, --verbose       run this program in verbose mode.

    Author: Freddy Cansick 2/2/2022
