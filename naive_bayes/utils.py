import xlrd


def get_score(list1,list2):
    if (len(list1) == len(list2)):
        same=0
        for i in range(0,len(list1)):
            l1=list1[i]
            l2=list2[i]
            if(l1==l2):
                same=same+1
    else:
        return 0
    return same/len(list1)

def get_essay_type(path):
    content = []
    rbook = xlrd.open_workbook(path)
    for i in range(0, len(rbook.sheets()) ):
        rsheet = rbook.sheet_by_index(i)
        for row in rsheet.get_rows():
            product_column = row[1]
            product_value = product_column.value
            if product_value != 'channelName':
                if product_value==str("财经"):
                    content.append(0)
                if product_value==str("房产"):
                    content.append(1)
                if(product_value==str('教育')):
                    content.append('2')
                if(product_value==str('科技')):
                    content.append(3)
                if(product_value==str('军事')):
                    content.append(4)
                if(product_value==str('汽车')):
                    content.append(5)
                if(product_value==str('体育')):
                    content.append(6)
                if(product_value==str('游戏')):
                    content.append(7)
                if(product_value==str('娱乐')):
                    content.append(8)
    return content


