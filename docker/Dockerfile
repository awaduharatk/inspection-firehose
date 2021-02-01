FROM python:3.7
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# lib
RUN apt-get install -y vim less
RUN apt-get install -y awscli

# pip
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

ADD ./docker /work
WORKDIR /work
RUN pwd
RUN pip install -r ./libList.txt


# aws configure
RUN cp -r ./aws ~/.aws

# alias
RUN echo "alias la='ls -al'" >> /root/.bashrc
RUN echo "alias ll='ls -l'" >> /root/.bashrc