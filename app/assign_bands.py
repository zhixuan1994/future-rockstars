import json

db = open('./data/members.json','r')
band_db = open('./data/bands.json','w')

db_manage = json.loads(db.read())

#The max number of bands
band_amount = len(db_manage)/6
band_amount = int(band_amount)

#initialize the data
band_list = []
singer_list = []
guitar_list = []
drummer_list = []
bassist_list = []
keyboardist_list = []
instrument_list = []

#grade the gender, male=0, female=1
def male_female_grade(type_list):
    total=[]
    for i in range(len(type_list)):
        if type_list[i].get('gender') == 'male':
            total.append(0)
        elif type_list[i].get('gender') == 'female':
            total.append(1)
    return total

#judge whether the female or male is free to choose. free=2, If not free,male=0,female=1. If no data = -1
def male_female_judge(type_list):
    j = 0
    for i in type_list:
        j=j+i
    if len(type_list) == 0:
        judge_result=-1
    elif j == len(type_list):
        judge_result=1
    elif j == 0:
        judge_result=0
    elif j < len(type_list):
        judge_result =2
    return judge_result

#choose male
def male_choose(type_list):
    for i in range(len(type_list)):
        if type_list[i].get('gender') == 'male':
            break
    return type_list[i]['member_info']

#choose female
def female_choose(type_list):
    for i in range(len(type_list)):
        if type_list[i].get('gender') == 'female':
            break
    return type_list[i]['member_info']

#remove the member which already been choosen
def member_remove(member,type_list):
    for i in range(len(type_list)):
        if type_list[i].get('member_info') == member:
            del type_list[i]
            break

for i in range(len(db_manage)):
    id_name = str(db_manage[i].get('memberId'))+db_manage[i].get('gender')
    temp = {'gender':db_manage[i].get('gender'),'member_info': id_name +" "+
            db_manage[i].get('firstName') +" " +db_manage[i].get('lastName')}
    if db_manage[i].get('talent') == 'Singer':
        singer_list.append(temp)
    elif db_manage[i].get('talent') == 'Guitarist':
        guitar_list.append(temp)
    elif db_manage[i].get('talent') == 'Drummer':
        drummer_list.append(temp)
    elif db_manage[i].get('talent') == 'Bassist':
        bassist_list.append(temp)    
    elif db_manage[i].get('talent') == 'Keybordist':
        keyboardist_list.append(temp)
    elif db_manage[i].get('talent') == 'Instrumentalist':
        instrument_list.append(temp)

all_member =[singer_list, guitar_list,drummer_list,bassist_list,keyboardist_list,instrument_list]
key = ['singer','guitarist','drummer','bassist','keyboardist','instrumentalist']

for i in range(band_amount):    
    m = str(i)
    balance_number = 6
    band_name = "band "+ m
    band_list.append({"name":band_name,"type":"band"})
    judge_list =[]
    
    #find the balance_number and best_number
    for n in all_member:
        temp_list = male_female_grade(n)
        temp_number = male_female_judge(temp_list)
        if temp_number == -1:
            balance_number-=1
        if temp_number == 1:
            balance_number-=2
        judge_list.append(temp_number)   
    print(judge_list)
    if balance_number < 1:
        balance_number = 0
    best_number = int(balance_number/2)
    print(best_number)
    
    #input the bands_list
    for j in range(len(judge_list)):
        if judge_list[j]==2:
            if best_number <1:
                male_result = male_choose(all_member[j])
                band_list[i][key[j]] = male_result
                member_remove(male_result,all_member[j])
            else:
                female_result = female_choose(all_member[j])
                band_list[i][key[j]] = female_result
                member_remove(female_result,all_member[j]) 
                best_number-=1
        if judge_list[j]==0:
            male_result = male_choose(all_member[j])
            band_list[i][key[j]] = male_result
            member_remove(male_result,all_member[j])
        if judge_list[j]==1:
            female_result = female_choose(all_member[j])
            band_list[i][key[j]] = female_result
            member_remove(female_result,all_member[j]) 
        if judge_list[j]==-1:
            band_list[i][key[j]]="null"
    print(band_list)


band_list = json.dumps(band_list)
band_db.write(band_list)   
band_db.close()
db.close()
