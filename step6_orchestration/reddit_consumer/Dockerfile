FROM continuumio/miniconda3
ENTRYPOINT [ "/bin/bash", "-c" ]
RUN conda update -n base -c defaults conda
RUN conda init bash
WORKDIR /app
COPY conda_env.yml environment.yml
RUN conda env create -f environment.yml
RUN echo "conda activate app" > ~/.bashrc
ENV PATH /opt/conda/envs/app/bin:$PATH
RUN conda list --explicit > env-spec-file.txt
COPY . /app
RUN pip install .
CMD ["reddit_consumer stdout"]