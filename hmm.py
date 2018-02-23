import math
import string
import  json
#print ('virali')

def nonrare(dictt):
    newDict = []
    for i in dictt:
        if dictt[i] > 3:
            newDict.append(i)
    return set(newDict)

def rare(dictt):
    newDict = []
    for i in dictt:
        if dictt[i] <= 3:
            newDict.append(i)
    return set(newDict)

def fileWrite(tag,word_tag,transitionProbabilities,words_list):
    op = open('hmmmodel.txt','w',encoding='utf8')
    dataa = json.loads("[{},{},{},{}]".format(json.dumps(tag), json.dumps(word_tag), json.dumps(transitionProbabilities), json.dumps(words_list)))
    op.write(json.dumps(dataa))


def deletedInterpolation(tag,tag_tag,tag_tag_tag, total_count):
    alpha = [0,0,0]
    for trigram in tag_tag_tag:
        delimeter = '@@'
        temp = trigram.split('@@')
        oneTwo = delimeter.join(temp[0:2])
        twoThree = delimeter.join(temp[1:3])
        if tag_tag[oneTwo][1] != 1:
            v1 = (tag_tag_tag[trigram][0] - 1) / (tag_tag[oneTwo][1] - 1)
        if tag[temp[1]][1] != 1:
            v2 = (tag_tag[twoThree][0] - 1) / (tag[temp[1]][1] - 1)
        v3 = (tag[temp[2]][0] - 1) / (total_count - 1)
        maximum = max(v1,v2,v3)
        if maximum == v1:
            alpha[0] += tag_tag_tag[trigram][0]
        if maximum == v2:
            alpha[1] += tag_tag_tag[trigram][0]
        if maximum == v3:
            alpha[2] += tag_tag_tag[trigram][0]

    total = alpha[0] + alpha[1] + alpha[2]
    maximum = max(alpha)
    minimum = min(alpha)
    alpha[0] = alpha[0] / total
    alpha[1] = alpha[1] / total
    alpha[2] = alpha[2] / total
    return alpha

def transitionProbability(tag, tag_tag):
    print(len(tag))
    for bigram in tag_tag:
        delimeter = '@@'
        V = len(tag)
        temp = bigram.split('@@')
        if tag[temp[0]][1] != 0:
            transitionProbabilities[temp[1]+'|'+temp[0]] = (tag_tag[bigram][0] + 1)/ (tag[temp[0]][1] + (V))

    tagkeys = tag.keys()
    for tag1 in tagkeys:
        for tag2 in tagkeys:
            str = tag1 + '|' + tag2
            if str not in transitionProbabilities:
                transitionProbabilities[str] = 1 / (tag[tag2][1] + (V))


def transitionProbabilitynnew(alpha, tag, tag_tag, tag_tag_tag, total_count):
    # print(tag)
    for trigram in tag_tag_tag:
        delimeter = '@@'
        temp = trigram.split('@@')
        oneTwo = delimeter.join(temp[0:2])
        twoThree = delimeter.join(temp[1:3])
        if tag_tag[oneTwo][1] != 0:
            v1 = (tag_tag_tag[trigram][0] + 1) / (tag_tag[oneTwo][1] + total_count * total_count)
        if tag[temp[1]][1] != 0:
            v2 = (tag_tag[twoThree][0] + 1) / (tag[temp[1]][1] + total_count)
        v3 = (tag[temp[2]][0] + 1) / ((total_count) + 1)
        total = alpha[0] * v1 + alpha[1] * v2 + alpha[2] * v3

        keeyy = temp[2] + '|' + oneTwo
        transitionProbabilities_new[keeyy] = total
    tagkeys = tag.keys()
    for tag1 in tagkeys:
        for tag2 in tagkeys:
            for tag3 in tagkeys:
                strr = tag1 + '|' + tag3 + '@@' + tag2
                str1 = tag3 + '@@' + tag2 + '@@' + tag1
                str2 = tag3 + '@@' + tag2
                str3 = tag2 + '@@' + tag1
                str4 = tag2
                str5 = tag3

                if str1 not in tag_tag_tag:
                    tag_tag_tag[str1] = [1,1]
                if str2 not in tag_tag:
                    tag_tag[str2] = [1,1]
                if str3 not in tag_tag:
                    tag_tag[str3] = [1,1]
                if str4 not in tag:
                    tag[str4] = [1,1]
                if str5 not in tag:
                    tag[str5] = [1,1]
                if strr not in transitionProbabilities_new:
                    v1 = (tag_tag_tag[str1][0] + 1) / (tag_tag[str2][1] + total_count * total_count)
                    v2 = (tag_tag[str3][0] + 1) / (tag[tag2][1] + total_count)
                    v3 = (tag[tag1][0] + 1) / ((total_count) + 1)

                total = alpha[0] * v1 + alpha[1] * v2 + alpha[2] * v3
                transitionProbabilities_new[strr] = total

