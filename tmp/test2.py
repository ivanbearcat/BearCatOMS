import re
from BearCatOMS.settings import BASE_DIR
sidebar_list = []
sidebar_list2 = []
with open(BASE_DIR + '/templates/public/sidebar.html') as f:
    line = f.readline()
    while line:
        data = re.search(r'[\u2E80-\uFE4F]+',line)
        if data:
            sidebar_list.append(data.group().replace('/',''))
        line = f.readline()
for i in sidebar_list:
    if  i != 'main' or i != 'user_perm':
        sidebar_list2.append(i)
print sidebar_list2