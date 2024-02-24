inputFasta=[]
with open(config['mashTreeConfig'],'r') as File:
    for fastaFile in File:
        inputFasta.append(
            fastaFile.strip("\n")
        )
rule mashTree:
    message:
        "Creat a tree using mash distances."
    input: inputFasta
        #* multiple genome fasta
    output: 
        #* tree between species and used for cactus
        mtree='results/mashTree/topology.tree'
    threads: 4
    shell: 
        '''
        mashtree --sketch-size 20000 --genomesize 1500000000 \
            --numcpus {threads} --mindepth 0  {input}  > {output.mtree}
        '''