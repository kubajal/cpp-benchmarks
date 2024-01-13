FROM almalinux:8

RUN dnf -y update && dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm

RUN dnf -y install \
        cmake \
        gcc-toolset-12 \
        git \
        python3.11 \
        python3.11-pip \
        vim \
	ccache && \
    dnf clean all


RUN alternatives --set python /usr/bin/python3.11

RUN python -m pip install cpplint

RUN echo "source scl_source enable gcc-toolset-12" >> /root/.bashrc

WORKDIR /app
