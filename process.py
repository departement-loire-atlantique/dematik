from dematik.dematik import Dematik
from os.path import isfile, join
import glob
import argparse

def generate(args):
    
    dk = Dematik('publik', args.debug)

    # Load field data
    field_data_files = glob.glob('./process/labels/*.yaml')
    for field_data_file in field_data_files:
        dk.load_field_data(field_data_file)

    # Generate
    definition_files = glob.glob('./process/definitions/' + args.pattern)
    for definition_file in definition_files:
        dk.generate(definition_file)

    # Unsed labels
    if not args.donotshowunused:
        dk.show_unused_labels()

if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument("--pattern", default='**/*.def')
  parser.add_argument("--debug", action='store_true')
  parser.add_argument("--donotshowunused", action='store_true')
  args = parser.parse_args()
 
  generate(args)