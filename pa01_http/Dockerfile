FROM fedora:latest

RUN dnf install -y file graphviz python3-pip python3-devel gcc diffutils ncurses curl wget fish tmux python3-numpy ranger vim-X11 git
RUN pip3 install python-Levenshtein mypy black py2cfg
# RUN useradd -m student
# USER student
# WORKDIR /home/student
