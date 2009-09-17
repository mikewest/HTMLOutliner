#!/usr/bin/env python
# encoding: utf-8

import os, sys, re
from optparse import OptionParser
from BeautifulSoup import *

class HTMLOutliner( object ):
    def __init__( self, html, show_attributes=False, indent=' ' ):
        self.html       = html
        self.soup       = BeautifulSoup( html )
        self.outline    = '' 
        self.indent     = indent
        self._generate_outline( show_attributes )

    def _generate_outline( self, show_attributes ):
        self.outline = self._outliner( self.soup, 0, show_attributes )

    def _outliner( self, node, level, show_attributes ):
        outline = ''
        indent  = "\n" + ( self.indent * level )
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

    parser=OptionParser(usage="Usage: %prog [options] filename", version="%prog 0.5")
    parser.add_option(  "-a", "--attributes", 
                        action="store_true", dest="show_attributes", default=False,
                        help="Display element attributes in the generated outline" )

    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.error("Please provide a filename to outline.")
    elif len(args) > 1:
        parser.error("Only one filename is accepted.  Please try again with a single file.")

    filename = args[ 0 ]

    try:
        with open( filename, 'r' ) as f:
            data = f.read()
        print HTMLOutliner( data, options.show_attributes ).render()
        return 0
    except IOError as (errno, strerror):
        parser.error("Could not open %s\nIOError #%s: %s" % ( filename, errno, strerror ) )

if __name__ == "__main__":
    sys.exit(main())
