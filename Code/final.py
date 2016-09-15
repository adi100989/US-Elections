
# coding: utf-8

# In[1]:

import numpy as np
import scipy.stats as ss
import pandas as pd
import math
import pandas.core.frame as pdf
import sklearn
from sklearn import preprocessing as ppc
from sklearn.decomposition import PCA

CANDIDATES = ['Hillary','Cruz','Sanders','Donald']
primary_results = 'primary_results.csv'
county_facts = 'county_facts.csv'

print("loading %s" % primary_results)
primaryResultDF = pd.read_csv(primary_results,sep=',',low_memory=False)
print("loading %s" % county_facts)
countyFactsDF = pd.read_csv(county_facts,sep=',',low_memory=False)

countyFactsDF = countyFactsDF[countyFactsDF['state_abbreviation']!= ""]

def concatCountyFactsWithPrimaryResult(countyDF, primaryDF, popDF, sentDF, name):
    primaryDataForName = primaryDF[primaryDF.candidate == name]
    #countyDF = countyDF[countyDF['fips'].isin(primaryDataForName['fips'])]
    #popDF = popDF[popDF['county'].isin(primaryDataForName['county'])]
    #sentDF = sentDF[sentDF['county'].isin(primaryDataForName['county'])]
    frames = [primaryDataForName,countyDF]
    result = pd.merge(primaryDataForName, countyDF, on=['fips', 'fips'])
    #result = pd.merge(primaryDataForName, countyDF, left_on = ['state','county'],right_on = ['state','county'])
    result.drop(['fips','party','candidate','fraction_votes','area_name','state_abbreviation_x','state_abbreviation_y'],inplace=True,axis=1)
    result.to_csv('./YYYYYY.csv')
    popDF.to_csv('./ZZZZZZZ.csv')
    result = pd.merge(result,popDF,on = ['state','county'],how = 'inner')
    result.to_csv('./XXXXXXX.csv')
    result = pd.merge(result,sentDF,left_on = ['state','county'],right_on = ['state','county'],how = 'inner')
    return result
    
def getCandidateDF(name):
    return concatCountyFactsWithPrimaryResult(countyFactsDF, primaryResultDF, name)

def getMatrix(name,train_or_test):
    list1= []
    popDF = pd.read_excel('popularity_' + train_or_test + '.xlsx',sheetname = name,sep = ',')
    sentDF = pd.read_excel('sentiment_' + train_or_test + '.xlsx',sheetname = name,sep = ',')
    pInd = popDF.index
    pCol = popDF.columns
    sInd = sentDF.index
    sCol = sentDF.columns
    print train_or_test
    for i in pInd:
        popDF.loc[i,'county'] = str(popDF.loc[i,'county']).lstrip().rstrip()
        popDF.loc[i,'state'] = str(popDF.loc[i,'state']).lstrip().rstrip()
    for i in sInd:
        #print sentDF.loc[i,'county']
        sentDF.loc[i,'county'] = str(sentDF.loc[i,'county']).lstrip().rstrip()
        sentDF.loc[i,'state'] = str(sentDF.loc[i,'state']).lstrip().rstrip()
    result = concatCountyFactsWithPrimaryResult(countyFactsDF,primaryResultDF,popDF,sentDF,name)
    result = result.reindex(np.random.permutation(result.index))
    county = result['county']
    state = result['state']
    y = result['votes']  
    result.drop(['votes','county','state'],inplace=True,axis=1)
    list1.append(result)
    list1.append(y)
    list1.append(county)
    list1.append(state)
    return list1


# In[2]:

PCA_START = 1
TEST_RUNS = 51 #change to 51
L2_START = -15
L2_END = 23
L2_RUNS = 37 #change to 37
L2_STEP = (float)(L2_END - L2_START) / L2_RUNS
CANDIDATES = ['Donald Trump','Ted Cruz','Hillary Clinton','Bernie Sanders']

