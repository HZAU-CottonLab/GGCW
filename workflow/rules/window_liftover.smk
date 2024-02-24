#* get
referenceDict={
    'species_A':config['queryGenome'], #* J85
    'species_B':config['targetGenome'], #* HC04
}
#? genomeConfig: test/species_A.txt

rule window_liftover:
    input: 
        halFile='results/minigraph_cactus/{species}/{species}.full.hal',
        genomeConfig='test/{species}.txt',
        SYN_HYD='results/AlignmentBlock/{}-{}_SYN_HYD.txt'.format(
            config['queryGenome'],config['targetGenome']
        )
    output: 
        queryWindow=temp('results/window_liftover/{species}_query_window_temp.txt'),
        windowMatch='results/window_liftover/{species}_liftover.txt'
    params:
        referenceGenome=lambda wildcards:referenceDict.get(wildcards.species),
        selectColumns=lambda wildcards: '1,2,3' if wildcards.species=='species_A' else '4,5,6'
    shell: 
        '''
        #? All window Annotated
        cut -f{params.selectColumns} {input.SYN_HYD}|awk '$1!="."{{print $0}}' >{output.queryWindow}
        python3  workflow/scripts/window_liftover.py {output.queryWindow} \
                {params.referenceGenome} \
                {input.genomeConfig} \
                {input.halFile} \
                {output.windowMatch}
        '''

rule windowMerge_between_species:
    message: 'Merge liftover windows between species.'
    input:  
        SYN_HYD='results/AlignmentBlock/{}-{}_SYN_HYD.txt'.format(
            config['queryGenome'],
            config['targetGenome']
        ),
        queryGenome_liftover='results/window_liftover/species_A_liftover.txt',
        targetGenome_liftover='results/window_liftover/species_B_liftover.txt'
    output:
        all_window_liftover='results/AlignmentBlock/All_sample_SYN_HYD.txt'
    shell:
        '''
        python  workflow/scripts/windowMerge.py {input.SYN_HYD} {input.queryGenome_liftover} \
            {input.targetGenome_liftover} {output.all_window_liftover}
        '''

