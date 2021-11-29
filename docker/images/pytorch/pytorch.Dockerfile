#cuda9.0 python3.5
#pytorch
FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04

ADD sources.list /etc/apt/

RUN apt-get update && \
    apt-get install -y --fix-missing build-essential \
        wget \
        curl \
        git \
        openssh-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-4.1.11-Linux-x86_64.sh && \
    /bin/bash Miniconda3-4.1.11-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-4.1.11-Linux-x86_64.sh 

ENV PATH=/opt/conda/bin:/usr/local/cuda/bin:/usr/local/nvidia/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple torch torchvision tqdm opencv-python

WORKDIR /root
