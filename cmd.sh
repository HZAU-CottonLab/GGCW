#TODO 安装Snakemake 



#TODO 构造整个流程的容器
#? 拉取Cactus镜像
singularity  pull docker://quay.io/comparative-genomics-toolkit/cactus:v2.7.1



#TODO 基于Cactus镜像进行构造该pipline
singularity  build --sandbox  GGCW cactus_v2.7.1.sif



#TODO 基于构造的Container运行GGCW pipeline流程


#? 根据A2和At跨物种的比较。对所有的windows进行拆分

