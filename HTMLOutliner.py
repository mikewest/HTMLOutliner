#!/usr/bin/env python
# encoding: utf-8

import os, sys, re
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
        self.html       = html
        self.soup       = BeautifulSoup( html )
        self.outline    = '' 
        self.generate_outline()

    def generate_outline( self ):
        self.outline = self._outliner( self.soup, 0 )[1:]

    def _outliner( self, node, level ):
        outline = ''
        indent  = "\n" + (' ' * level)
        for i in node.contents:
            if isinstance( i, Tag ):
                inner_outline = self._outliner( i, level + 1 )
                if re.match( r'^\s*$', inner_outline ):
                    tag = "%(indent)s<%(tag)s></%(tag)s>"
                else:
                    tag = "%(indent)s<%(tag)s>%(inner)s%(indent)s</%(tag)s>"
                    
                outline += tag % {
                                    'tag':      i.name,
                                    'inner':    inner_outline,
                                    'indent':   indent
                                 }

        return outline
                
            
    def render( self ):
        return self.outline

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
