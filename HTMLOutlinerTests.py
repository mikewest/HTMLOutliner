#!/usr/bin/env python

import unittest
from HTMLOutliner import HTMLOutliner

class HTMLOutlinerTester( unittest.TestCase ):
    def assertOutline( self, input, expected ):
        result = HTMLOutliner( input ).render()
        self.assertEquals( result, expected )

class BasicTests( HTMLOutlinerTester ):
    def testBasecase( self ):
        self.assertOutline(
            "<strong>This is a string.</strong>",
            "<strong></strong>"
        )

if __name__ == '__main__':
    unittest.main()
