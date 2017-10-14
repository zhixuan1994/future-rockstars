import json
import math

db=open('./data/members.json','r')
dorm_db=open('./data/dorms.json','w')
db_manage=json.loads(db.read())

boy_oldCampers=[]
boy_middleCampers=[]
boy_youngCampers=[]
girl_oldCampers=[]
girl_middleCampers=[]
girl_youngCampers=[]
boy_dorm =[]
girl_dorm =[]
total_dorm=[]

#separate the members into different age
def age_judge(age_range,target):
    min_age=age_range[0]
    max_age=age_range[1]
    temp_judge = int(target.get('age'))
    temp_member = str(target.get('memberId')) +str(target.get('age'))+' '+ target.get('firstName')+' '+ target.get('lastName')
    if temp_judge >= min_age and temp_judge <= max_age:
        return temp_member
    else:
        return 0

age_case=[[13,14],[15,16],[17,18]]
boy_list=[boy_youngCampers,boy_middleCampers,boy_oldCampers]
girl_list=[girl_youngCampers,girl_middleCampers,girl_oldCampers]

#separate members into different gender
for i in range(len(db_manage)):
    if db_manage[i].get('gender') == 'male':
        for j in range(len(age_case)):
            temp = age_judge(age_case[j],db_manage[i])
            if temp !=0:
                boy_list[j].append(temp)
    if db_manage[i].get('gender') == 'female':
        for j in range(len(age_case)):
            temp = age_judge(age_case[j],db_manage[i])
            if temp !=0:
                girl_list[j].append(temp)          
                
#separate boys into their own dorm_member
member_loop = math.ceil(len(boy_list[0])/3) + math.ceil(len(boy_list[2])/3)
member_list=[[],[],[]]
if member_loop < 8:
    extra_loop =0  
else:
    extra_loop = member_loop-8
    member_loop =8
for loop in range(member_loop):
    i = divmod(loop,3)[1]
    print(loop)
    if i == 1:
        i=2
    elif i == 2:
        i=0
    for j in range(3):
        if len(boy_list[i]) != 0:
            member_list[j].append(boy_list[i][0])
            del boy_list[i][0]
        elif len(boy_list[1]) != 0:
            member_list[j].append(boy_list[1][0])
            del boy_list[1][0]
        else:
            break  
    print(member_list)  
for loop in range(extra_loop):
    extra_list=[]
    for i in range(3):
        if len(boy_list[i]) !=0:
            extra_list.append(boy_list[i])
    j=0
    while j < 3:
        if len(member_list[j]) <8:
            member_list[j].append(extra_list[0])
            del extra_list[0]
        j+=1       
member_small = math.ceil(len(boy_list[1])/3)
for loop in range(member_small):
    for j in range(3):
        if len(boy_list[1]) == 0:
            break
        elif len(member_list[j]) < 8:
            member_list[j].append(boy_list[1][0])
            del boy_list[1][0]

#separate girls into their own dorm_member
member_loop = math.ceil(len(girl_list[0])/3) + math.ceil(len(girl_list[2])/3)
member_listG=[[],[],[]]
if member_loop < 8:
    extra_loop =0  
else:
    extra_loop = member_loop-8
    member_loop =8
for loop in range(member_loop):
    i = divmod(loop,3)[1]
    if i == 1:
        i=2
    elif i == 2:
        i=0
    for j in range(3):
        if len(girl_list[i]) != 0:
            member_listG[j].append(girl_list[i][0])
            del girl_list[i][0]
        elif len(girl_list[1]) != 0:
            member_listG[j].append(girl_list[1][0])
            del girl_list[1][0]
        else:
            break
for loop in range(extra_loop):
    extra_list=[]
    for i in range(3):
        if len(girl_list[i]) !=0:
            extra_list.append(girl_list[i])
    j=0
    while j < 3:
        if len(member_listG[j]) <8:
            member_listG[j].append(extra_list[0])
            del extra_list[0]
        j+=1
member_small = math.ceil(len(girl_list[1])/3)
for loop in range(member_small):
    for j in range(3):
        if len(girl_list[1]) == 0:
            break
        elif len(member_listG[j]) < 8:
            member_listG[j].append(girl_list[1][0])
            del girl_list[1][0]

#import each member into their dorm            
for i in range(3):
    dorm_name ="boy-dorm" +" "+ str(i)
    boy_dorm.append({'name':dorm_name,'type':'dorm','gender':'Male','members':member_list[i]})
    
for i in range(3):
    dorm_name ="girl-dorm" +" "+ str(i)
    girl_dorm.append({'name':dorm_name,'type':'dorm','gender':'Female','members':member_listG[i]})   
    
total_dorm = boy_dorm + girl_dorm
total_dorm = json.dumps(total_dorm)
dorm_db.write(total_dorm)
dorm_db.close()
db.close()
