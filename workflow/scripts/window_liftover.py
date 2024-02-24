import pandas as pd 
import sys
import re 
import logging
from util.bedtools import intersectBed
from util.halLiftover import halLiftover
logging.basicConfig(
    level=logging.INFO
)
query_windows=pd.read_csv(
    sys.argv[1],header=None,index_col=None,sep="\t"
)
queryGenome=sys.argv[2]

target_Samples=[]
with open(sys.argv[3],'r') as File:
    for line in File:
        line=re.split("\s+",line)
        if line[0]!=queryGenome:
            target_Samples.append(line[0])

halFile=sys.argv[4]
liftoverData_finally=pd.DataFrame()

#? 
for queryChr,Chrwindow  in query_windows[[0,1,2]].groupby([0]):
    ChrData=pd.DataFrame(columns=['windowChr','windowStart','windowEnd'])
    for targetGenome in target_Samples:
        logging.info("parseing {} vs {}".format(queryChr,targetGenome))
        genomeData=[]
        try:
            liftoverData=halLiftover(
                Chrwindow,halFile,queryGenome,targetGenome
            )
        except Exception as e:
            #* can't liftover this region in target genome
            logging.info("{}:{}".format(e,queryChr))
            for window in Chrwindow.values:
                genomeData.append(
                    (
                        window[0],int(window[1]),int(window[2]),"."
                    )
                )
            continue
        intersectedData=intersectBed(
            Chrwindow,liftoverData[[9,11,12,13,15,16,0,2,8]]
        )
        for window,windowLiftover in intersectedData.groupby([0,1,2]):
            if windowLiftover.iloc[0,3] ==".":
                #*  can't liftover this region in target genome
                genomeData.append(
                    (
                        window[0],int(window[1]),int(window[2]),"."
                    )
                )
            else:
                windowLiftover[12]=windowLiftover.apply(
                    lambda x: int(x[9])+int(x[10]), axis=1
                )
                windowLiftover=windowLiftover.sort_values(by=[12],ascending=False)
                #* filter query less than intersect query
                windowLiftover=windowLiftover.loc[
                    windowLiftover.apply(
                        lambda x:True if int(x[1])<=int(x[4]) and int(x[2])>=int(x[5]) else False,axis=1
                    )
                ]
                if windowLiftover.empty:
                    genomeData.append(
                    (
                        window[0],int(window[1]),int(window[2]),"."
                        )
                    )
                    continue
                genomeData.append(
                    (
                        window[0],int(window[1]),int(window[2]),"{}:{}-{}".format(
                            windowLiftover.iloc[0,6],windowLiftover.iloc[0,7],windowLiftover.iloc[0,8]
                        )
                    )
                )
        genomeData=pd.DataFrame(genomeData,columns=['windowChr','windowStart','windowEnd',targetGenome])
        #* add different sample result
        ChrData=pd.merge(ChrData,genomeData,on=['windowChr','windowStart','windowEnd'],how='outer')
    liftoverData_finally=pd.concat([liftoverData_finally,ChrData],axis=0)

liftoverData_finally.to_csv(
    sys.argv[5],header=True,sep="\t",index=False
)