#!/usr/bin/python3

import os
import sys
import requests
import argparse
from colored import fg, bg, attr

w_blacklist = [ 'privacy', 'redacted', 'dnstination', 'west' ]

def extractDatas( t_json ):
    for index in ['technical_contact','registrant_contact','administrative_contact']:
        if index in t_json:
            company,email = extractData( t_json[index] )
            if company and company not in t_datas['companies']:
                t_datas['companies'].append( company )
            if email and email not in t_datas['emails']:
                t_datas['emails'].append( email )


def extractData( tab ):
    if not 'company_name' in tab:
        company = False
    elif 'registrant_contact' in t_json and 'company_name' in t_json['registrant_contact']:
        company = t_json['registrant_contact']['company_name']
        for wbl in w_blacklist:
            if wbl in company.lower():
                company = False
                break
    else:
        company = False


    if not 'email_address' in tab:
        email = False
    elif 'registrant_contact' in t_json and 'email_address' in t_json['registrant_contact']:
        email = t_json['registrant_contact']['email_address']
        for wbl in w_blacklist:
            if wbl in email.lower():
                email = False
                break
    else:
        email = False

    return company,email


parser = argparse.ArgumentParser()
parser.add_argument( "-e","--email",help="email you are looking for (required or -d or -c)" )
parser.add_argument( "-c","--company",help="company you are looking for (required or -d or -e)" )
parser.add_argument( "-d","--domain",help="domain you already know (required or -c)" )
parser.add_argument( "-k","--key",help="whoxy api key (required)" )
parser.add_argument( "-v","--verbose",help="enable verbose mode, default off", action="store_true" )
parser.parse_args()
args = parser.parse_args()

t_domains = []
t_datas = {
    'companies': [],
    'emails': []
}

if args.verbose:
    _verbose = True
else:
    _verbose = False

if args.company:
    t_datas['companies'].append( args.company )

if args.email:
    t_datas['emails'].append( args.email )

if args.domain:
    _domain = args.domain
else:
    _domain = False

if not _domain and not len(t_datas['companies']) and not len(t_datas['emails']):
    parser.error( 'domain or company or email required' )

if args.key:
    _key = args.key
else:
    parser.error( 'api key is required' )


if _domain:
    if _verbose:
        sys.stdout.write( '%s[+] search for domain: %s%s\n' % (fg('green'),_domain,attr(0)) )
    url = 'http://api.whoxy.com/?key='+_key+'&whois='+_domain
    if _verbose:
        print(url)
    r = requests.get( url )
    t_json = r.json()
    # print(t_json)
    extractDatas( t_json )
    if _verbose:
        print(t_datas)


for company in t_datas['companies']:
    page = 1
    company = company.replace( ' ', '+' )
    if _verbose:
        sys.stdout.write( '%s[+] search for company: %s%s\n' % (fg('green'),company,attr(0)) )

    while True:
        url = 'http://api.whoxy.com/?key='+_key+'&reverse=whois&company='+company+'&mode=micro&page='+str(page)
        page = page + 1
        if _verbose:
            print(url)
        r = requests.get( url )
        t_json = r.json()
        # print(t_json)

        if 'search_result' in t_json and len(t_json['search_result']):
            for result in t_json['search_result']:
                if not result['domain_name'] in t_domains:
                    t_domains.append( result['domain_name'] )
                    print( result['domain_name'] )
        else:
            break


for email in t_datas['emails']:
    page = 1
    if _verbose:
        sys.stdout.write( '%s[+] search for email: %s%s\n' % (fg('green'),email,attr(0)) )

    while True:
        url = 'http://api.whoxy.com/?key='+_key+'&reverse=whois&email='+email+'&mode=micro&page='+str(page)
        page = page + 1
        if _verbose:
            print(url)
        r = requests.get( url )
        t_json = r.json()
        # print(t_json)

        if 'search_result' in t_json and len(t_json['search_result']):
            for result in t_json['search_result']:
                if not result['domain_name'] in t_domains:
                    t_domains.append( result['domain_name'] )
                    print( result['domain_name'] )
        else:
            break
