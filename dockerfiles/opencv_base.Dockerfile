# Loading ubuntu 
FROM ubuntu:18.04

# Cria as variaveis de ambiente para adicionar um usuario non-root (Valores padroes)
ARG username=fsalvagnini
ARG uid=1000
ENV USER $username
ENV UID $uid
ENV HOME /home/$USER
ENV PROJECT_DIR $HOME/data_augmentation

# Atualiza os pacotes e instala python e as dependências do opencv
RUN apt-get update && apt-get install -y python3-dev libglib2.0-0 libsm6 libxext6 libfontconfig1 libxrender1 nano curl \ 
        && rm -rf /var/lib/apt/lists/*

# Cria o usuario non-root
RUN adduser --disabled-password \
        --gecos "Non-root user" \
        --uid $UID \
        --home $HOME \
        $USER

# Loga com o usuario criado
USER $USER

# Copia o arquivo de requisitos para dentro da imagem 
COPY ocv_requirements.txt ${PROJECT_DIR}/ocv_requirements.txt
# Efetua o upgrade do pip e do setup_tools, também instala os pacotes python do arquivo ocv_requirements
ENV PATH="${HOME}/.local/bin:${PATH}"
RUN curl https://bootstrap.pypa.io/get-pip.py | python3 \
        && python3 -m pip install --upgrade pip setuptools \
        && python3 -m pip install -r ${PROJECT_DIR}/ocv_requirements.txt

WORKDIR ${PROJECT_DIR}