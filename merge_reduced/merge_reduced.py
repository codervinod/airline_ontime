import csv
import operator
from optparse import OptionParser
import os
import StringIO
import zipfile


class MergeReduced(object):
  def __init__(self, in_path):
    self.in_path = os.path.abspath(in_path)
    self.data = dict()

  def run(self):
    for root, file in self.read_files_in_path():
      for key, val in self.read_file(root, file):
        self.data[key] = val

    self.output_data()

  def read_files_in_path(self):
    for root, subdirs, files in os.walk(self.in_path):
      if not files:
        continue
      for file in files:
        if file.startswith("part"):
          yield root, file

  def read_file(self, root, file):
    file_path = os.path.abspath(os.path.join(root, file))
    with open(file_path, "r") as fp:
      line = fp.readline()
      while line:
        print line
        line_ar = line.split("\t")
        line = fp.readline()
        if len(line_ar) >= 2:
          yield line_ar[0], int(line_ar[1].split("\n")[0])
        else:
          yield None, None

  def output_data(self):
    self.data = sorted(self.data.items(), key=operator.itemgetter(1),
                       reverse=True)
    print self.data


def main(options):
  merge_reduced = MergeReduced(
    in_path=options.in_path)
  merge_reduced.run()


if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-i", "--inpath", dest="in_path",
                    help="path to input data")

  (options, args) = parser.parse_args()
  main(options)
