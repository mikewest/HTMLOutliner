#!/usr/bin/env python

import unittest
from HTMLOutliner import HTMLOutliner

class HTMLOutlinerTester( unittest.TestCase ):
    def assertOutline( self, input, expected ):
        result      = HTMLOutliner( input ).render()
        self.assertEquals( result.strip(), expected.strip() )

class BasicTests( HTMLOutlinerTester ):
    def testBasecase( self ):
        self.assertOutline(
            "<strong>This is a string.</strong>",
            "<strong></strong>"
        )

    def testOneLevel( self ):
        self.assertOutline(
            "<em><strong>This is a string.</strong></em>",
            """
<em>
 <strong></strong>
</em>
            """
        )

    def testTwoLevels( self ):
        self.assertOutline(
            "<p><em><strong>This is a string.</strong></em></p>",
            """
<p>
 <em>
  <strong></strong>
 </em>
</p>
            """
        )

    def testSelfClosing( self ):
        self.assertOutline(
            '<p><img></p>',
            """
<p>
 <img>
</p>
            """
        )

class AttributeTests( HTMLOutlinerTester ):
    def testSingle( self ):
        self.assertOutline(
            """<strong class="classname">This is a string.</strong>""",
            """<strong class="classname"></strong>"""
        )
        self.assertOutline(
            """<strong class='classname'>This is a string.</strong>""",
            """<strong class="classname"></strong>"""
        )

    def testMultiple( self ):
        self.assertOutline(
            """<strong id='elID' class='classname'>This is a string.</strong>""",
            """<strong id="elID" class="classname"></strong>"""
        )

if __name__ == '__main__':
    unittest.main()
