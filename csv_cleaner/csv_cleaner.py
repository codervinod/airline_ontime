import csv
from optparse import OptionParser
import os
import StringIO
import zipfile


class CsvCleaner(object):
  def __init__(self, in_path, out_path, col_list):
    self.in_path = os.path.abspath(in_path)
    self.out_path = os.path.abspath(out_path)
    self.col_list = col_list

  def run(self):
    for root, file in self.read_files_in_path():
      for root, file, csv_data in self.extract_csv_from_zip(root, file):
        self.filter_csv_columns(root, file, csv_data)

  def filter_csv_columns(self, root, file, csv_data):
    reader = csv.reader(csv_data)
    header = reader.next()
    col_index_list = []
    for col in self.col_list:
      if col not in header:
        return
      col_index_list.append(header.index(col))

    out_path = os.path.join(self.out_path, file.replace(".zip", ".csv"))
    with open(out_path, 'w') as csvfile:
      csv_writer = csv.writer(csvfile, delimiter='\t',
                              quotechar='|', quoting=csv.QUOTE_MINIMAL)

      for row in reader:
        filtered_row = []
        for col_id in col_index_list:
          filtered_row.append(row[col_id].strip())
        csv_writer.writerow(filtered_row)

  def read_files_in_path(self):
    for root, subdirs, files in os.walk(self.in_path):
      if not files:
        continue
      for file in files: yield root, file

  def extract_csv_from_zip(self, root, file):
    zip_file_path = os.path.abspath(os.path.join(root, file))
    if file.endswith(".zip"):
      input_zip = zipfile.ZipFile(zip_file_path)
      for name in input_zip.namelist():
        if name.endswith(".csv"):
          yield root, file, StringIO.StringIO(input_zip.read(name))


def main(options):
  csv_cleaner = CsvCleaner(
    in_path=options.in_path, out_path=options.out_path,
    col_list=[
      "Origin", "Dest", "AirlineID", "ArrDelayMinutes",
      "DayOfWeek", "UniqueCarrier", "DepDelayMinutes",
      "FlightDate", "CRSDepTime"])
  csv_cleaner.run()


if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-i", "--inpath", dest="in_path",
                    help="path to input data")
  parser.add_option("-o", "--outpath", dest="out_path",
                    help="path to output data")
  (options, args) = parser.parse_args()
  main(options)
