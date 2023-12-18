FROM fedora:latest

RUN dnf install -y ShellCheck bat cargo cgdb clang-tools-extra cmake cppcheck curl diffutils file fish gcc gcc-g++ gcovr gdb git gnupg2 graphviz httpd ltrace lynx make mc micro mtr nano nasm nc ncurses nmap octave pandoc poetry python3-black python3-devel python3-docopt python3-numpy python3-pip python3-scikit* ranger rr rust-debugger-common rust-doc rust-gdb rust-lldb rust-src rustfmt shfmt strace tmux traceroute valgrind vim vim-X11 vim-enhanced vim-filesystem vim-fugitive vim-jedi vis wget whois zsh
RUN pip3 install --upgrade python-Levenshtein mypy black py2cfg pudb assigner mujoco
RUN fish -c "fish_add_path --prepend bin/ .local/bin/ .cargo/bin/"
RUN wget https://github.com/nushell/nushell/releases/download/0.87.1/nu-0.87.1-x86_64-unknown-linux-gnu.tar.gz
RUN tar -xf nu-0.87.1-x86_64-unknown-linux-gnu.tar.gz
RUN mv nu-0.87.1-x86_64-unknown-linux-gnu/nu bin/nu
RUN rm -rf nu-0.87.1-x86_64-unknown-linux-gnu*
