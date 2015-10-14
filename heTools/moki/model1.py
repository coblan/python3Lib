import csv
with open('d:/egg2.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')
    spamwriter.writerow(['a', '1', '1', '2', '中文'])
    spamwriter.writerow(['b', '3', '3', '6', '4'])
    spamwriter.writerow(['c', '7', '7', '10', '4'])
    spamwriter.writerow(['d', '11','11','11', '1'])
    spamwriter.writerow(['e', '12','12','14', '3'])
    