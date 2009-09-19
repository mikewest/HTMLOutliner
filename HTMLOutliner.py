#!/usr/bin/env python
# encoding: utf-8

import os, sys, re
from optparse import OptionParser
from BeautifulSoup import *

class HTMLOutliner( object ):
    def __init__( self, html, show_attributes=False, show_comments=False, indent=' ' ):
        self.html       = html
        self.soup       = BeautifulSoup( html )
        self.outline    = '' 
        self.indent     = indent
        self.attributes = show_attributes
        self.comments   = show_comments
        self._generate_outline()

    def _generate_outline( self ):
        self.outline = self._outliner( self.soup, 0 )

    def _outliner( self, node, level ):
        outline = ''
        indent  = "\n" + ( self.indent * level )
        for i in node.contents:
            if self.comments and isinstance( i, Comment ):
                # Deal with "HTMLDoc" comments: only display the first
                # line of actual text, without the `- ` mess.
                comment = str( i ).strip().split("\n")[0]
                comment = re.sub( r'^-\s+', '', comment )
                outline += '%(indent)s<!-- %(comment)s -->' % {
                                                                'indent':  indent,
                                                                'comment': comment
                                                            }
            elif isinstance( i, Tag ):
                inner_outline = self._outliner( i, level + 1 )
                if re.match( r'^\s*$', inner_outline ):
                    if self.soup.SELF_CLOSING_TAGS.has_key( i.name ):
                        tag = "%(indent)s<%(tag)s%(attrs)s>"
                    else:
                        tag = "%(indent)s<%(tag)s%(attrs)s></%(tag)s>"
                else:
                    tag = "%(indent)s<%(tag)s%(attrs)s>%(inner)s%(indent)s</%(tag)s>"
                
                attributes = ''
                if self.attributes:
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
    parser.add_option(  "-c", "--comments", 
                        action="store_true", dest="show_comments", default=False,
                        help="Display comments in the generated outline (only the first line of a multi-line comment will be displayed)" )
    parser.add_option(  "-i", "--indent",
                        action="store", dest="indent", default=" ",
                        help="Define the indentation for each line of the document (defaults to a single space)" )
    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.error("Please provide a filename to outline.")
    elif len(args) > 1:
        parser.error("Only one filename is accepted.  Please try again with a single file.")

    filename = args[ 0 ]

    try:
        with open( filename, 'r' ) as f:
            data = f.read()
        print HTMLOutliner( data,
                            show_attributes=options.show_attributes,
                            show_comments=options.show_comments,
                            indent=options.indent ).render()
        return 0
    except IOError as (errno, strerror):
        parser.error("Could not open %s\nIOError #%s: %s" % ( filename, errno, strerror ) )

if __name__ == "__main__":
    sys.exit(main())
