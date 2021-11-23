import random

list_name = []
f_i = open("data_list.log", 'r')
for line in f_i:
    list_name.append(line.split()[0])
f_i.close()

list_new_name = list(range(len(list_name)))
random.shuffle(list_new_name)

f_o = open("change_name.sh", 'w')
for idx, ele in enumerate(list_name):
    f_o.write("mv Art_dataset/" + ele + ' Art_dataset/tmp_' + str(list_new_name[idx]) + ".jpg\n")
for idx in range(len(list_name)):
    f_o.write("mv Art_dataset/tmp_"  + str(idx) + '.jpg Art_dataset/' + str(idx) + ".jpg\n")
f_o.close()
