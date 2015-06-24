Title: grep cut find text in a file
Date: 2011-11-12 02:37
Tags: grep, linux, bash

[TOC]

grep is an amazing tool for getting efficiently finding text

### grep parameters and examples explained

`grep -r -i -w -n -A2 -B1 'hidden' /tmp`

- search the /tmp directory and subdirectories recursively
- case insensitive
- only match the whole word, so "thidden" would not be returned as a match
- print the line number in the file where it was found
- print the two lines after the grep match
- print the one line before the grep match
- start the search in the /tmp directory


|command|notes|
|---|---|
| `grep -c 'hidden' ./myfile `| *only display the number of matches in the file* |
| `grep -r -l 'hidden' /tmp ` | *recursively search /tmp and only display the file names which contain "hidden"|
|`grep "hidden treasure" /home/ubuntu/*.txt` | *search only txt files* |
| `grep ab.d file` | *find a single character wildcard*|
| `grep "ab.*e" file`| *find a infinite repitions of a single character, word ends in e*|
| `grep "ab.*e." file` | find a infinite repitions of a single character, word ends with a single character* |
| `grep "ab[c-e]f" file `| *find with a wildcard of a subset of range of characters* |


Useful parameters:

- `-v` = invert the match so do NOT show lines that match (typically | grep -v 'myexclude')
- `-x` = whole line match only
- `-C 2` = print two lines before and two lines after a match

`grep ubuntu /etc/passwd | cut -d: -f3`
>  only print the user id by piping the match to cut which delimits by colon and outputs the 3rd column


### cut to only display a part of a path

    :::bash
    #!/bin/bash
    # iterate through the list of subdirectories
    # cut out each subdirectory name (using forward slash delimiter)
    # compare a text file within to a similarly organized TEMP directory
    
    DIRECTORY=/var/lib/tomcat6/webapps/*
    
    for dir in $DIRECTORY
    do
      if [ -d $dir ];
      then
        echo $dir
        NAME=`echo $dir | cut -d "/" -f 6 `
        diff $dir/WEB-INF/app.properties /var/lib/tomcat6/TEMP/$NAME/WEB-INF/app.properties
      fi
    done
    
### more info
- <https://en.wikipedia.org/wiki/Grep>
- <http://www.gnu.org/software/grep/manual/grep.html>
- <http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_04_02.html>
- <http://linux.die.net/man/1/cut>
