import csv
import random

# creates a new csv with a random subsample

sample_size = 200
path = 'sample/'

files = ['uued_uudised', 'elu24', 'err', 'paevaleht', 'postimees', 'telegram'] # ohtuleht

for file in files:
    all_rows = []
    with open(path + file + '.csv', 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            all_rows.append(row)
    samples = random.sample(all_rows, sample_size)
    with open(path + file + '_samples.csv', 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        for sample in samples:
            csv_writer.writerow(sample)