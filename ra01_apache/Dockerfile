FROM fedora:latest

RUN dnf install -y file graphviz python3-pip python3-devel diffutils gcc gdb diffutils ncurses curl wget httpd ShellCheck lynx fish tmux python3-numpy ranger vim-X11 micro nano git shfmt
RUN pip3 install python-Levenshtein mypy black py2cfg pudb
# RUN wget -O shfmt https://github.com/mvdan/sh/releases/download/v3.7.0/shfmt_v3.7.0_linux_amd64
# RUN chmod +x ./shfmt
RUN fish -c "fish_add_path --prepend bin/ .local/bin/ .cargo/bin/"

# RUN useradd -m student
# USER student
# WORKDIR /home/student
