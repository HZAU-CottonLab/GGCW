rule progressive_cactus:
    input: 
        fastaConfig=config['progressiveConfig']
    output: 
        hal='results/progressive_cactus/evolution.hal'
    params:
        tmpStore='./progressive_tmp'
    benchmark: "results/benchmarks/progressive_cactus_benchmark.txt"
    threads: 20
    shell: 
        '''
        cactus {params.tmpStore} {input.fastaConfig} {output.hal} --maxCores {threads} --logInfo
        '''