import Orange
data = Orange.data.Table('pre.tab')
ruledict = []
def get_freqItems():
    f = open('freqItems.csv','w+')
    inducer = Orange.associate.AssociationRulesInducer(support = 0.1, store_examples = True)
    for set in  inducer.get_itemsets(data):
        line = ''
        for item in set[0]:
            line+= str(data.domain[item[0]].name)+'='+str(data.domain[item[0]][item[1]])+'\t'
        line+= 'count='+str(len(set[1]))
        f.write(line+'\n')
        print line
    f.close()

def getAssociateRules():
    global ruledict
    f = open('Associaterule.csv', 'w+')
    rules = Orange.associate.AssociationRulesInducer(data, support=0.1,classificationRules = 1)
    for rule in rules:
        f.write('%f   %f  %f  %s  '%(rule.support,rule.confidence,rule.lift,rule)+'\n')
        ruledict.append((rule.support,rule.confidence,rule.lift, rule))
        print '%f   %f  %f  %s  '%(rule.support,rule.confidence,rule.lift,rule)
    f.close()
    print ruledict

def delRedundent():
    size = len(ruledict)
    rmatrix = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(-2)
        rmatrix.append(row)
    for i in range(size):
        for j in range(size):
            if(i < j):
                if str(ruledict[i][3]).split(' -> ')[0].find(str(ruledict[j][3]).split(' -> ')[0]) != -1 and ruledict[i][2]<ruledict[j][2] and str(ruledict[i][3]).split(' -> ')[1]==str(ruledict[j][3]).split(' -> ')[1]:
                    rmatrix[i][j] = 1
                elif str(ruledict[j][3]).split(' -> ')[0].find(str(ruledict[i][3]).split(' -> ')[0]) != -1 and ruledict[j][2]<ruledict[i][2] and str(ruledict[j][3]).split(' -> ')[1]==str(ruledict[i][3]).split(' -> ')[1]:
                    rmatrix[i][j] = -1
    flag = []
    for i in range(size):
        flag.append(0)
    for i in range(size):
        for j in range(size):
            if rmatrix[i][j] == 1:
                flag[i]=1
            elif rmatrix[i][j] == -1:
                flag[j]=1
    withoutRedt = []
    for i in range(size):
        if flag[i]!=1:
            withoutRedt.append(ruledict[i])
    f = open('AssociateRuleR.csv','w+')
    for item in withoutRedt:
        f.write(str(item)+'\n')
    f.close()
    return withoutRedt

if __name__ == '__main__':
    get_freqItems()
    getAssociateRules()
    delRedundent()
