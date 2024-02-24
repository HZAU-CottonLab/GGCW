import pandas as pd 
import sys 

#TODO set gene bed 
gene_gff=pd.read_csv(
    sys.argv[1],
    header=None,index_col=None,sep="\t",
    comment='#'
)
sampleName=sys.argv[2]
OrthogroupData=pd.read_csv(
    sys.argv[3],header=0,index_col=None,sep="\t"
)
#? get gene Id
gene_gff[9]=gene_gff[8].apply(lambda x:x[3:].split(";")[0])
geneBed=gene_gff.loc[gene_gff[2]=="gene"]
#* bed of gene
geneBed=geneBed[[0,3,4,9,6]]
geneBed.index=range(0,geneBed.shape[0])

def gene_map_orthogroup(mapDict,OrthoId,geneList,sample):
    if pd.isna(geneList):
        #*
        pass
    else:
        for geneId in geneList.split(","):
            geneId=geneId.strip()
            mapDict[geneId]=mapDict.get(geneId,OrthoId)


GeneMap_dict=dict()
OrthogroupData[['Orthogroup',"{}.pep".format(sampleName)]].apply(     
        lambda x:gene_map_orthogroup(GeneMap_dict,x.iloc[0],x.iloc[1],sampleName),axis=1
    )
geneBed[7]=geneBed[9].apply(
        lambda x:GeneMap_dict.get(
            x,"None"
        )
    )    

#* save bed file
geneBed.to_csv(
    sys.argv[4],header=False,index=False,sep="\t"
)