#!/usr/bin/python3

import os
import sys
import re
import requests
import argparse
from colored import fg, bg, attr

w_blacklist = [ 'privacy', 'redacted', 'dnstination', 'west' ]


# https://twitter.com/intigriti/status/1639610098954932225
def searchDomainBuiltwith( _domain ):
    global _verbose, t_data

    if _verbose:
        sys.stdout.write( '%s[+] calling builtwith targeting domain%s\n' % (fg('green'),attr(0)) )

    try:
        url = 'https://builtwith.com/relationships/'+_domain
        r = requests.get( url )
    except Exception as e:
        sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
        return

    rgxp = r'("https://builtwith.com/relationships/[^"]+)'
    matches = re.findall( rgxp, r.text, re.IGNORECASE )

    if matches:
        for m in matches:
            if not '/tag/' in m:
                domain = m.replace('https://builtwith.com/relationships/','').replace('"','')
                if not domain in t_data['domains']:
                    t_data['domains'].append( domain )
                    print( domain )


def searchDomainWhoxy( _domain, _whoxy_key ):
    global _verbose, t_data

    if _verbose:
        sys.stdout.write( '%s[+] whoxy key found, calling whoxy api targeting domain%s\n' % (fg('green'),attr(0)) )

    url = 'http://api.whoxy.com/?key='+_whoxy_key+'&whois='+_domain
    if _verbose:
        sys.stdout.write( '%s[+] %s%s\n' % (fg('white'),url,attr(0)) )

    try:
        r = requests.get( url )
        t_json = r.json()
        # print(t_json)
    except Exception as e:
        sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
        return

    extractDatasWhoxy( t_json )
    if _verbose:
        print(t_data)


def searchCompanyWhoxy( _whoxy_key ):
    global _verbose, t_data

    if _verbose:
        sys.stdout.write( '%s[+] whoxy key found, calling whoxy api targeting company%s\n' % (fg('green'),attr(0)) )

    for company in t_data['companies']:
        page = 1
        company = company.replace( ' ', '+' )
        if _verbose:
            sys.stdout.write( '%s[+] search for company: %s%s\n' % (fg('green'),company,attr(0)) )

        while True:
            url = 'http://api.whoxy.com/?key='+_whoxy_key+'&reverse=whois&company='+company+'&mode=micro&page='+str(page)
            page = page + 1
            if _verbose:
                sys.stdout.write( '%s[+] %s%s\n' % (fg('white'),url,attr(0)) )

            try:
                r = requests.get( url )
                t_json = r.json()
                # print(t_json)
            except Exception as e:
                sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
                continue

            if 'search_result' in t_json and len(t_json['search_result']):
                for result in t_json['search_result']:
                    if not result['domain_name'] in t_data['domains']:
                        t_data['domains'].append( result['domain_name'] )
                        print( result['domain_name'] )
            else:
                break


def searchEmailWhoxy( _whoxy_key ):
    global _verbose, t_data

    if _verbose:
        sys.stdout.write( '%s[+] whoxy key found, calling whoxy api targeting email%s\n' % (fg('green'),attr(0)) )

    for email in t_data['emails']:
        page = 1
        if _verbose:
            sys.stdout.write( '%s[+] search for email: %s%s\n' % (fg('green'),email,attr(0)) )

        while True:
            url = 'http://api.whoxy.com/?key='+_whoxy_key+'&reverse=whois&email='+email+'&mode=micro&page='+str(page)
            page = page + 1
            if _verbose:
                sys.stdout.write( '%s[+] %s%s\n' % (fg('white'),url,attr(0)) )

            try:
                r = requests.get( url )
                t_json = r.json()
                # print(t_json)
            except Exception as e:
                sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
                continue

            if 'search_result' in t_json and len(t_json['search_result']):
                for result in t_json['search_result']:
                    if not result['domain_name'] in t_data['domains']:
                        t_data['domains'].append( result['domain_name'] )
                        print( result['domain_name'] )
            else:
                break


def extractDatasWhoxy( t_json ):
    global _verbose, t_data

    for index in ['technical_contact','registrant_contact','administrative_contact']:
        if index in t_json:
            company,email = extractDataWhoxy( t_json, t_json[index] )
            if company and company not in t_data['companies']:
                t_data['companies'].append( company )
            if email and email not in t_data['emails']:
                t_data['emails'].append( email )

    return


def extractDataWhoxy( t_json, tab ):
    global _verbose, t_data

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

t_data = { 'domains':[], 'companies':[], 'emails':[] }

if args.verbose:
    _verbose = True
else:
    _verbose = False

if args.company:
    t_data['companies'].append( args.company )

if args.email:
    t_data['emails'].append( args.email )

if args.domain:
    _domain = args.domain
else:
    _domain = False

if not _domain and not len(t_data['companies']) and not len(t_data['emails']):
    parser.error( 'domain or company or email required' )

if args.key:
    _whoxy_key = args.key
else:
    _whoxy_key =  os.getenv('WHOXY_KEY')
    if not _whoxy_key:
        _whoxy_key = ""


if _domain:
    if _verbose:
        sys.stdout.write( '%s[+] search for domain: %s%s\n' % (fg('green'),_domain,attr(0)) )

    # sorry it's not relevant enough
    # searchDomainBuiltwith( _domain )

    if len(_whoxy_key):
        searchDomainWhoxy( _domain, _whoxy_key )


if len(_whoxy_key) and len(t_data['companies']):
    searchCompanyWhoxy( _whoxy_key )


if len(_whoxy_key) and len(t_data['emails']):
    searchEmailWhoxy( _whoxy_key )