def n_fold_with_dev(pred_mtr,outcome,n,mthd):
    outcome = np.asarray(outcome)
    total = pred_mtr.shape[0]
    step = int(total / n)
    count = 0
    min_MSE = np.inf
    min_testMSE = np.inf
    best_count = np.inf
    best_n = np.inf
    best_numda = np.inf
    best_alpha = np.inf
    while count < TEST_RUNS:
        for p in range(L2_RUNS): 
            if mthd == 'PCA':
                mypca = PCA(PCA_START + count)
                pca_mtr = mypca.fit(pred_mtr).components_
                pca_npred = np.dot(pred_mtr,pca_mtr.T)
            MSE = 0
            testMSE = 0
            if mthd != 'PCA' and count == 0:
                MSE = np.inf
                testMSE = np.inf
            for i in range(n):
                if i == n - 2:
                    dev_range = list(range(step * (n - 2),step * (n - 1)))
                    test_range = list(range(step * (n - 1),step * n))
                    train_range = list(range(0,step * (n - 2)))
                elif i == n - 1:
                    dev_range = list(range(step * (n - 1),step * n))
                    test_range = list(range(0,step))
                    train_range = list(range(step,step * (n - 1)))
                else:
                    dev_range = list(range(step * i,step * i + step))
                    test_range = list(range(step * (i + 1),step * (i + 2)))
                    train_range = list(range(0,step * i)) + list(range(step * (i + 2),step * n))
                train_set = pred_mtr[train_range]
                test_set = pred_mtr[test_range]
                dev_set = pred_mtr[dev_range]
                train_y = outcome[train_range]
                test_y = outcome[test_range]
                dev_y = outcome[dev_range]

                if mthd == 'PCA':
                    train_set_pca = pca_npred[train_range]
                    test_set_pca = pca_npred[test_range]
                    dev_set_pca = pca_npred[dev_range]
                    clf = sklearn.linear_model.Ridge(alpha = 2 ** (L2_START + p),fit_intercept = True,normalize = False)
                    model = clf.fit(train_set_pca,train_y)
                    y_pred = model.predict(dev_set_pca)
                    y_test_pred = model.predict(test_set_pca)
                    dif = dev_y - y_pred
                    dif_test = test_y - y_test_pred
                    MSE += (sum(dif * dif)) / len(dif)
                    testMSE += (sum(dif_test * dif_test)) / len(dif_test)
            testMSE = testMSE / n
            MSE = MSE / n
            if MSE < min_MSE:
                min_MSE = MSE
                best_count = PCA_START + count
                min_testMSE = testMSE
                best_alpha = 2 ** (L2_START + p)
                best_model = model
            #print('Components: %d\nALPHA: %f\nMSE: %f\n'%(PCA_START + count,2 ** (L2_START + p),MSE))
        count += 1
    #print('Best components: %d\Best alpha: %f'%(best_count,best_alpha))
    full_pca = PCA()
    pca_mtr = full_pca.fit(pred_mtr).components_
    pca_mtr = pca_mtr[range(0,best_count)]
    pca_mtr = pca_mtr.T	
    #print('Best Test MSE:%f'%min_testMSE)

    return [min_testMSE,pca_mtr,best_model]

def get_mapping(X,Y,n = 10,with_MSE = False):
    PCA_mapping = n_fold_with_dev(X, Y, n, 'PCA')
    if with_MSE:
        return PCA_mapping
    return PCA_mapping[1]

def my_main(candList):
    #outFile = open('./PCA_out.txt','w')
    PCA_Dict = {}
    for name in candList:
        PCA_Dict[name] = []
        dataMtr = getMatrix(name,'train')
        X = dataMtr[0].as_matrix()
        Y = dataMtr[1].values.T.tolist()
        PCA_mapping = get_mapping(X,Y,n = 10,with_MSE = True)
        #outFile.write(name + ':\nMSE: %f\nPCA_Matrix:\n'%PCA_mapping[0])
        #outFile.write(str(PCA_mapping[1]) + '\n\n')
        PCA_Dict[name].append(PCA_mapping[1])
        PCA_Dict[name].append(PCA_mapping[2])
    #outFile.close()
    return PCA_Dict

def PrimaryPredict(CANDIDATE_LIST):
    model_dict = my_main(CANDIDATES)
    Pred_Dict = {}
    for name in CANDIDATE_LIST:
        dataMtr = getMatrix(name,'test')
        X = dataMtr[0].as_matrix()
        pca_mtr = np.dot(X,model_dict[name][0])
        pred = model_dict[name][1].predict(pca_mtr)
        Pred_Dict[name] = pred
        df_pred = [dataMtr[3],dataMtr[2],pred]
        df_pred = pd.DataFrame.from_records(df_pred)
        df_pred = df_pred.T
        df_pred.to_csv('./results/Predict_' + name + '.csv')
    return Pred_Dict

