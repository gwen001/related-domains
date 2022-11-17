<h1 align="center">related-domains</h1>

<h4 align="center">Find related domains of a given domain using Whoxy API.</h4>

<p align="center">
    <img src="https://img.shields.io/badge/python-v3-blue" alt="python badge">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT license badge">
    <a href="https://twitter.com/intent/tweet?text=https%3a%2f%2fgithub.com%2fgwen001%2frelated-domains%2f" target="_blank"><img src="https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fgwen001%2Frelated-domains" alt="twitter badge"></a>
</p>

<p align="center">
    <img src="https://img.shields.io/github/stars/gwen001/related-domains?style=social" alt="github stars badge">
    <img src="https://img.shields.io/github/watchers/gwen001/related-domains?style=social" alt="github watchers badge">
    <img src="https://img.shields.io/github/forks/gwen001/related-domains?style=social" alt="github forks badge">
</p>

---

## Install

```
git clone https://github.com/gwen001/related-domains
cd related-domains
pip3 install -r requirements.txt
```

## Usage

```
$ python3 related-domains.py -d example.com -k $WHOXY_KEY
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
  -v, --verbose         enable verbose mode, default off
```

---

<img src="https://raw.githubusercontent.com/gwen001/related-domains/main/preview.png" />
<img src="https://raw.githubusercontent.com/gwen001/related-domains/main/whoxy.png" />

---

Feel free to [open an issue](/../../issues/) if you have any problem with the script.  

