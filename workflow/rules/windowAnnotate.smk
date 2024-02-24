queryGenome=config['queryGenome']
targetGenome=config['targetGenome']

rule halSynteny_window:
    input: 
        halFile='results/progressive_cactus/evolution.hal'
    output:
        #* 输出PSL文件
        pslFilePath="results/progressive_cactus/{}-{}.psl".format(queryGenome,targetGenome),
    benchmark: "results/benchmarks/halSynteny_{}_{}_benchmark.txt".format(queryGenome,targetGenome)
    params:
        minBlockSize=5000,
        maxAnchorDistance=5000,
    shell: 
        '''
        halSynteny {input.halFile}  --maxAnchorDistance {params.maxAnchorDistance} \
            --minBlockSize {params.minBlockSize} \
            --queryGenome {queryGenome} \
            --targetGenome {targetGenome} \
            {output.pslFilePath}
        '''

rawGenomePath=config['rawDataPath']
rule windowAnnotate_betweenSpecies:
    message: 'Get SYN and HYD region'
    input: 
         queryGenomeIndex='{}/{}.chr.fa.fai'.format(rawGenomePath,queryGenome),
         targetGenomeIndex='{}/{}.chr.fa.fai'.format(rawGenomePath,targetGenome),
         syntenyPSL="results/progressive_cactus/{}-{}.psl".format(queryGenome,targetGenome),
    output:
        syntenyBlock=temp('results/AlignmentBlock/{}-{}_SYN_temp.txt'.format(queryGenome,targetGenome)),
        all_Block='results/AlignmentBlock/{}-{}_SYN_HYD.txt'.format(queryGenome,targetGenome)
    shell: 
        '''
        #TODO synteny Block from PSL
        #* dealt with PSL file
        cat {input.syntenyPSL}|awk '{{
            print $10"\\t"$12"\\t"$13"\\t"$14"\\t"$16"\\t"$17"\\t"$9
            }}' >{output.syntenyBlock}
        #* get SYN and HYD 
        python3 workflow/scripts/SYN_HYD.py {output.syntenyBlock}  \
            {input.queryGenomeIndex} {input.targetGenomeIndex} \
            {output.all_Block}
        '''

