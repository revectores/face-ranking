import os

PATH = 'training_records_folder/'
EXT_NAME = '.bmp'

i = 0
records = []
for file_name in os.listdir(PATH):
    records.append({})
    records_file = open(PATH + file_name)
    while True:
        record = records_file.readline()
        if not record:
            break
        record = record.split(';')
        if record[0][-len(EXT_NAME):] not in EXT_NAME:
            continue
        img_name, img_rank = record[0].rstrip(EXT_NAME), int(record[1].strip('\n'))
        records[i][img_name] = img_rank
    i += 1

records_num = len(records)
averages = [sum(record.values())/records_num for record in records]
proportions = [sum(averages)/average for average in averages]
weights = [proportion/sum(proportions) for proportion in proportions]

record_file = open("average_ranking.txt", 'w')
for img_name in sorted(records[0].keys()):
    rank = sum([records[i][img_name] * weights[i] for i in range(records_num)])
    average_record = "{img_name};{rank}\n".format(img_name=img_name, rank=rank)
    record_file.write(average_record)
record_file.close()
