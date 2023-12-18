#!/bin/bash

######## Variable globals -> ########
# The file containing the "main" entry point for the program.
# In C or C++, this is the file containing the main() function
# In Python, this is whichever file you run via python3 whatever.py
# In Bash, this is whichever file you run via bash whatever.sh
# In Rust, this is src/main.rs
main_file="icmp_ping_client_scapy.py"

# Any arguments you want passed to the main driver, upon excution.
# If you do not have any arguments, just leave as an empty string, ""
main_file_arguments=""

# The language that the assignment is written in.  Currently supported
# options are "cpp", "python", "bash", "rust"
language="python"

# Whether or not to score the student using a static analyzer.
# For Python, this is the mypy type-checker.
# For C or C++, this is cppcheck.
# For Bash, this is shellcheck
# Not needed at all with rust?
enable_static_analysis=false

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
    ["iactuallytestedthis-icmp_ping_scapy.png"]="PNG image data"
    ["iactuallytestedthis-icmp_traceroute_scapy.png"]="PNG image data"
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

custom_test_1() {
    # check content of ping output; timing agnostic
    custom_test_score=0
    rm -f custom_tests/outputs/*.out
    if [[ "$IS_IN_DOCKER" ]]; then
        python3 icmp_ping_client_scapy.py localhost 12 2 >custom_tests/outputs/t1.out
    else
        sudo python3 icmp_ping_client_scapy.py localhost 12 2 >custom_tests/outputs/t1.out
    fi
    if ! diff -yZB --width=160 <(cut -d = -f1,2 custom_tests/outputs/t1.out | head -n -2) <(cut -d = -f1,2 custom_tests/goals/t1.out | head -n -2); then
        custom_test_score=0
        return
    fi
    custom_test_score=100
}

custom_test_1_2() {
    # check the format of ping output
    custom_test_score=0

    match=1
    inner_pattern='^[0-9]+ bytes from .+ \(.+\): ping_seq=[0-9]+ time=[0-9]+ ms$'
    while read -r line; do
        if ! [[ "$line" =~ $inner_pattern ]]; then
            match=0
            echo "regex failed to match for: \"$line\""
        fi
    done < <(tail -n +2 custom_tests/outputs/t1.out | head -n -4)

    num='[0-9]+\.[0-9]{3}'
    secondlast_pattern="12 packets transmitted, 12 received, 0.000% packet loss, time ${num}ms$"
    if ! [[ "$(tail -n -2 custom_tests/outputs/t1.out | head -n -1)" =~ $secondlast_pattern ]]; then
        echo "Regex failed to match \"$(tail -n -2 custom_tests/outputs/t1.out | head -n -1)\""
        match=0
    fi

    last_pattern="^rtt min/avg/max/mdev = ${num}/${num}/${num}/${num} ms$"
    if ! [[ "$(tail -n -1 custom_tests/outputs/t1.out)" =~ $last_pattern ]]; then
        echo "Regex failed to match \"$(tail -n -1 custom_tests/outputs/t1.out)\""
        match=0
    fi

    if (( match == 1 )); then
        custom_test_score=100
    fi
}

custom_test_2() {
    # check traceroute content -- if you are consistently failing this test but you are sure your
    # traceroute is right, try increaseing the max ttl
    custom_test_score=0
    if [[ "$IS_IN_DOCKER" ]]; then
        python3 icmp_traceroute_client_scapy.py bad.horse >custom_tests/outputs/t2.out
    else
        sudo python3 icmp_traceroute_client_scapy.py bad.horse >custom_tests/outputs/t2.out
    fi

    matches=0
    last_line_number=0
    in_order=1
    while read -r line; do
        grep_result=$( grep --color=auto -n "$line" custom_tests/outputs/t2.out )
        grep_code=$?

        line_number=$( echo "$grep_result" | cut --delimiter=":" --field=1 )

        if (( $grep_code == 0 )) ; then
            matches=$(( $matches + 1 ))
            if (( $line_number <= $last_line_number )); then
                in_order=0
                echo "OUT OF ORDER at $grep_result"
            else
                echo "$grep_result"
            fi
            last_line_number=$line_number
        fi
    done < custom_tests/goals/t2_goal_trace.out

    if (( $matches > 15 && in_order == 1 )); then
        custom_test_score=100
    fi
}

custom_test_2_2() {
    # tests the formatting of traceroute's output
    custom_test_score=0

    ipv4='([0-9]{1,3}\.){3}[0-9]{1,3}'
    num='[0-9]+\.[0-9]{3}'
    pattern="[0-9]+( +(\*|(.+)) \(${ipv4}\))?( +((${num} ms)|\*)){2,3}"

    match=1
    lines_exist=0
    while read -r line; do
        lines_exist=1
        if ! [[ "$line" =~ $pattern ]]; then
            match=0
            echo "\"$line\" did not match the regex"
        fi
    done < <(tail -n +2 custom_tests/outputs/t2.out)

    if (( match == 1 && lines_exist == 1 )); then
        custom_test_score=100
    fi
}
######## <- Custom tests ########

source .admin_files/grade_backend.sh
