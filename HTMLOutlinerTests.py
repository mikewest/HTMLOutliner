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

if __name__ == '__main__':
    unittest.main()
