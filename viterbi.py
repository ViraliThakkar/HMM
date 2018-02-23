import json
import math

def nonrare(dictt):
    newDict = []
    for i in dictt:
        if dictt[i] > 3:
            newDict.append(i)
    return set(newDict)

def viterbi(tag, word_tag, transitionProbabilities, line):
    print(line)
    words = line.split()
    tags = list(tag.keys())
    tags.remove('<s>')
    tags.remove('</s>')
    tags.insert(0,'<s>')
    tags.insert(len(tags),'</s>')
    Matrix = [[0 for x in range(len(words))] for y in range(len(tag))] # rows = tags columns = words
    bMatrix = [[0 for x in range(len(words))] for y in range(len(tag))]
    for idx in range(1, len(tag) - 1):
        if tags[idx]+'|'+'<s>' in transitionProbabilities and words[0]+'/'+tags[idx] in word_tag:
            Matrix[idx][0] = transitionProbabilities[tags[idx]+'|'+'<s>']*word_tag[words[0]+'/'+tags[idx]]
            #Matrix[idx][0] = (-math.log(transitionProbabilities[tags[idx] + '|' + '<s>'])) + (-1*math.log(word_tag[words[0] + '/' + tags[idx]]))
            bMatrix[idx][0] = '<s>'
    for idx1 in range(1, len(words)):
        for idx2 in range(1, len(tags)-1):
            maxx=-1
            for idx3 in range(1, len(tags) - 1):
                if tags[idx2]+'|'+tags[idx3] in transitionProbabilities and words[idx1]+'/'+tags[idx2] in word_tag:
                    temp = Matrix[idx3][idx1 - 1] * transitionProbabilities[tags[idx2]+'|'+tags[idx3]] * word_tag[words[idx1]+'/'+tags[idx2]]
                    #temp = Matrix[idx3][idx1 - 1] + (-1*math.log(transitionProbabilities[tags[idx2]+'|'+tags[idx3]])) + (-1*math.log(word_tag[words[idx1]+'/'+tags[idx2]]))
                    if maxx < temp:
                        maxx = temp
                        bMatrix[idx2][idx1] = tags[idx3]
            Matrix[idx2][idx1] = maxx
    #print(bMatrix)

    maxx = -1
    for idx1 in range(1, len(tags) - 1):
        #if '</s>'+'|'+tags[idx1] in transitionProbabilities:
        temp = Matrix[idx1][len(words) - 1] * transitionProbabilities['</s>'+'|'+tags[idx1]]
        #temp = Matrix[idx1][len(words) - 1] + (-1*math.log(transitionProbabilities['</s>' + '|' + tags[idx1]]))
        if maxx < temp:
            maxx = temp
            bMatrix[0][len(words) - 1] = tags[idx1]
    Matrix[0][len(words) - 1] = maxx
    '''for index in range(len(words)):
        print('-----row')
        for index1 in range(len(tags)):
            if bMatrix[index1][index] != 0:
                print(bMatrix[index1][index]+'  {}'.format(index1))'''

    #print(tags)
    ans = []
    length = len(words) - 1
    ii = tags.index(bMatrix[0][len(words) - 1])
    for idx in range(len(words)):
        #print(tags[ii])
        ans.append(tags[ii])
        ii = tags.index(bMatrix[ii][length])
        length -= 1
    ans = ans[::-1]
    #delimeter = ' '
    #fop.write(delimeter.join(ans))
    return ans