def n_fold_with_dev_2(pred_mtr,outcome,n,mthd):
    # mthd = 'PCA'|'L1'|'L2' for different methods
    pred_mtr = ppc.scale(pred_mtr)
    outcome = ppc.scale(outcome)
    outcome = np.asarray(outcome)
    total = pred_mtr.shape[0]
    step = int(total / n)
    count = 0
    min_MSE = np.inf
    min_testMSE = np.inf
    best_count = np.inf
    best_n = np.inf
    best_numda = np.inf
    best_alpha = np.inf
    while count < TEST_RUNS:
        for p in range(L2_RUNS): 
            if mthd == 'PCA':
                mypca = PCA(PCA_START + count)
                pca_mtr = mypca.fit(pred_mtr).components_
                pca_npred = np.dot(pred_mtr,pca_mtr.T)
            MSE = 0
            testMSE = 0
            if mthd != 'PCA' and count == 0:
                MSE = np.inf
                testMSE = np.inf
            for i in range(n):
                if i == n - 2:
                    dev_range = list(range(step * (n - 2),step * (n - 1)))
                    test_range = list(range(step * (n - 1),step * n))
                    train_range = list(range(0,step * (n - 2)))
                elif i == n - 1:
                    dev_range = list(range(step * (n - 1),step * n))
                    test_range = list(range(0,step))
                    train_range = list(range(step,step * (n - 1)))
                else:
                    dev_range = list(range(step * i,step * i + step))
                    test_range = list(range(step * (i + 1),step * (i + 2)))
                    train_range = list(range(0,step * i)) + list(range(step * (i + 2),step * n))
                train_set = pred_mtr[train_range]
                test_set = pred_mtr[test_range]
                dev_set = pred_mtr[dev_range]
                train_y = outcome[train_range]
                test_y = outcome[test_range]
                dev_y = outcome[dev_range]
        
                if mthd == 'PCA':
                    train_set_pca = pca_npred[train_range]
                    test_set_pca = pca_npred[test_range]
                    dev_set_pca = pca_npred[dev_range]
                    clf = sklearn.linear_model.Ridge(alpha = 2 ** (L2_START + p),fit_intercept = True,normalize = False)
                    model = clf.fit(train_set_pca,train_y)
                    y_pred = model.predict(dev_set_pca)
                    y_test_pred = model.predict(test_set_pca)
                    dif = dev_y - y_pred
                    dif_test = test_y - y_test_pred
                    MSE += (sum(dif * dif)) / len(dif)
                    testMSE += (sum(dif_test * dif_test)) / len(dif_test)
            testMSE = testMSE / n
            MSE = MSE / n
            if MSE < min_MSE:
                min_MSE = MSE
                best_count = PCA_START + count
                min_testMSE = testMSE
                best_alpha = 2 ** (L2_START + p)
                best_model = model
            #print('Components: %d\nALPHA: %f\nMSE: %f\n'%(PCA_START + count,2 ** (L2_START + p),MSE))
        count += 1
    print('Best components: %d'%(best_count))
    full_pca = PCA()
    pca_mtr = full_pca.fit(pred_mtr).components_
    pca_mtr = pca_mtr[range(0,best_count)]
    pca_mtr = pca_mtr.T
    print('Best Test MSE:%f'%min_testMSE)

    return [min_testMSE,pca_mtr,best_model]

def get_mapping_2(X,Y,n = 10,with_MSE = False):
    PCA_mapping = n_fold_with_dev_2(X, Y, n, 'PCA')
    if with_MSE:
        return PCA_mapping
    return PCA_mapping[1]

def my_main_2(candList):
    outFile = open('./PCA_out_2.txt','w')
    PCA_Dict = {}
    print "Calculating MSEs for candidates {Donald Trump, Ted Cruz, Hillary Clinton, Bernie Sanders} in this order :\n"
    for name in candList:
        PCA_Dict[name] = []
        dataMtr = getMatrix(name,'train')
        X = dataMtr[0].as_matrix()
        Y = dataMtr[1].values.T.tolist()
        PCA_mapping = get_mapping_2(X,Y,n = 10,with_MSE = True)
        outFile.write(name + ':\nMSE: %f\nPCA_Matrix:\n'%PCA_mapping[0])
        outFile.write(str(PCA_mapping[1]) + '\n\n')
        PCA_Dict[name].append(PCA_mapping[1])
        PCA_Dict[name].append(PCA_mapping[2])
    outFile.close()
    return PCA_Dict

