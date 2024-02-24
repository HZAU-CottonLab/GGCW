rule geneBed_annotated:
    message:"Get Gene bed information"
    input: 
        gff3='test/GeneSet/{sample}.final.gene.gff3',
        orthogroupData='test/GeneSet/Orthogroups.tsv'
    output: 
        geneBed='results/GeneSet/geneBed/{sample}_ortholog.bed'
    shell: 
        '''
         python workflow/scripts/Ortholog_bed.py {input.gff3} {wildcards.sample} \
                {input.orthogroupData} {output.geneBed}
        '''



referenceDict={
    'species_A':config['queryGenome'], #* J85
    'species_B':config['targetGenome'], #* HC04
}
rule syntelog_gene_within_species:
    input:
        #? window liftover from halliftover
        window_liftover='results/window_liftover/{species}_liftover.txt' 
    output:
        syngelogGene='results/GeneSet/{species}_syntelog.txt' 
    threads:1
    params:
        geneBedPath='results/GeneSet/geneBed/',
        referenceGenome=lambda wildcards:referenceDict.get(wildcards.species)
    benchmark: "results/benchmarks/syntelogGene_{species}_benchmark.txt"
    shell:
        '''
        python workflow/scripts/gene_liftover.py {params.referenceGenome} {input.window_liftover} \
            {params.geneBedPath} {output.syngelogGene}
        '''
