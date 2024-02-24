
#TODO Get SYN and HYD sequence from synteny Block
import sys 
import pandas  as pd 
import re
from util.bedtools import merge_bed,intersectBed,subtractBed_genome
import logging 
logging.basicConfig(
    level=logging.INFO
)



syntenyRegion=pd.read_csv(
    sys.argv[1],
    header=None,index_col=None,sep="\t"
)

#* merge synteny bed
query_synteny=syntenyRegion.sort_values(by=[0,1,2])[[0,1,2]]
query_mergeBed=merge_bed(query_synteny)
target_synteny=syntenyRegion.sort_values(by=[3,4,5])[[3,4,5]]
target_mergeBed=merge_bed(target_synteny)


#* get divergence region
queryGenomeIndex=sys.argv[2]
targetGenomeIndex=sys.argv[3]
querySubstractBed=subtractBed_genome(
    queryGenomeIndex,query_mergeBed
)
targetSubstractBed=subtractBed_genome(
    targetGenomeIndex,target_mergeBed
)

syntenyRegion['regionType']='synteny'
query_HYD=[]
for val in querySubstractBed.values:
    query_HYD.append(
        (val[0],int(val[1]),int(val[2]),'.',-1,-1,'divergence')
    )
target_HYD=[]
for val in targetSubstractBed.values:
    target_HYD.append(
        ('.',-1,-1,val[0],int(val[1]),int(val[2]),'divergence')
    )

query_HYD=pd.DataFrame(query_HYD,columns=[0,1,2,3,4,5,'regionType'])
target_HYD=pd.DataFrame(target_HYD,columns=[0,1,2,3,4,5,'regionType'])


#TODO  merge all windows
#? synteny 
#? divergence
logging.info("merge all annotated windows")
mergeData=pd.concat(
    [ 
        syntenyRegion[[0,1,2,3,4,5,'regionType']],
        query_HYD,
        target_HYD
    ]
)

mergeData.to_csv(
    sys.argv[4],header=False,index=False,sep="\t"
)





