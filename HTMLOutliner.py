#!/usr/bin/env python
# encoding: utf-8

import os, sys, re
import getopt
from BeautifulSoup import *

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

class HTMLOutliner( object ):
    def __init__( self, html ):
        self.html       = html
        self.soup       = BeautifulSoup( html )
        self.outline    = '' 
        self.generate_outline()

    def generate_outline( self, show_attributes=True ):
        self.outline = self._outliner( self.soup, 0, show_attributes )[1:]

    def _outliner( self, node, level, show_attributes ):
        outline = ''
        indent  = "\n" + (' ' * level)
        for i in node.contents:
            if isinstance( i, Tag ):
                inner_outline = self._outliner( i, level + 1, show_attributes )
                if re.match( r'^\s*$', inner_outline ):
                    if self.soup.SELF_CLOSING_TAGS.has_key( i.name ):
                        tag = "%(indent)s<%(tag)s%(attrs)s>"
                    else:
                        tag = "%(indent)s<%(tag)s%(attrs)s></%(tag)s>"

                else:
                    tag = "%(indent)s<%(tag)s%(attrs)s>%(inner)s%(indent)s</%(tag)s>"
                
                attributes = ''
                if show_attributes:
                    for attr in i.attrs:
                        attributes += ' %s="%s"' % ( attr[0], attr[1] )

                outline += tag % {
                                    'attrs':    attributes,
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
        filename = argv[ 1 ]
        with open( filename, 'r' ) as f:
            data = f.read()
        print HTMLOutliner( data ).render()
        return 0
    except:
        raise Usage(msg)
        return 2

if __name__ == "__main__":
    sys.exit(main())
