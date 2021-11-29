FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04

ADD sources.list /etc/apt/

RUN apt-get update && \
    apt-get install -y --fix-missing build-essential \
        wget \
        curl \
        git \
        openssh-server \
        openjdk-8-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV HADOOP_VERSION=2.9.0
LABEL HADOOP_VERSION=2.9.0

RUN wget -qO- https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | \
    tar xz -C /usr/local && \
    mv /usr/local/hadoop-${HADOOP_VERSION} /usr/local/hadoop

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 \
    HADOOP_INSTALL=/usr/local/hadoop \
    HADOOP_VISIBLE_DEVICES=all

ENV HADOOP_HOME=${HADOOP_INSTALL} \
    HADOOP_BIN_DIR=${HADOOP_INSTALL}/bin \
    HADOOP_SBIN_DIR=${HADOOP_INSTALL}/sbin \
    HADOOP_HDFS_HOME=${HADOOP_INSTALL} \ 
    HADOOP_COMMON_LIB_NATIVE_DIR=${HADOOP_INSTALL}/lib/native \ 
    HADOOP_OPTS="-Djava.library.path=${HADOOP_INSTALL}/lib/native"

ENV PATH=/usr/local/cuda/bin:/usr/local/nvidia/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${HADOOP_SBIN_DIR}:${HADOOP_BIN_DIR}

WORKDIR /root
