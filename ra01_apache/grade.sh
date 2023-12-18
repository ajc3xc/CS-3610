#!/bin/bash

######## Variable globals -> ########
# The file containing the "main" entry point for the program.
# In C or C++, this is the file containing the main() function
# In Python, this is whichever file you run via python3 whatever.py
# In Bash, this is whichever file you run via bash whatever.sh
# In Rust, this is src/main.rs
main_file="apache_setup.sh"

# Any arguments you want passed to the main driver, upon excution.
# If you do not have any arguments, just leave as an empty string, ""
main_file_arguments=""

# The language that the assignment is written in.  Currently supported
# options are "cpp", "python", "bash", "rust"
language="bash"

# Whether or not to score the student using a static analyzer.
# For Python, this is the mypy type-checker.
# For C or C++, this is cppcheck.
# For Bash, this is shellcheck
# Not needed at all with rust's awesome compiler!
enable_static_analysis=true

# Whether or not to score the student using an autoformatter (dock points
# if not formatted correctly).
# For Python, this is black.
# For C++, this is clang-format.
# For Bash, this is shfmt
# For Rust, this is rustfmt
enable_format_check=true

# Whether or not to use fuzzy or ridig diffs
# If you choose true, fuzzy diffs will give partial credit.
# This can be helpful for string-heavy assignments,
# where correctness is reasonable to estimate statistically.
# If you choose false, rigid diffs will be all-or-none.
# This is helpful when the assignment is mathy,
# where correctness is not reasonable to estimate statistically.
fuzzy_partial_credit=true

# The timeout duration in seconds for killing a student process.
# This can limit infinite run-times.
# For computationally expensive operations, you may increase this time as desired.
process_timeout=15

# The file to which the final grade is written
# This file can be saved as as artifact in gitlb CI/CD, and used to upload scores to Canvas using assigner.
student_file="results.txt"
######## <- Variable globals ########

######## File and type existence tests -> ########
# Load the specified assosicative array with files you want to check for the existence of.
# Key is the file, and Value must be a sub-string within what is produced by the bash command:
# $ file file.whatever
declare -A file_arr
file_arr=(
    ["iactuallytestedthis-apache_setup.png"]="PNG image data"
    ["wireshark_cap_web.pcapng"]="pcapng capture file"
    ["report.md"]="ASCII text"
)
######## <- File and type existence tests ########

######## Custom tests -> ########
# Any tests other than the unit tests and the stdout diff tests belong here,
# and must be bash functions whose names begin with "custom_test".
# Custom tests should report their score by assigning their result (0-100)
# to the custom_test_score, e.g.:
# custom_test_score=100
# Custom tests are performed alphabetically,
# so number them if you want them in order.

custom_test_1_server() {
    custom_test_score=0
    rm -f your_outputs/*
    bash apache_setup.sh

    echo "================================================================================"
    echo -e "\ncurl test"
    timeout 3s curl localhost:80/hello_world.html -o your_outputs/out_curl.html &>/dev/null
    if ! diff -yZB your_outputs/out_curl.html goal_files/hello_world.html; then
        custom_test_score=0
        return
    fi

    echo "================================================================================"
    echo -e "\nwget test"
    timeout 3s wget localhost:80/dir/hello_web.html -O your_outputs/out_wget.html &>/dev/null
    if ! diff -yZB your_outputs/out_wget.html goal_files/dir/hello_web.html; then
        custom_test_score=0
        return
    fi

    echo "================================================================================"
    echo -e "\n404 test"
    timeout 3s curl localhost:80/doesnotexist.html -o your_outputs/out_404.html &>/dev/null
    head -4 your_outputs/out_404.html >your_outputs/out_4044.html
    head -4 goal_files/not_found.html >temp_not_found.html
    if diff -yZB your_outputs/out_4044.html temp_not_found.html; then
        custom_test_score=100
    else
        custom_test_score=0
    fi
    rm temp_not_found.html
}

custom_test_2_server_headers() {
    custom_test_score=0
    echo "================================================================================"
    echo -e "\nHeaders test"
    if curl -I localhost:80 | grep "Server: Apache"; then
        custom_test_score=100
    else
        custom_test_score=0
    fi
}

custom_test_3_cgi() {
    custom_test_score=0
    echo "================================================================================"
    echo -e "\ncgi python test"
    timeout 3s curl localhost:80/cgi-bin/python.py -o your_outputs/py.html &>/dev/null
    if ! diff -yZB your_outputs/py.html goal_files/py.html; then
        custom_test_score=0
        return
    fi

    echo "================================================================================"
    echo -e "\ncgi bash test"
    timeout 3s curl localhost:80/cgi-bin/bash.sh -o your_outputs/sh.html &>/dev/null
    if ! diff -yZB your_outputs/sh.html goal_files/sh.html; then
        custom_test_score=0
        return
    fi
    custom_test_score=100
}

custom_test_4_cgi_input() {
    custom_test_score=0
    echo "================================================================================"
    echo -e "\ncgi python test"
    timeout 3s curl localhost:80/cgi-bin/python_inputs.py?arg1=hi -o your_outputs/py_input1.html &>/dev/null
    if ! diff -yZB your_outputs/py_input1.html goal_files/py_input1.html; then
        custom_test_score=0
        return
    fi

    echo "================================================================================"
    echo -e "\ncgi bash test"
    timeout 3s curl localhost:80/cgi-bin/python_inputs.py?arg1=hey -o your_outputs/py_input2.html &>/dev/null
    if ! diff -yZB your_outputs/py_input2.html goal_files/py_input2.html; then
        custom_test_score=0
        return
    fi
    custom_test_score=100
}
######## <- Custom tests ########

source .admin_files/grade_backend.sh
