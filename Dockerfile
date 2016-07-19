FROM python:2.7.11

RUN apt-get update && apt-get install -y \
        wget curl git vim tig screen tree \
        cmake

RUN useradd --uid 1000 -d /opt/bitwrap bitwrap

WORKDIR /opt/
RUN git clone --depth=1 -b maint/v0.24 https://github.com/libgit2/libgit2.git

RUN mkdir /opt/libgit2/build
WORKDIR /opt/libgit2/build

RUN cmake .. -DCMAKE_INSTALL_PREFIX=../_install -DBUILD_CLAR=OFF
RUN cmake --build . --target install

ENV LIBGIT2=/opt/libgit2/_install/ LD_LIBRARY_PATH=/opt/libgit2/_install/lib

RUN mkdir /opt/app /repo

ENV PROJECT_VERSION=0.0.3

COPY requirements.txt /opt/app/

COPY . /opt/app/
WORKDIR /opt/app

RUN pip install -r requirements.txt 
RUN chown bitwrap:bitwrap /opt/app /repo

USER bitwrap

EXPOSE 8080
VOLUME ["/repo"]

ENV BITWRAP_REPO_PATH=/repo/

ENTRYPOINT ["/opt/app/entry.sh"]
