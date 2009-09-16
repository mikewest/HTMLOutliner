#!/usr/bin/env python
# encoding: utf-8

import os, sys
import getopt
from BeautifulSoup import *

help_message = '''
HTMLOutliner outlines HTML.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

class HTMLOutliner( object ):
    def __init__( self, html ):
        self.html = html
        self.soup = BeautifulSoup( html )
        self.generate_outline()

    def generate_outline( self ):
        print self.soup.prettify()

    def render( self ):
        return self.soup.prettify()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "outline="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
   
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