def viterbinew(tag, word_tag, transitionProbabilities, line):
    print(line)
    words = line.split()
    #print(len(words))
    tags = list(tag.keys())
    tags.remove('<s>')
    tags.remove('</s>')
    tags.insert(0,'<s>')
    tags.insert(len(tags),'</s>')
    Matrix = [[0 for x in range(len(words))] for y in range(len(tag))] # rows = tags columns = words
    bMatrix = [[0 for x in range(len(words))]  for y in range(len(tag))]
    for idx in range(1, len(tag) - 1):
        if words[0]+'/'+tags[idx] in word_tag:
            Matrix[idx][0] = transitionProbabilities[tags[idx]+'|'+'<s>'+'@@'+'<s>']*word_tag[words[0]+'/'+tags[idx]]
            #Matrix[idx][0] = (-math.log(transitionProbabilities[tags[idx] + '|' + '<s>'])) + (-1*math.log(word_tag[words[0] + '/' + tags[idx]]))
            bMatrix[idx][0] = '<s>'
        else:
            Matrix[idx][0] = transitionProbabilities[tags[idx] + '|' + '<s>' + '@@' + '<s>'] #* word_tag[words[0] + '/' + tags[idx]]
            # Matrix[idx][0] = (-math.log(transitionProbabilities[tags[idx] + '|' + '<s>'])) + (-1*math.log(word_tag[words[0] + '/' + tags[idx]]))
            bMatrix[idx][0] = '<s>'
    if len(words) >= 2:
        #for idx1 in range(1, len(words)):
        for idx2 in range(1, len(tags)-1):
            maxx=-1
            for idx3 in range(1, len(tags) - 1):
                if tags[idx2]+ '|'+'<s>'+'@@'+tags[idx3]  in transitionProbabilities and words[1]+'/'+tags[idx2] in word_tag:
                    temp = Matrix[idx3][1] * transitionProbabilities[tags[idx2]+'|' + '<s>'+'@@'+tags[idx3] ] * word_tag[words[1]+'/'+tags[idx2]]
                    #temp = Matrix[idx3][idx1 - 1] + (-1*math.log(transitionProbabilities[tags[idx2]+'|'+tags[idx3]])) + (-1*math.log(word_tag[words[idx1]+'/'+tags[idx2]]))
                    if maxx < temp:
                        maxx = temp
                        bMatrix[idx2][1] = tags[idx3]
            Matrix[idx2][1] = maxx

    for idx1 in range(2, len(words)):
        for idx2 in range(1, len(tags)-1):
            maxx=-1
            for idx3 in range(1, len(tags) - 1):
                for idx4 in range(1, len(tags) - 1):
                    if tags[idx2]+'|'+tags[idx4] +'@@'+ tags[idx3] in transitionProbabilities and words[idx1]+'/'+tags[idx2] in word_tag:
                        temp = Matrix[idx3][idx1 - 1] * transitionProbabilities[tags[idx2]+'|'+tags[idx4]+'@@'+ tags[idx3]] * word_tag[words[idx1]+'/'+tags[idx2]]
                        #temp = Matrix[idx3][idx1 - 1] + (-1*math.log(transitionProbabilities[tags[idx2]+'|'+tags[idx3]])) + (-1*math.log(word_tag[words[idx1]+'/'+tags[idx2]]))
                        if maxx < temp:
                            maxx = temp
                            bMatrix[idx2][idx1] = tags[idx3]
            Matrix[idx2][idx1] = maxx
    #print(bMatrix)

    maxx = -1
    for idx1 in range(1, len(tags) - 1):
        for idx2 in range(1, len(tags) - 1):
            #if '</s>'+'|'+tags[idx1] in transitionProbabilities:
            temp = Matrix[idx1][len(words) - 1] * transitionProbabilities['</s>'+'|'+tags[idx2] + '@@' + tags[idx1]]
            #temp = Matrix[idx1][len(words) - 1] + (-1*math.log(transitionProbabilities['</s>' + '|' + tags[idx1]]))
            if maxx < temp:
                maxx = temp
                bMatrix[0][len(words) - 1] = tags[idx1]
    Matrix[0][len(words) - 1] = maxx
    '''for index in range(len(words)):
        print('-----row')
        for index1 in range(len(tags)):
            if bMatrix[index1][index] != 0:
                print(bMatrix[index1][index]+'  {}'.format(index1))'''

    #print(tags)
    ans = []
    length = len(words) - 1
    ii = tags.index(bMatrix[0][len(words) - 1])
    for idx in range(len(words)):
        #print(tags[ii])
        ans.append(tags[ii])
        #print(bMatrix[ii][length])
        #print(length)
        ii = tags.index(bMatrix[ii][length])
        length -= 1
    ans = ans[::-1]
    #delimeter = ' '
    #fop.write(delimeter.join(ans))
    return ans

fopen = open('hmmmodel.txt',encoding='utf8')
bigDict = json.load(fopen)
tag = bigDict[0]
word_tag = bigDict[1]
transitionProbabilities = bigDict[2]
nonrare_Words = nonrare(bigDict[3])
wwords = bigDict[3]
tags= list(tag.keys())
print(len(nonrare_Words))
train = open('en_dev_raw.txt',encoding="utf8")
fop = open('hmmoutput.txt','w',encoding='utf8')
answer = ''
for line in train:
    line_new = ''
    line = line.rstrip()
    words = line.split()
    for word in words:
        if word not in wwords:
            for idx in tags:
                word_tag[word + '/' + idx] = 1 / len(tags)
        '''if word not in nonrare_Words:
            line_new += '_RARE_'
        else:
            line_new += word
        line_new += ' '''
    final_tags = viterbinew(tag, word_tag, transitionProbabilities, line)
    for ii in range(len(words)):
        words[ii] = words[ii] + '/' + final_tags[ii]
    answer += ' '.join(words).rstrip()
    answer += '\n'
answer = answer.rstrip()
fop.write(answer)