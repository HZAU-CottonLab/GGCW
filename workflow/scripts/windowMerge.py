#TODO merge liftover windows
import pandas as pd 
import sys 
import logging 
logging.basicConfig(
    level=logging.INFO
)



SYN_HYD=pd.read_csv(
    sys.argv[1],header=None,sep="\t",index_col=None
)

query_liftover=pd.read_csv(
    sys.argv[2],header=0,index_col=None,sep="\t"
)
target_liftover=pd.read_csv(
    sys.argv[3],header=0,index_col=None,sep="\t"
)

#? windowRegion
step1_merge=pd.merge(
    SYN_HYD,
    query_liftover,
    left_on=[0,1,2],
    right_on=['windowChr','windowStart','windowEnd'],
    how='outer'
)
selectcolumns=[i for i in step1_merge.columns if i not in ['windowChr','windowStart','windowEnd'] ]
step1_merge=step1_merge[selectcolumns]

#* 
setp2_merge=pd.merge(
    step1_merge,
    target_liftover,
    left_on=[3,4,5],
    right_on=['windowChr','windowStart','windowEnd'],
    how='outer'
)
selectcolumns=[i for i in setp2_merge.columns if i not in ['windowChr','windowStart','windowEnd'] ]
setp2_merge=setp2_merge[selectcolumns]

setp2_merge.to_csv(
    sys.argv[4],
    header=False,index=False,sep="\t"
)