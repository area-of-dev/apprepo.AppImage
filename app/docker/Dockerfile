# Copyright 2020 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
FROM ubuntu:22.04

ARG TOKEN
ENV TOKEN=${TOKEN}

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update --fix-missing
RUN apt-get -y install apt-utils
RUN apt-get -y upgrade

RUN apt-get install -y kmod make gcc wget gpg curl
RUN apt-get install -y rpm2cpio cpio
RUN apt-get install -y fuse file
RUN apt-get install -y python3 python3-venv python3-pip python3-apt
# RUN apt-get install -y python3-dnf 

RUN apt-get -y install apt-file
RUN apt-file update

COPY ./requirements.txt /root/requirements.txt
RUN python3 -m pip install -r /root/requirements.txt