data = open('input.txt',encoding="utf8")
#data = open('data.txt')
word_tag = {}
words_list = {}
tag = {}
tag_tag = {}
tag_tag_tag = {}
total_count = 0
emissionProbabilities = {}
transitionProbabilities = {}
transitionProbabilities_new = {}
tag['<s>'] = [0,0]
tag['</s>'] = [0,0]

for line in data:
    line = line.rstrip()
    line_list = line.split()
    for idx in (line_list):
        temp1 = idx.rsplit('/',1)
        if temp1[0] not in words_list:
            words_list[temp1[0]] = 1
        else:
            words_list[temp1[0]] += 1
#print(words_list)
rare_Words = rare(words_list)
nonrare_Words = nonrare(words_list)
data.close()
data = open('input.txt',encoding="utf8")
for line in data:
    line = line.rstrip()
    tag['<s>'][0] += 1
    tag['<s>'][1] += 1
    line_list = line.split()
    total_count += len(line_list)
    tag_list = ['<s>']
    length = len(line_list) - 1
    for idx in range(len(line_list)):
        '''temp1 = line_list[idx].rsplit('/',1)
        delimeter='/'
        if temp1[0] in rare_Words:
            temp1[0] = '_RARE_'
        line_list[idx] = delimeter.join(temp1)'''
        if line_list[idx] not in word_tag:
            word_tag[line_list[idx]] = 1
        else:
            word_tag[line_list[idx]] += 1
        temp1 = line_list[idx].rsplit('/',1)
        tag_list.append(temp1[1])
        '''if temp1[0] not in words_list:
            words_list[temp1[0]] = 1
        else:
            words_list[temp1[0]] += 1'''
        if idx < length:
            if temp1[1] not in tag:
                tag[temp1[1]] = [1,1]
            else:
                temp2 = tag[temp1[1]]
                temp2[0] += 1
                temp2[1] += 1
                tag[temp1[1]] = temp2
        else:
            if temp1[1] not in tag:
                tag[temp1[1]] = [1,0]
            else:
                temp2 = tag[temp1[1]]
                temp2[0] += 1
                temp2[1] += 0
                tag[temp1[1]] = temp2


    tag_list.append('</s>')
    length = len(tag_list) - 3
    for idx in range(len(tag_list) - 1):
        if idx < length:
            st = '@@'
            str = st.join(tag_list[idx:idx + 2])
            if str not in tag_tag:
                tag_tag[str] = [1,1]
            else:
                temp2 = tag_tag[str]
                temp2[0] += 1
                temp2[1] += 1
                tag_tag[str] = temp2
        else:
            st = '@@'
            str = st.join(tag_list[idx:idx + 2])
            if str not in tag_tag:
                tag_tag[str] = [1, 0]
            else:
                temp2 = tag_tag[str]
                temp2[0] += 1
                temp2[1] += 0
                tag_tag[str] = temp2
    length = len(tag_list) - 4
    for idx in range(len(tag_list) - 2):
        if idx < length:
            st = '@@'
            str = st.join(tag_list[idx:idx + 3])
            if str not in tag_tag_tag:
                tag_tag_tag[str] = [1, 1]
            else:
                temp2 = tag_tag_tag[str]
                temp2[0] += 1
                temp2[1] += 1
                tag_tag_tag[str] = temp2
        else:
            st = '@@'
            str = st.join(tag_list[idx:idx + 3])
            if str not in tag_tag_tag:
                tag_tag_tag[str] = [1, 0]
            else:
                temp2 = tag_tag_tag[str]
                temp2[0] += 1
                temp2[1] += 0
                tag_tag_tag[str] = temp2
    tag['</s>'][0] += 1
print(len(tag_tag))
alpha = deletedInterpolation(tag, tag_tag, tag_tag_tag, total_count)

'''new_dict = {}
rare_words = []
final_words = []
for pair in words_list.items():
    if pair[1] not in new_dict.keys():
        new_dict[pair[1]] = []
    else:
        new_dict[pair[1]].append(pair[0])

for i in new_dict.items():
    final_words += new_dict[i]
rare_words += new_dict[1]
rare_words += new_dict[2]
rare_words += new_dict[3]
rareWords = set(rare_words)
finalWords = set(final_words)

finalWords = finalWords - rareWords'''


'''for word in word_tag:
    temp = word.split('/')
    if temp[0] in rareWords:
        str = '_RARE_/'+ temp[1]
        if str in word_tag:
            word_tag[str] += word_tag[word]
            word_tag[word].delete()
        else:
            word_tag[str] = word_tag[word]
            word_tag[word].delete()'''

print(word_tag)
transitionProbability(tag,tag_tag)
transitionProbabilitynnew(alpha, tag, tag_tag, tag_tag_tag, total_count)
line = "The third was being run by the head of an investment firm ."
#line = "ride make hay eat drink"

for wt in word_tag:
    temp = wt.rsplit('/',1)
    word_tag[wt] = word_tag[wt] / tag[temp[1]][0]

#fileWrite(tag,word_tag,transitionProbabilities,words_list)
fileWrite(tag,word_tag,transitionProbabilities_new,words_list)

print(tag)
print(len(words_list))
print ((tag_tag))
#print(transitionProbabilities)


