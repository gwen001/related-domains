<h1 align="center">related-domains</h1>

<h4 align="center">Find related domains of a given domain using Whoxy API.</h4>

<p align="center">
    <img src="https://img.shields.io/badge/python-v3-blue" alt="python badge">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT license badge">
    <a href="https://twitter.com/intent/tweet?text=https%3a%2f%2fgithub.com%2fgwen001%2frelated-domains%2f" target="_blank"><img src="https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fgwen001%2Frelated-domains" alt="twitter badge"></a>
</p>

<!-- <p align="center">
    <img src="https://img.shields.io/github/stars/gwen001/related-domains?style=social" alt="github stars badge">
    <img src="https://img.shields.io/github/watchers/gwen001/related-domains?style=social" alt="github watchers badge">
    <img src="https://img.shields.io/github/forks/gwen001/related-domains?style=social" alt="github forks badge">
</p> -->

---

## Description

This Python tool does not search for similar domains, it uses the informations of the domain you provide (contact email, organization...) to search for domains that have been registered by the same peoples/companies. So the results are quite reliable.

## Sources

Implemented sources are:

- builtwith.com
- whoxy.com

## Requirements

You need a [WHOXY API key](https://www.whoxy.com/) but <b><ins>it's free</ins></b>.

## Install

```
git clone https://github.com/gwen001/related-domains
cd related-domains
pip3 install -r requirements.txt
```

## Usage

```
$ python3 related-domains.py -d example.com -k xxxxxxxxxxxxxxxxxxxxxx
```

```
usage: related-domains.py [-h] [-e EMAIL] [-c COMPANY] [-d DOMAIN] [-k KEY] [-v]

options:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        email you are looking for (required or -d or -c)
  -c COMPANY, --company COMPANY
                        company you are looking for (required or -d or -e)
  -d DOMAIN, --domain DOMAIN
                        domain you already know (required or -c)
  -k KEY, --key KEY     whoxy api key (required)
  -s SOURCE, --source SOURCE
                        list of sources separated by comma, available sources are: builtwith,crtsh,whoxy (default=whoxy)
  -v, --verbose         enable verbose mode, default off
```

## Changelog

- 2023-07-18: builtwith re-enabled and crtsh added
- 2023-04-28: remove builtwith because it was not relevant at all, fix a fatal bug
- 2023-03-26: code review & builtwith added


---

<img src="https://raw.githubusercontent.com/gwen001/related-domains/master/preview.gif" />

---

Feel free to [open an issue](/../../issues/) if you have any problem with the script.  