def PrimaryPredict_2(CANDIDATE_LIST):
    model_dict = my_main_2(CANDIDATES)
    Pred_Dict = {}
    for name in CANDIDATE_LIST:
        dataMtr = getMatrix(name,'test')
        X = dataMtr[0].as_matrix()
        pca_mtr = np.dot(X,model_dict[name][0])
        pred = model_dict[name][1].predict(pca_mtr)
        Pred_Dict[name] = pred
        df_pred = [dataMtr[3],dataMtr[2],pred]
        df_pred = pd.DataFrame.from_records(df_pred)
        df_pred = df_pred.T
        #df_pred.to_csv('./Predict_2_' + name + '.csv')
    return Pred_Dict

if __name__ == '__main__':
    #for values
    PrimaryPredict(CANDIDATES)
    PCA_START = 1
    TEST_RUNS = 51
    L2_START = -15
    L2_END = 23
    L2_RUNS = 37
    L2_STEP = (float)(L2_END - L2_START) / L2_RUNS
    CANDIDATES = ['Donald Trump','Ted Cruz','Hillary Clinton','Bernie Sanders']
    PrimaryPredict_2(CANDIDATES)


# In[3]:

def Aggregation(candidate_name_1, candidate_name_2, candidate_name_3, candidate_name_4):
    candidate_1 = pd.read_csv("results/Predict_" + candidate_name_1)
    candidate_2 = pd.read_csv("results/Predict_" + candidate_name_2)
    candidate_3 = pd.read_csv("results/Predict_" + candidate_name_3)
    candidate_4 = pd.read_csv("results/Predict_" + candidate_name_4)
    
    votes_1 = {}
    votes_2 = {}
    votes_3 = {}
    votes_4 = {}
    sum =  0
    #print len(candidate_1)
    
    for i in xrange(len(candidate_1)):
        if candidate_1['0'][i] not in votes_1 :
            votes_1.update({candidate_1['0'][i]:candidate_1['2'][i]})
        elif candidate_1['0'][i] in votes_1 :   
            votes_1[candidate_1['0'][i]] += candidate_1['2'][i]
    
    #print votes_1['Mississippi']
    
    for i in xrange(len(candidate_2)):
        if candidate_2['0'][i] not in votes_2 :
            votes_2.update({candidate_2['0'][i]:candidate_2['2'][i]})
        elif candidate_2['0'][i] in votes_2 :   
            votes_2[candidate_2['0'][i]] += candidate_2['2'][i]

    for i in xrange(len(candidate_3)):
        if candidate_3['0'][i] not in votes_3 :
            votes_3.update({candidate_3['0'][i]:candidate_3['2'][i]})
        elif candidate_3['0'][i] in votes_3 :   
            votes_3[candidate_3['0'][i]] += candidate_3['2'][i]
            
    for i in xrange(len(candidate_4)):
        if candidate_4['0'][i] not in votes_4 :
            votes_4.update({candidate_4['0'][i]:candidate_4['2'][i]})
        elif candidate_4['0'][i] in votes_4 :   
            votes_4[candidate_4['0'][i]] += candidate_4['2'][i]
    
    #print votes_2
    '''
    list_item_1 = []    
    list_item_2 = [] 
    list_item_3 = [] 
    list_item_4 = [] 
    #print votes_2['Utah']
       
    for item in votes_1:
        list_item_1.append([item, votes_1[item]])
    list_item_1.sort(key=lambda x: x[0])
    for item in votes_2:
        list_item_2.append([item, votes_2[item]])
    list_item_2.sort(key=lambda x: x[0])
    for item in votes_3:
        list_item_3.append([item, votes_3[item]])
    list_item_3.sort(key=lambda x: x[0])
    for item in votes_4:
        list_item_4.append([item, votes_4[item]])
    list_item_4.sort(key=lambda x: x[0])
    '''
    #print list_item_2
    i = 0
    j = 0
    k = 0
    l = 0
    f1 = open('final_result.csv', 'w+')
    print >>f1, "state,Hillary,DemOthers,Trump,RepOthers"
    #print votes_2['Alabama']
    #print list_item_1
    for item in votes_1:
        #print item
        #print votes_2[item[0]]
        val_1 = int(votes_1[item])
        if item in votes_2:
            #print "has"
            val_2 = int(votes_2[item])
        else:
            val_2 = 0
        if item in votes_3:
            #print "has"
            val_3 = int(votes_3[item])
        else:
            val_3 = 0
        if item in votes_4:
            #print "has"
            val_4 = int(votes_4[item])
        else:
            val_4 = 0
        #print >>f1, item[0], ",", int(item[1]), ",", int(list_item_2[j][1]), ",", int(list_item_3[k][1]), ",", int(list_item_4[l][1])
        print >>f1, item, ",", val_1, ",", val_2, ",", val_3, ",", val_4
        #int(list_item_2[i][1]), ",", int(list_item_3[i][1]), ",", int(list_item_4[i][1])
        i += 1
        

