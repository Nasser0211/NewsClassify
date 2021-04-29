# newsClassify
# 预处理

## 文本选择

总共可用类共9类（其他类无文章）， 每类文章随机抽取150篇

共计9*150篇文章。

## 取词

通过TF-IDF算法，每篇文章选取35个关键词。

**选词规则：**

TF(t)=该词出现次数/文章词语总数

IDF(t)=log[(文档总数/（1+出现该词文档数）]；

取max(TF(t)*IDF(t))35

运用库：jieba.analyse

**词语过滤：**

去除关键词中禁用表中的词以及重复的词，最终获得关键词约15000

```python
#input:path
#output:content   
def keyword_cutting(path):
    content = []
    rbook = xlrd.open_workbook(path)
    jieba.analyse.set_stop_words('source/stop_words.txt')
    for i in range(0, len(rbook.sheets())):
        rsheet = rbook.sheet_by_index(i)
        for row in rsheet.get_rows():
            product_column = row[0]  # 品名所在的列
            product_value = product_column.value
            if product_value != 'content':
                tf_result = analyse.extract_tags(product_value, topK=50)
                tf_result = [w for w in tf_result if len(w) > 1
                             and not re.match('^[a-z|A-Z|0-9|.]*$', w)]
                content.append(tf_result)
return content
```

**词语相似值：**

基于哈工大同义词词林进行词语相似值计算

![image-20210429141338239](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20210429141338239.png)



# 特征工程

**特征矩阵构建：**

matrix[i]=type.num

matrix[j]=keyword.value

![img](file:///C:\Users\lenovo\Documents\Tencent Files\794252610\Image\C2C\EC71540BA3BC04617FBC80659C87B220.png)



# 分类算法

## 基于朴素贝叶斯

先验概率：p(A)=[该类型文章总数+1]/文章总数

条件概率：p(B)*=该词在该类出现的文章数/该类所有的文章数

**计算概率：**

## 分类器

# 测试结果

测试选择：每类文章30篇共270篇



# 不足之处以及设想改进

**1.特征矩阵数据量不够全面，特征矩阵特征值没有聚合**

设想改进：

  (1)增加文章数选择，每类文章随机抽取增至600篇，每篇文章选取关键词30

  (2)进行特征值聚合

```python
content=['比赛','竞赛','战争','战役','增长','上升']
dict=content_resolve(content)
#output:[['比赛','竞赛'],['战争','战役'],['增长','上升']]
list1=['比赛','竞赛']
list2=...
...
matrix[j]=list.value
```

**2.f1_score低，计算概率公式存在问题，需进一步调参**

设想改进：

 对计算概率公式进行调参

引入文章标题特征矩阵，更新计算概率

**3.无法进行其他类判断，需进一步改进**

需要分析计算概率，概率值低于一个值，那么判断该文章为其他类
