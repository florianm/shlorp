from __future__ import unicode_literals
import os, sys, re, subprocess, time, codecs


import splinter


#from unidecode import unidecode
# import pypandoc
from bs4 import BeautifulSoup, UnicodeDammit
from tidylib import tidy_document
from datetime import datetime

def get_html_old(urls=[], timeout_in_seconds=500):
    """Download confluence pages with attachments and authentication.

    HTML web pages will be downloaded as follows:

    * the complete page with all linked assets will be downloaded (-p, --page-requisites)
    * all files will be downloaded inside /source (hard-coded here and in fab setup)
    * domain and path will be converted to folders
    * embedded links will be converted to relative links to locally saved assets (-k, --convert-links)
    * assets will be downloaded even from cross-domain hosts (-H, --span-hosts)
    * all pages will be saved with .html extension (-E, --html-extension)
    * the assets in /s are excluded because they are unneccessary (-X /s)

    Authentication is handled as Basic with HTTP username and password for each request.
    This requires the following settings variables to be imported:
    
    * USERNAME
    * PASSWORD

    :param urls: A list of [url, filename] to download
    :param timeout_in_seconds: the network timeout in seconds
    """
    print("[DOWNLOAD] Donwloading...")

    for url in urls:
        cmd = ("wget --http-user {0} --http-password {1} -P source/ " +\
                "-E -H -k -p -X /s -T {2} '{3}?os_authType=basic'").format(
                USERNAME, PASSWORD, timeout_in_seconds, url[0])
        #print(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

    print("[DOWNLOAD] Success!")
