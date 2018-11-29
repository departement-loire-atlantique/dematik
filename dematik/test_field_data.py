from field_data import FieldData
import unittest

class FieldDataTest(unittest.TestCase):
    def setUp(self):
        self.fd = FieldData()   
        self.fd.load("test/labels.yaml")

    def assert_label(self, field_data, label):
        self.assertEqual(field_data, {"label" : label})

    def test_accent(self):
        self.assert_label(self.fd.simple_accent, "&#233;coute")

    def test_esperluette(self):
        self.assert_label(self.fd.esperluette, u"ceci &#38; cela")

    def test_htmltag(self):
        self.assert_label(self.fd.htmltag, u"tag &#60;tr&#62; tag")

    def test_quotes(self):
        self.assert_label(self.fd.quotes, u"l'habitat l&#8217;habitat")

    def test_title_and_items(self):
        self.assertEqual(self.fd.title_and_items, 
             {
                 "label" : u"Civilit&#233;",
                 "items" : ["M", "Mme"]
             })
    
    def test_multilines(self):
        self.assert_label(self.fd.multilines, u"multi aper&#231;u line text")

    def retour_ligne(self):
        self.assert_label(self.fd.retour_ligne, 
            u"multi **gras** line text *italique*<br />saut de ligne")

    def test_ecriture_inclusive(self):
        self.assert_label(self.fd.ecriture_inclusive, u"participant&#183;e&#183;s")

    def test_not_defined(self):
        with self.assertRaises(ValueError) as context:
            self.fd.not_defined

        self.assertTrue("L'attribut not_defined est inconnu" in context.exception)

if __name__ == '__main__':
    unittest.main()