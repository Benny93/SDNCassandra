
# from https://stackoverflow.com/questions/5909873/how-can-i-pretty-print-ascii-tables-with-python
def pprinttable(rows):
  """
  Author: MattH
    Here's a quick and dirty little function I
    wrote for displaying the results from SQL
    queries I can only make over a SOAP API.
    It expects an input of a sequence of one or
    more namedtuples as table rows. If there's
    only one record, it prints it out differently.
  :param rows: Rows of the table
  :return: Formatted table
  """
  if len(rows) > 1:
    headers = rows[0]._fields
    lens = []
    for i in range(len(rows[0])):
      lens.append(len(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x)))))
    formats = []
    hformats = []
    for i in range(len(rows[0])):
      if isinstance(rows[0][i], int):
        formats.append("%%%dd" % lens[i])
      else:
        formats.append("%%-%ds" % lens[i])
      hformats.append("%%-%ds" % lens[i])
    pattern = " | ".join(formats)
    hpattern = " | ".join(hformats)
    separator = "-+-".join(['-' * n for n in lens])
    print hpattern % tuple(headers)
    print separator
    _u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, str) else t
    for line in rows:
        print pattern % tuple(_u(t) for t in line)
  elif len(rows) == 1:
    row = rows[0]
    hwidth = len(max(row._fields,key=lambda x: len(x)))
    for i in range(len(row)):
      print "%*s = %s" % (hwidth,row._fields[i],row[i])