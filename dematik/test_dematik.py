from .dematik import Dematik
import os
import unittest

class DematikTest(unittest.TestCase):

    def test_metadata(self):
        dk = Dematik('publik', True)
        dk.load_field_data(os.path.join(os.path.dirname(os.path.realpath(__file__)), "test", "labels.yaml"))
        form = dk.render_form(os.path.join(os.path.dirname(os.path.realpath(__file__)), "test", "simpleform.def"))
        self.assertIn('<workflow>accentu&#233;</workflow>', form)
        self.assertIn('<option varname="test">13 &#233;lastiques</option>', form)
        self.assertIn('<option varname="toto">18 &#233;lastiques</option>', form)

        # Datasource
        self.assertIn('<data_source><type>formula</type><value>[\'&#233;l&#233;ment 1\', \'&#233;l&#233;ment 2\', \'&#233;l&#233;ment 3\']</value></data_source>', form)
        self.assertIn('<data_source><type>json</type><value>{{passerelle_url}}csvdatasource/dispatch-communes/data</value></data_source>', form)
        self.assertIn('<data_source><type>jsonp</type><value>{{passerelle_url}}csvdatasource/dispatch-communes/data</value></data_source>', form)
        self.assertIn('<data_source><type>communes_datasource_id</type></data_source>', form)

        self.assertIn('<data_source><type>json</type><value>URL json</value></data_source>', form)
        self.assertIn('<data_source><type>jsonp</type><value>URL jsonp</value></data_source>', form)
        self.assertIn('<data_source><type>Communes</type></data_source>', form)

if __name__ == '__main__':
    unittest.main()