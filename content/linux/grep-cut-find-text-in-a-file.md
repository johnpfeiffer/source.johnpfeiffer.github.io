Title: grep cut find text in a file
Date: 2011-11-12 02:37
Tags: grep, linux, bash

[TOC]

grep is an amazing tool for getting efficiently finding text

|command|notes|
|---|---|
|`grep "hidden treasure" /home/ubuntu/*.txt` | *search only txt files* |
|`grep -r "hidden treasure" /home/ubuntu` | *recursive search* |
|`grep -H -r "hidden treasure" /home/ubuntu`| *only print the filenames + search text of matches*|
|`grep -H treasure /etc/* -R <code>&#124;</code> cut -d: -f1`| *only print the filename of matches by piping to cut*|
|`grep -Hir "hidden treasure" .` | *case insensitive search the current directory*|
| `grep ab.d file` | *find a single character wildcard*|
| `grep "ab.*e" file`| *find a infinite repitions of a single character, word ends in e*|
| `grep "ab.*e." file` | find a infinite repitions of a single character, word ends with a single character* |
| `grep "ab[c-e]f" file `| *find with a wildcard of a subset of range of characters* |
| `grep -i "IpAddress=" app.properties &#124; cut -f 2 -d "=" `| * after grep use cut to further parse the text* |


Useful parameters:
- `-n` = line number
- `-v` = invert the match so do NOT show lines that match (typically grep

### cut to only display a part of a path

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
        NAME=`echo $dir | cut -f 6 -d "/"`
        diff $dir/WEB-INF/app.properties /var/lib/tomcat6/TEMP/$NAME/WEB-INF/app.properties
      fi
    
    done
    
### more info
- <https://en.wikipedia.org/wiki/Grep>
- <http://www.gnu.org/savannah-checkouts/gnu/grep/manual/grep.html>
- <http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_04_02.html>