Aggregation("Hillary Clinton.csv", "Bernie Sanders.csv", "Donald Trump.csv", "Ted Cruz.csv")
    


# In[4]:

import csv
PROB_DEM = dict()
free_voters = dict()
print "Primaries prediction done!! Now predicting final results..."
print "Reading primary_to_final.csv..."
available = open('final_result.csv').read()
with open('primary_to_final.csv', 'rb') as csvfile:
        data = csv.reader(csvfile)
        csvfile.next()
        for row in data:
            #print row
            state, obama, dem, john, rep, finalObama, finalJohn = row
            freevoter = int(finalObama) + int(finalJohn) - int(rep) - int(john) - int(dem) - int(obama)
            free_voters[state] = freevoter
            #print freevoter
            totalVoters = int(finalObama) + int(finalJohn)
            #print totalVoters
            obamaPerformance = int(obama)*1.00/(int(obama) + int(john))
            #print obamaPerformance
            othersVotes = int(dem) + int(rep)
            #print othersVotes
            obamaTotal = int(obama) + obamaPerformance*othersVotes
            #print obamaTotal
            PROB_DEM[state] = (int(finalObama)*1.0 - int(obamaTotal)*1.0)/(freevoter*1.0)
        #pprint(PROB_DEM)
trumpFinal = dict()
hillaryFinal = dict()
print "Reading Part 1 (primary)results..."
with open('final_result.csv', 'rb') as csvfile:
        data = csv.reader(csvfile)
        csvfile.next()
        for row in data:
            #state, state_abb, county, fips, party, candidate, votes, fraction_votes = row
            state, Hillary, DemOthers, Trump, RepOthers = row
            state = state.strip()
            trumpPerformance = int(Trump)*1.00/(int(Trump) + int(Hillary))
            othersVotes = int(DemOthers) + int(RepOthers)
            trumpTotal = int(Trump) + trumpPerformance*othersVotes
            hillaryTotal = int(Hillary) + (1-trumpPerformance)*othersVotes
            trumpFinal[state] = int(free_voters[state]*PROB_DEM[state] + trumpTotal)
            hillaryFinal[state] = int(free_voters[state]*(1-PROB_DEM[state]) + hillaryTotal)
        #pprint(hillaryFinal)
print "\nFinal results statewise :\n"
with open('electoral_votes.csv', 'rb') as csvfile:
        data = csv.reader(csvfile)
        csvfile.next()
        hillary_counts = 0
        trump_counts = 0
        i = 0
        hill = 0
        dump = 0
        for row in data:
            state, electoral_votes = row
            state = state.strip()
            if state in available:
                i += 1
                electoral_votes = int(electoral_votes)
                if(hillaryFinal[state] > trumpFinal[state]):
                    hillary_counts += electoral_votes
                    hill += 1
                    print state, "won by Hillary"
                else:
                    trump_counts += electoral_votes
                    print state, "won by Trump"
                    dump += 1
        print "\nTrump   Total :", trump_counts, "("+str(dump)+" states)"
        print "Hillary Total :", hillary_counts, "("+str(hill)+" states)"
        if(trump_counts > hillary_counts):
            print "Congratualtions Trump!! :("
        else:
            print "\nCogratualtions Hillary!! :)"
        print i

