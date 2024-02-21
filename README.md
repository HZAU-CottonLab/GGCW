<h1 align="center">Graph genome comparison workflow</h1>
<div align="center">
    <a href="https://github.com/HZAU-CottonLab/GGCW/stargazers">
        <img src="https://img.shields.io/github/stars/HZAU-CottonLab/GGCW.svg" />
    </a>
    <a href="https://memotrace.cn/" target="_blank">
        <img alt="GitHub forks" src="https://img.shields.io/github/forks/HZAU-CottonLab/GGCW?color=eb6ea5">
    </a>
    <a href="https://memotrace.cn/" target="_blank">
        <img src="https://img.shields.io/badge/container-singularity-green" />
    </a>
    <a href="https://memotrace.cn/" target="_blank">
        <img src="https://img.shields.io/github/license/HZAU-CottonLab/GGCW" />
    </a>
    <a href="https://github.com/HZAU-CottonLab/GGCW/releases" target="_blank">
        <img alt="GitHub release (with filter)" src="https://img.shields.io/github/v/release/HZAU-CottonLab/GGCW">
    </a>
</div>

<blockquote>
    <div style="background-color: #eaf7ea; border-radius: 10px; padding: 20px; position: relative;">
    <div style="position: relative;">
        <div style="position: absolute;top: 0;bottom: 0;left: 0;width: 2px;background-color: #000000;"></div>
        <h2>GGCW</h2>
        <div style="text-indent: 2em;">
            <p>
                This workflow is designed for comparing different species at the pan-genomic level and provides base-level alignment information to identify sequence with <strong>synteny (SYN) </strong>as well as <strong>hyper divergence (HYD)</strong>. Moreover, according to the orthogroups inferred by OrthoFinder, homologous genes located in collinear regions can be identified.
            </p>
        </div>
    </div>
    </div>
</blockquote>

## Work flow
<div align="center">
    <img src="asset/workflow.png" height="540"/>
</div>

> The workflow is developed based on Snakemake, which comprises several interdependent parts. For instance, when comparing genomes, it is necessary to manually modify the corresponding configuration files.
```bash
#? example data direction test/
- raw_genome.config  #? for genome masked
- mashTree.config  #? for phylogenetic tree
- evolution.txt #? for Progressive-Cactus
- species_A.txt #? for Minigraph-Cactus
- species_B.txt #? Minigraph-Cactus
```

### Table of contents

- Genome alignment
    - softmasked genome
    - phylogenetic tree
    - Progressive-Cactus (aligning reference samples for different species)
    - Minigraph-Cactus (aligning same species)
    - identity SYN and HYD
-   homologous gene in SYN
    - OrthoFinder
    - identified homoeologous in SYN region

## Requirements

- Python
    - pandas
    - pysam
    - pybedtools
- Perl
- Snakemake
- Cactus
- mashtree
- quicktree
- seqtk


## Install

```bash

```


## Usage example

```bash

```


