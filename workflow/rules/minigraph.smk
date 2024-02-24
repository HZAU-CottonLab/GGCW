referenceDict={
    'species_A':config['queryGenome'], #* J85
    'species_B':config['targetGenome'], #* HC04
}

rule minigraph_cactus:
    input: 
        fastaConfig='/data/zpliu/Graph_genome_comparison_workflow/test/{species}.txt'
    output: 
        hal='results/minigraph_cactus/{species}/{species}.full.hal',
    params:
        tmpStore=lambda wildcards:'./minigraph_tmp_{}/'.format(wildcards.species),
        outputDir=lambda wildcards:'results/minigraph_cactus/{}/'.format(wildcards.species),
        reference=lambda wildcards:referenceDict.get(wildcards.species)
    benchmark: "results/benchmarks/minigraph_cactus_{species}_benchmark.txt"
    threads: 20
    shell: 
        '''
        cactus-pangenome {params.tmpStore} {input.fastaConfig} --outDir {params.outputDir} \
        --reference {params.reference} \
        --outName {wildcards.species} \
        --maxCores {threads} --logInfo
        '''