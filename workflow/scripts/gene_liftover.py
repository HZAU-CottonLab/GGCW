import pandas as pd 
import sys 
import re 
import logging
from util.bedtools import intersectBed


logging.basicConfig(
    level=logging.INFO
)

queryGenome=sys.argv[1]
window_liftover=pd.read_csv(
    sys.argv[2],header=0,index_col=None,sep="\t"
)

#! selected samples
window_liftover[queryGenome]=window_liftover.apply(
    lambda x:"{}:{}-{}".format(x['windowChr'],x['windowStart'],x['windowEnd']),axis=1
)

sampleList=[queryGenome]+list(window_liftover.columns[3:-1])
window_liftover=window_liftover[sampleList]

logging.info(
    "reading gene bed ... \n"
)

#? configure 
geneBedSetPath=sys.argv[3]
geneOrthoBedFile=dict()
for sample in sampleList:
    geneOrthoBedFile[sample]=geneOrthoBedFile.get(sample, 
        pd.read_csv(
                "{}/{}_ortholog.bed".format(
                    geneBedSetPath,sample
                ),
                header=None,index_col=None,sep="\t"
            )
    )

def get_queryRegion_OrthoId(queryRegion:pd.DataFrame,geneBed:pd.DataFrame,genome:str):
    '''
    @description state gene info in specific region
    '''
    intersectedData=intersectBed(
            queryRegion,geneBed
        )
    #! gene ID in this region
    filter_intersected=intersectedData.loc[ 
            intersectedData.apply(lambda x:True if int(x[4])>=int(x[1]) and int(x[5])<=int(x[2]) else False,axis=1)
        ]
    if filter_intersected.empty:
        #* non gene 
        return pd.DataFrame(columns=["orthoId",genome]) 
    #! multiple ortholog genes in one region
    reOrderData=[]
    for OrthoGroupId,GroupData in filter_intersected.groupby([8]):
        reOrderData.append(
            (OrthoGroupId[0],"-".join(GroupData[6].values))
        )
    reOrderData=pd.DataFrame(reOrderData,columns=["orthoId",genome])
    return  reOrderData

syntenicGeneInfo=[]
for val in window_liftover.values:
    logging.info(
        "deal with: >>>>>>>>>>>>>>>>>>>\n{}".format(
            "\t".join([str(i) for i in val])
        )
    )
    regionGenome=pd.DataFrame(columns=["orthoId"])
    for sample,genomeRegion in zip(sampleList,val):
        if genomeRegion==".":
            sampleRegion=pd.DataFrame(
                columns=["orthoId",sample]
            )
        else:
            #*split region chr
            Chr=genomeRegion.split(":")[0]
            Start=int(genomeRegion.split(":")[1].split("-")[0])
            End=int(genomeRegion.split("-")[-1])
            #! intersecter with gene region
            geneBedFile=geneOrthoBedFile.get(
                sample
            )
            sampleRegion=get_queryRegion_OrthoId(
                pd.DataFrame(
                    [(Chr,Start,End)]
                ),
                geneBedFile,
                sample
            )
        #* merge difference sample in this region
        regionGenome=pd.merge(
            regionGenome,
            sampleRegion,
            on=['orthoId'],
            how='outer'
        )
    regionGenome=regionGenome[['orthoId']+sampleList]
    for geneInfo in  regionGenome.values:
        syntenicGeneInfo.append(
            list(val)+ list(geneInfo)
        )
geneColumns=sampleList+['orthoId']+[ "{}_gene".format(i) for i in sampleList ]
syntenicGeneInfo=pd.DataFrame(
    syntenicGeneInfo,columns=geneColumns
)
syntenicGeneInfo.to_csv(
    sys.argv[4],header=True,index=False,sep="\t"
)