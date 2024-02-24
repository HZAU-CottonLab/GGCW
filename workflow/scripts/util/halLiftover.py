'''
Descripttion: 
version: 
Author: zpliu
Date: 2023-07-26 19:45:12
LastEditors: zpliu
LastEditTime: 2023-08-04 14:52:06
@param: 
'''
import pandas as pd 
import subprocess
import os 
from tempfile import NamedTemporaryFile

def halLiftover(queryBed,halFile,queryGenome,targetGenome):
    '''
    @queryBed: pd.DataFrame
    @halFile:
    @queryGenome:
    @targetGenome: 
    '''
    #? exec in container
    halbin='halLiftover'
    queryBedFile=NamedTemporaryFile(mode="w+")
    targetFile=NamedTemporaryFile(mode="w+")
    queryBed.to_csv(
        queryBedFile.name,header=False,index=False,sep="\t"
    )
    #* use halLiftover
    commond='{} --outPSL {} {} {} {} {} '.format(
        halbin,halFile,queryGenome,queryBedFile.name,targetGenome,targetFile.name
    )
    subprocess.run(
       args=[commond],
        check=True,
        shell=True
    )
    #* get liftover window
    if os.path.getsize(targetFile.name)>0:
        PSLout=pd.read_csv(
            targetFile.name,
            header=None,index_col=None,sep="\t"
        )
    else:
        raise Exception("query Chrom not in hal or can't liftover this region")
    queryBedFile.close()
    targetFile.close()
    return PSLout

if __name__ =="__main__":
    #* query window
    queryBed=pd.DataFrame(
        [ 
            ("A13",99781907,99781914)
        ]
    )
    halLiftover(
    queryBed,'A13.full.hal',
    "HC04-A13","TW100-A13"
    )