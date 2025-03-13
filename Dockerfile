FROM python:3.13.2
RUN apt update
RUN apt install -y wget curl bash sudo git

WORKDIR /
RUN git clone https://github.com/Jimmy2099/QuantDataHub.git
WORKDIR /QuantDataHub

#TA-Lib
RUN  wget https://github.com/TA-Lib/ta-lib/releases/download/v0.6.4/ta-lib_0.6.4_amd64.deb
RUN dpkg -i ta-lib_0.6.4_amd64.deb
RUN rm  -rf  ta-lib_0.6.4_amd64.deb
RUN pip install TA-Lib
#

#
#TODO
