import json
import random

db = open('./data/members.json', 'r')
band_db = open('./data/bands2.json', 'w')
db_manage = json.loads(db.read())

# The max number of bands
band_amount = int(len(db_manage) / 6)

# initialize the data
band_list, singer_list, guitar_list, drummer_list = [], [], [], []
bassist_list, keyboardist_list, instrument_list = [], [], []

# Average


def average(list):
    sum = 0
    length = 0
    for i in list:
        if i != 0:
            sum = sum + i
            length += 1
    if length != 0:
        return sum / length
    else:
        return 0


# variance


def variance(list, average):
    sum = 0
    length = 0
    for i in list:
        if i != 0:
            sum = sum + (i - average)**2
            length += 1
    if length != 0:
        return sum / length
    else:
        return 0

# band_assignment (age + talent rank)


def band_rank(member_list, first):
    talent_list = []
    age_list = []
    talentf_list = []
    temp = []
    talent_grade = 0
    for i in range(6):
        talent_list.append(0)
        age_list.append(0)
        num = first
        for j in range(len(member_list)):
            if i == 0:
                talent_list[i] = member_list[first][1]
                age_list[i] = member_list[first][2]
                break
            elif member_list[j][0] == i:
                num = j
                talent_list[i] = member_list[j][1]
                age_list[i] = member_list[j][2]
                ave_add = average(talent_list)
                var_add = variance(talent_list, ave_add)
                var_balance = abs(var_add - 1.25)
                if var_balance < 0.35:
                    age_ave = average(age_list)
                    age_var = variance(age_list, age_ave)
                    age_balance = abs(age_var - 3.125)
                    age_ave_bal = abs(age_ave - 3.5)
                    if len(talent_list) > 3:
                        if ave_add > 2.7:
                            talent_list[-1] = 0
                            age_list[-1] = 0
                        elif age_balance < 0.7 and age_ave_bal < 1:
                            break
                        else:
                            age_list[-1] = 0
                            talent_list[-1] = 0
                    elif age_var > 1.125:
                        break
                    else:
                        age_list[-1] = 0
                        talent_list[-1] = 0
                else:
                    talent_list[-1] = 0
                    age_list[-1] = 0
        if talent_list[i] ==0:
            num = 0
        talentf_list.append([i, talent_list[i], age_list[i], num])
    return talentf_list

# Judge wither the band is full


def band_full(band):
    grade = 0
    for i in range(6):
        if band[i][1] == 0:
            grade += 1
    return grade


# input data into each dataset type. Change this will change the input to achieve that each semester get the different result
for i in range(len(db_manage)):
    id_name = db_manage[i].get('memberId') + " || " + \
        str(db_manage[i].get('age'))
    temp = {'trank': db_manage[i].get('trank'), 'age': db_manage[i].get('age'),
            'member_info': id_name + " || " + db_manage[i].get('firstName') + " "
            + db_manage[i].get('lastName') + " || " + str(db_manage[i].get('trank'))}
    if db_manage[i].get('talent') == 'Singer':
        singer_list.append(temp)
    elif db_manage[i].get('talent') == 'Guitarist':
        guitar_list.append(temp)
    elif db_manage[i].get('talent') == 'Drummer':
        drummer_list.append(temp)
    elif db_manage[i].get('talent') == 'Bassist':
        bassist_list.append(temp)
    elif db_manage[i].get('talent') == 'Keyboardist':
        keyboardist_list.append(temp)
    elif db_manage[i].get('talent') == 'Instrumentalist':
        instrument_list.append(temp)

# list random input
random.shuffle(singer_list)
random.shuffle(guitar_list)
random.shuffle(drummer_list)
random.shuffle(bassist_list)
random.shuffle(keyboardist_list)
random.shuffle(instrument_list)

all_member = [singer_list, guitar_list, drummer_list,
              bassist_list, keyboardist_list, instrument_list]
key = ['singer', 'guitarist', 'drummer',
       'bassist', 'keyboardist', 'instrumentalist']
members_list = []
for i in range(6):
    for j in range(len(all_member[i])):
        temp_list = [i, all_member[i][j]['trank'],
                     all_member[i][j]['age'] - 12]
        members_list.append(temp_list)
singer_numf = len(all_member[0])
print(members_list)
all_member = singer_list+ guitar_list + drummer_list + bassist_list + keyboardist_list + instrument_list

# generate the result
for i in range(band_amount):
    singer_num =singer_numf- i
    m = str(i)
    balance_number = 6
    band_name = "band " + m
    band_list.append({"name": band_name, "type": "band"})
    band_temp = band_rank(members_list, 0)
    band_grade = band_full(band_temp)
    if band_grade == 0:
        band_finial = band_temp
    else:
        band_finial = band_temp
        for sti in range(singer_num - 1):
            band_temp = band_rank(members_list, sti + 1)
            grade_temp = band_full(band_temp)
            print(grade_temp)
            if grade_temp == 0:
                band_finial = band_temp
                break
            elif grade_temp < band_grade:
                band_finial = band_temp
                band_grade = grade_temp
    band_member = band_finial
    small = 0
    print(band_finial)
    for ss in range(6):
        tem = band_finial[ss][3]
        if tem == 0:
            band_list[i][key[ss]] = 'null'
        else: 
            tem = tem - small
            band_list[i][key[ss]] = all_member[tem]['member_info']
            del all_member[tem]
            del members_list[tem]
            small+=1
    if small == 0:
        del band_list[i]
        break
print('kkkkkk', band_list)

    # write the whole result into band_list, which will write into the json file after all done

# result input
band_list = json.dumps(band_list)
band_db.write(band_list)
band_db.close()
db.close()
