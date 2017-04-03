import csv
from optparse import OptionParser
import os
import StringIO
import zipfile


class CsvCleaner(object):
  def __init__(self, path, col_list):
    self.path = os.path.abspath(path)
    self.col_list = col_list

  def run(self):
    for file in self.read_files_in_path():
      for file, csv_data in self.extract_csv_from_zip(file):
        self.filter_csv_columns(file, csv_data)

  def filter_csv_columns(self, file, csv_data):
    reader = csv.reader(csv_data)
    header = reader.next()
    col_index_list = []
    for col in self.col_list:
      if col not in header:
        return
      col_index_list.append(header.index(col))

    for row in reader:
      filtered_row = []
      for col_id in col_index_list:
        filtered_row.append(row[col_id])
      print "\t".join(filtered_row)

  def read_files_in_path(self):
    for root, subdirs, files in os.walk(self.path):
      if not files:
        continue
      for file in files: yield os.path.abspath(os.path.join(root, file))

  def extract_csv_from_zip(self, file):
    if file.endswith(".zip"):
      input_zip = zipfile.ZipFile(file)
      for name in input_zip.namelist():
        if name.endswith(".csv"):
          yield file, StringIO.StringIO(input_zip.read(name))


def main(options):
  csv_cleaner = CsvCleaner(path=options.path, col_list=["Origin", "Dest"])
  csv_cleaner.run()


if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-p", "--path", dest="path",
                    help="path to input data")
  (options, args) = parser.parse_args()
  main(options)
