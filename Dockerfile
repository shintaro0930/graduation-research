ARG nvidia_cuda_version=11.4.0-cudnn8-devel-ubuntu20.04

FROM nvidia/cuda:${nvidia_cuda_version}

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y git && \
    apt-get install -y tree && \
    apt-get install -y screen && \
    apt-get install -y mecab && \
    apt-get install -y mecab-ipadic-utf8 && \
    apt-get install -y libmecab-dev && \
    apt-get install -y swig && \
    apt-get install -y curl

RUN pip3 install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

RUN pip3 install --upgrade pip && \
    pip3 install requests && \
    pip3 install MeCab-python3  && \
    pip3 install transformers && \
    pip3 install transformers[ja]