Notice: Our use of Shlorp to generate multi-author, data-driven reports is now superseded by [Ckan-o-Sweave](https://bitbucket.org/dpaw/ckan-o-sweave), a template Sweave project integrating content from a CKAN data catalogue (figures, captions, text) and the project itself.

![shlorp](http://i.imgur.com/ujwCg.jpg) 

[Picture credits](http://www.reddit.com/user/tehjeff)

Shlorp is a webscraper pipelining wget, beautifulsoup, pandoc, and latex 
to generate PDF from Confluence Wiki pages. It was designed against very specific 
page structures and content, and will require some customisation to scrape and layout other targets.

## Purpose
Shlorp scrapes and layouts some very specifically set up reports we author collaboratively on an Atlassian Confluence wiki.
Some metadata that ends up in PDF metadata, as title and so on, is located under very specific headings.
Content comes from a variety of sources, even copy/pasted MS Word in Windows-encodings may be found.

## What you get out of Shlorp
If you find yourself stuck in an annual collaborative editing / email-Ms Word-versionitis / layouting nightmare, Shlorp might be for you - but
we offer no warranties, use at own risk!
Modifying Shlorp to scrape different content will require some knowledge of Python, HTML/DOM, and LaTeX, but the code should be readable
and documented enough to be adaptable without having to reinvent the wheel once again.

# Build status
[![wercker status](https://app.wercker.com/status/2538dd1dac1944d7a528642b3266c3b9/m/ "wercker status")](https://app.wercker.com/project/bykey/2538dd1dac1944d7a528642b3266c3b9)

# Get SHLORPed
Shlorp uses fabric as make tool.
```
sudo apt-get install fabric
fab setup
# modify shlorp.settings to your needs
fab run
```

Run `fab -l` to see other make targets at hand.

Run `fab makedoc` to generate the developer docs at [docs/build/html/index.html](docs/build/html/index.html)

# Workflow

* In a Ubuntu environment, fabric is installed.
* Optionally, a virtualenv is created with virtualenvwrapper and activated
* Fabric is installed
* A set of URLs, a username and a password are given in shlorp/settings.py (copied from shlorp/settings.template).
* HTML pages are downloaded from the given URLs (login requires un and pw)
* attached files are sanitized and re-linked in the HTML files
* HTML is parsed and transformed according to specific rules

The Confluence web pages are assumed to be of a somewhat defined structure. 
This script removes some elements, uses others to set variables to feed the pandoc latex template, and transforms the rest
into clean HTML, which in turn will arrive more or less correctly in the pandoc-generated latex.

* Modified HTML is translated into LaTeX using a custom LaTeX template, using variables extracted from
each HTML file. 
* The LaTeX file is further modified and re-saved, pending 
* compliation by XeLaTeX and 
* compression through GhostScript.


# Resources

* [Confluence auth](https://confluence.atlassian.com/display/BAMKB/Automating+Bamboo+operations+using+wget+or+Curl)
* [HTML download](http://www.linuxjournal.com/content/downloading-entire-web-site-wget)
* [HTML parsing](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* HTML parsing using HTMLtidy, BeautifulSoup
* HTML to LaTeX conversion using [Pandoc](http://johnmacfarlane.net/pandoc/) and wrapper pypandoc
* [regex replacements](http://xahlee.blogspot.com.au/2012/04/idiomatic-findreplace-script-in-python.html)

# Authors and Copyright
Copyright (C) 2012-2013 Department of Parks and Wildlife

* [Florian Mayer](Florian.Mayer@dpaw.wa.gov.au)

# License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
