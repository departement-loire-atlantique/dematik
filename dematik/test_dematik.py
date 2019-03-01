from .dematik import Dematik
import os
import unittest

class DematikTest(unittest.TestCase):

    def test_metadata(self):
        dk = Dematik('publik', True)
        form = dk.render_form(os.path.join(os.path.dirname(os.path.realpath(__file__)), "test", "simpleform.def"))
        self.assertIn('<workflow>accentu&#233;</workflow>', form)
        self.assertIn('<option varname="test">13 &#233;lastiques</option>', form)

if __name__ == '__main__':
    unittest.main()