rawDataPath=config['rawDataPath']
rule genome_masked:
    input: 
        rawFasta=lambda wildcards:'{}/{}.chr.fa'.format(
            rawDataPath,
            wildcards.accession
        ),
        maskedRegion=lambda wildcards:'{}/{}_softMasked_region.bed'.format(
            rawDataPath,
            wildcards.accession
        ),
    
    output: 
        maskedFasta='results/maskedGenome/{accession}-softmasked.fa'
    shell: 
        '''
        #TODO masked genome 
        cat {input.maskedRegion} |awk '{{print $1"\\t"$2-1"\\t"$3}}' \
            |seqtk seq -l 60 -M /dev/stdin {input.rawFasta} >{output.maskedFasta}
        '''