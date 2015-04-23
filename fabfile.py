"""Fabric buildscript for Shlorp.

Imports are wrapped in try-except blocks to handle different scenarios:

* running sphinx-autodoc will run imports, which fail on (but do not require) `fabric.api`
* running `fab setup` will provide dependencies, which will be imported in modules
* once dependencies are installed, the import of `shlorp.convert` will work
* confidential settings are in the .env file (not in repo)
* run this fab file with `honcho run fab COMMAND` to add variables defined in .env to os.environ


"""

import os, sys
try:
    from fabric.api import *
except:
    pass # for sphinx-doc

import splinter

#try:
#from shlorp import convert as c
#except:
#    print("MISSING DEPENDENCIES! Run `fab setup` to install dependencies.")

#-----------------------------------------------------------------------------#
# Setup and one-off operations

def setup_system():
    """Aux: Installs system dependencies.
    
    Uses apt-get to install wget, tidylib, latex, pandoc and firefox.
    """
    local("sudo apt-get install -y wget tidy texlive-latex-base inkscape "+\
            "texlive-latex-extra texlive-full texlive-xetex pandoc firefox")

def setup_python():
    """Aux: Installs python dependencies as per requirements.txt.
    
    Uses pip-install to install requirements into the active virtualenv.
    """
    local("pip install -r requirements.txt")

def setup_folders():
    """Aux: Creates project folders.
    
    Creates folders for:

    * downloaded web pages (source)
    * layouted products (build)
    * sphinx documentation (doc)
    * log files (log)
    """
    local("mkdir -p source; return 0")
    local("mkdir -p build; return 0")
    local("mkdir -p doc; return 0")
    local("mkdir -p log; return 0")

def setup():
    """Main: Sets up the whole build environment.

    Runs setup_system, setup_python, setup_folders.
    """
    setup_system()
    setup_python()
    setup_folders()

#-----------------------------------------------------------------------------#
def download():
    """Aux: Downloads source material.
    
    Uses shlorp.convert.get_html to download all files from shlorp.settings.SOURCES
    to source/ using shlorp.settings.{USERNAME and .PASSWORD} for authentication.
    """
    print("Downloading web pages...")
    _get_html()
    print("Done.")

def convert_images():
    """Aux: Convert all SVG images to PDF.

    Uses inkscape to export SVG to PDF:
    >>> inkscape -z -D --file="test.svg" --export-pdf="test.pdf" --export-latex
    """
    print("Converting images...")
    print("Done.")

def clean_html():
    """Aux: Parses and cleans downloaded HTML.
    
    Uses BeautifulSoup4 to parse and modify downloaded web pages.
    Removes parts of the DOM, extracts metadata from DOM, fixes some markup, e.g.
    image tags use the following paragraph as caption.
    """
    print("TODO bs4 HMTL")

def make_tex():
    """Aux: Translates HTML to LaTeX source files.
    
    Uses Pandoc to translate HTML to LaTeX.
    """
    print("TODO pandoc HTML")

def clean_tex():
    """Aux: Parses and cleans up LaTeX files.
    
    Uses black magic, regular expressions and other witchcraft to post-process LaTeX.
    Handles some format and layout issues which pandoc cannot translate correctly.
    """
    print("TODO parse and postprocess tex")

def make_pdf():
    """Aux: Compiles LaTeX to PDF.
    
    Uses PDFLatex to compile LaTeX to PDF.
    >>> pdflatex -interaction=nonstopmode -shell-escape 'test'
    """
    print("TODO xelatex to PDF")

def compress_pdf():
    """Aux: Compresses created PDF.
    
    Uses ghostscript to compress PDFs to print quality (300dpi).
    """
    print("TODO ghostscript compress PDF")


#-----------------------------------------------------------------------------#
def run():
    """Main: Part 1 and 2: scrapes web content and processes content into PDF"""
    download()
    chomp()
    print("\n\n\nSuccess, expected end!")

def chomp():
    """Main: Part 2 - processes previously downloaded content into PDF"""
    #convert_images() # latex package svg converts SVG to PDF, PDFLaTeX only
    clean_html()
    make_tex()
    clean_tex()
    make_pdf()
    compress_pdf()


#-----------------------------------------------------------------------------#
# Testing, documentation, admin
def test():
    """Main: Runs tests."""
    print("Testing PDFLaTeX (cheating: skipp skippity skip)")
    #local("cd demo && pdflatex -interaction=nonsttopmode -shell-escape test.tex")
    print("Done.")

def makedoc():
    """Main: Compiles documentation.
    
    Uses sphinx to auto-generate documentation from docstrings in python code.
    """
    local("cd doc && make html")

def readdoc():
    """Main: Open docs in Firefox. Because lazy.
    """
    local("firefox doc/build/html/index.html &")

# workhorse functions

def _get_authenticated_browser(un, pw, ls):
    """Provide an authenticated splinter.Browser
    """
    br = splinter.Browser()
    br.visit(ls)
    if br.title == 'Log In - Confluence':
        un = br.find_by_id('os_username')[0]
        print(repr(un))
        un.fill(un)
        pw = br.find_by_id('os_password')[0]
        pw.fill(pw)
        lb = br.find_by_id('loginButton')[0]
        lb.click()
        return br
    else:
        print("this is not the login screen")
        return None

def _get_html(un=settings.USERNAME, pw=settings.PASSWORD, 
        ls=settings.LOGONSERVER, sources=settings.SOURCES):
    """Download HTML pages

    Args: 
    :param un: The username, default: settings.USERNAME
    :param pw: The password, default: settings.PASSWORD
    :param ls: The logon server, default: settings.LOGONSERVER
    :param sources: a list of URLs as strings, default: settings.SOURCES
    """
    br = _get_authenticated_browser(os.environ["USERNAME"], 
            os.environ["PASSWORD"], os.environ["LOGONSERVER"])
    if not br:
        print("shlorp.convert.get_authenticated_browser() did not return a "
              "splinter.Browser object. Exiting.")
        return None
    for url in os.environ["SOURCES"]:
        br.visit(url)
        print(br.title)


# download HTML pages
