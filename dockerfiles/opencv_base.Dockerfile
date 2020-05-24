# Loading ubuntu 
FROM ubuntu:18.04

# Create the environments variable to add a non-root user
ARG username=fsalvagnini
ARG uid=1000
ENV USER $username
ENV UID $uid
ENV HOME /home/$USER
ENV PROJECT_DIR $HOME/data_augmentation

# Atualiza os pacotes e instala python e as dependências do opencv
RUN apt-get update && apt-get install -y python3-dev libglib2.0-0 libsm6 libxext6 libfontconfig1 libxrender1 nano curl \ 
        && rm -rf /var/lib/apt/lists/*
# Create a non-root user
RUN adduser --disabled-password \
        --gecos "Non-root user" \
        --uid $UID \
        --home $HOME \
        $USER

# Switch to fsalvagnini user
USER $USER

# Copia o arquivo de requisitos para dentro da imagem 
COPY ocv_requirements.txt ${PROJECT_DIR}/ocv_requirements.txt
# Efetua o upgrade do pip e do setup_tools, também instala os pacotes python do arquivo ocv_requirements
ENV PATH="${HOME}/.local/bin:${PATH}"
RUN curl https://bootstrap.pypa.io/get-pip.py | python3 \
        && python3 -m pip install --upgrade pip setuptools \
        && python3 -m pip install -r ${PROJECT_DIR}/ocv_requirements.txt

WORKDIR ${PROJECT_DIR}

# # Installing anaconda (Explicar b e p)
# #Installs Anaconda3 2020.02
# # -b           run install in batch mode (without manual intervention),
# #              it is expected the license terms are agreed upon
# # -f           no error if install prefix already exists
# # -h           print this help message and exit
# # -p PREFIX    install prefix, defaults to $PREFIX, must not contain spaces.
# # -s           skip running pre/post-link/install scripts
# # -u           update an existing installation
# # -t           run package tests after installation (may install conda-build)

# ENV CONDA_DIR $HOME/anaconda
# ENV PROJECT_DIR $HOME/data_augmentation
# RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh -O ~/conda_install.sh \
#         && chmod +x ~/conda_install.sh && ~/conda_install.sh -b -p $CONDA_DIR \
#         && rm ~/conda_install.sh && mkdir $PROJECT_DIR
# COPY environment.yml $PROJECT_DIR/environment.yml
# COPY ocv_test.jpg $PROJECT_DIR/ocv_test.jpg

# # Adiciona os comandos conda ao PATH
# ENV PATH=$CONDA_DIR/bin:$PATH
# # make conda activate command available from /bin/bash --login shells
# RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile
# # make conda activate command available from /bin/bash --interative shells
# RUN conda init bash

# # Cria o ambiente conda
# RUN conda update --name base --channel defaults conda \
#         && conda activate base \
#         && conda install -c conda-forge jupyterlab \
#         && conda deactivate \
#         && conda env create --prefix $PROJECT_DIR -f $PROJECT_DIR/environment.yml \
#         && conda clean --all --yes

# USER root



# USER $USER

# EXPOSE 8888

# CMD [ "jupyter-lab", "--no-browser", "--ip", "0.0.0.0" ]