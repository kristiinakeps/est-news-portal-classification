import csv
import random

# creates a new csv with a random subsample

sample_size = 10000

path = 'sample/'

files = ['uued_uudised', 'elu24', 'err', 'paevaleht', 'postimees', 'telegram'] # ohtuleht
delimiters = [',', ';', ',', ',', ';', ',']

for i in range(len(files)):
    file = files[i]
    delimiter = delimiters[i]
    all_rows = []
    with open(path + file + '.csv', 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=delimiter)
        header = next(csv_reader)
        for row in csv_reader:
            all_rows.append(row)
    if sample_size < len(all_rows):
        samples = random.sample(all_rows, sample_size)
    else:
        samples = all_rows
    with open(path + file + '_samples.csv', 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f, delimiter=delimiter)
        csv_writer.writerow(header)
        for sample in samples:
            csv_writer.writerow(sample)