Title: Using find grep cut awk sort dd with files and text and listing files with ls
Date: 2011-11-12 02:37
Tags: grep, linux, bash, cut, awk, sort, dd, files, text, ls, sort by size, sort by date, exec

[TOC]

There are amazing linux command line utilities that make finding and manpiulating files very easy

## create copy truncate

Assuming you understand the basics like:

    touch example.txt
> make an empty file named file.txt

    echo "hi" >> example.txt
> append the hi content into example.txt, note that a single > will overwrite the contents

    cat example.txt | tee -a example2.txt
> - display the contents of the file to the output console and also pipe the result to the **tee** utility which appends it to another file - tee is better than >> 
> - except that tee always returns 0 so if you have set -e then prefer >

    :> example.txt
> truncate the file without disturbing any existing readers of that file (e.g. zero a log without messing up an applications ability to write to the file)

    cp -a example.txt example2.txt
> copy archive which preserves timestamp (but will also overwrite the target - in this example probably zero bytes)

    rm example.txt
> remove a file, -f forces removal without a prompt, -rf to recursively force remove a file or directory **be careful**

## ls lists files in a directory

    ls /etc
> list the files and directories in the /etc directory

    ls -1
> lists just the names (not including hidden .dot files or directories) in the current directory

    ls -1a
> lists just the names including hidden .dot files

    ls -ahl | grep -v IGNORETHIS
> exclude lines that match IGNORETHIS

    ls -f
> unsorted list of files which is the only way to work with directories with a very large number of files

### list directories

    ls -d */
> list names of directories in the current directory

    ls -1 -d */
> using a "numeral one" parameter lists one directory name per line

    ls -l -d */
> using a "lowercase letter L" parameter lists the extended information (permissions, owner, timestamps)

    ls -d ./*/
> list names of directories in the current directory

    echo */
> lists the names of directories in the current directory

    find -type d
> find recursively starting from the current directory and display the relative path all objects of type directory

    find /tmp -maxdepth 1 -type d
> find all directories in /tmp up to 1 level deep (/tmp/foo)

    find /tmp -maxdepth 2 -type d
> find all directories in /tmp up to 2 levels deep (/tmp/foo/bar)

### counting the listings

    ls -1 | wc
> lists just the names of non hidden files piped to word count, number one looks a lot like lowercase L (sadindeed)

    ls -1 | wc -l
> list just names and count only the lines (number one, then lowercase L)

    ls -ahl | wc -l
> counting hidden files BUT directories too

    for file in /PATH/foo*; do cp "$file" /mnt/BAR/; done
> when there are too many files in a directory: "/bin/cp: Argument list too long"
> a one liner for copying each file as a parameter

### sorting by size or timestamp

    ls -Sla
> sort by size (largest to smallest with full details displayed, show . hidden files too)

    ls -Slar
> sort by size (reversed, so smallest to largest with full details displayed, show . hidden files too)

    ls -Slarh
> sort by size (reversed, so smallest to largest with full details displayed, show . hidden files too, human sizes like MB)

    ls -ahtlr
> sort by timestamp (reversed so oldest first, show . hidden files too, human sizes like MB)


    ls -ahtlr | head -n3
> only the 3 oldest lines

    ls -la --time-style=full-iso foobar.txt
> list the full modified timestamp
<https://www.gnu.org/software/coreutils/manual/html_node/Formatting-file-timestamps.html>

## find

find is better than locate because locate depends on a cron job to index the file system and so may miss recent results

### find to list files

    find -type f
> find and display the relative path all objects of type file

    find /tmp -maxdepth 1 -type f -print | wc -l
> wc = count lines = files in the /tmp directory

    find -type f -print | wc -l
> to get all subdirs too

### find a specific file or types of files

    find -name "MyCProgram.c"
> case sensitive, starts in the current directory 

    find startdirectory -name 'partoffileordirname'
> e.g. find /home/joe -name '.tx'
> which would return txt's as well as txv?'s

    find / -iname "MyCProgram.c"
> case insensitive, starts from root 

    find -maxdepth 1 -not -iname "MyCProgram.c"
> case insensitive, starts from current directory, will search subdirectory(ies) and list all items //that do NOT match the query

    find . -type f -exec ls -s {} \; | sort -n -r | head -5
> the largest 5 files

    find . -not -empty -type f -exec ls -s {} \; | sort -n | head -5
> the smallest not empty 5 files 

    find . -type d
> all directories in the current directory

    find . -type f | wc
> count the number of files (can recurse subdirectories)

    find . -type f -iname '*.pyc' -exec mv {} /tmp/PYC/ \;
> move all .pyc files (start from this directory and indefinitely recurse down)

    find . -name "*api*" -exec cat {} \;
> find everything containing api and cat it

    find . -type f -iname '*.yaml' -exec grep --line-number --with-file 'needle' {} \;
> search the contents of a specific file extension and output the filename and line number of each match

### find and exec to modify a set of files

    find . -type f -name "*api*" -exec cat {} \; | grep objectid
> find all files that contain an api and output the contents but filter to only display lines that contain "objectid"

    find . -maxdepth 1 -type d -exec du -sh {} \;
> only one level down if it's a directory show the disk usage summary (human sizes)

    find DIR1 DIR2 -maxdepth 1 -type f -exec basename {} \; | sort | uniq -d
> lists all file names in directories, sorted, show only repeats (aka duplicates)

    find . -name '*.txt' -exec sh -c 'mv "$0" "${0%.txt}.java"' {} \;
> find all .txt files and renames them to .java

    for f in ; do mv "$f" "$(echo $f | sed 's/-/\ /g')"; done find . -type f -iname ".py" | rename s/.py/.py.txt/ .py {} \;
> only works on the current directory (no recursion?)

    find . -type f -iname '.py' | while read filename; do mv -v "${filename}" "echo "${filename}" | sed -e 's/\.py$/\.py.txt/'"; done
> a lot of extra work to achieve a recursive rename from .py to .py.txt

    find . -type f -iname "*.java" -exec grep -Hni "case-insensitive-text" {} \;
> find java files and return if they contain some text

    find . -type f -iname "*.java" -exec grep -Hn "fileSizeInMB < 100" {} \;
> find java files and return if they contain some case sensitive text
    
    find . -type d -name directoryname* -exec ls -ahl {} \;
> find case insensitive directories beginning with "directoryname" and list their contents
    
    sudo find /var/www/java -type f -iname ".txt" -exec chown root:www-data {} \;
> find case insensitive files ending with ".txt" and change their owner to root and group to  www-data

    sudo find /var/www/java -type f -iname "*.txt" -exec chmod 640 {} \; 
> find case insensitive files ending with ".txt" and change their permissions to 640

    sudo find /var/www/d -type d -iname "web*" -exec chmod 750 {} \;
> find case insensitive directories beginning with "web" and change their permissions to 750
    
    find . -type f -iname "*.sh" -exec mv {} . ";" 
> find files ending in .sh and move them into the current directory
    
    find /dir/dir -type f -mtime +540 -mtime -720 -printf \%p\,\%s\,\%AD\,|%TD\\n > /dir/dir/output.csv
    
    find ~ -empty //check the home directory for empty files (size 0)
    
    
    find / -mindepth 3 -maxdepth 5 -iname passwd
> case insensitive, starts from root, will search subdirectory levels between 2 and 4
    
    find / 3 -maxdepth 5 -iname passwd &
> case insensitive, starts from root, will search at most 4 subdir levels, will start in background 
> note that you'll have to press enter once as the text results will scroll to interrupt your 
> bash session ... once the job's done pressing enter will return you to the prompt


     find -iname "MyCProgram.c" -exec md5sum {} \;
> interesting use: creating a md5sum of all of the results

    find -inum 16187430 -exec mv {} new-test-file-name \;
> interesting - find a file by inode number (ls -i) and then rename/move it

    find / -perm 700 -type f
> find all files from root below, with permissions set exactly to 700, only regular files (-type f)

    find / -perm 700 -type f -exec ls -l {} \;
> while the above just lists the files the below runs an ls -l to see everything about them...


RUN "man find" IF YOU NEED TO FIND SOMETHING SPECIFIC ABOUT FILES AND PERMISSIONS


> any files newer than the one given find -newer file-i-made-yesterday

search the home directory size equal to 100 MB, use +100MB for greater than and -100MB for less than find ~ -size 100M

<http://www.thegeekstuff.com/2009/03/15-practical-linux-find-command-examples/>

### find files by modified time

There is an implied AND operator with find but for OR or NOT...

    find / -mmin -10
> something modified 10 minutes ago

    find . -mtime 1 
> find files modified between 24 and 48 hours ago 

    find . -mtime +1 
> find files modified more than 48 hours ago

    find . -mmin +5 -mmin -10
> find files modifed between # 6 and 9 minutes ago


    find / -type f -mtime -7 | xargs tar -rf weekly_incremental.tar
> find files modified in the last 7 days and create a .tar file from them

    find / -name core -delete
> same if using Gnu find


    find / -user username
> find all of the files a user owns..


    -mtime +60 means you are looking for a file modified 60 days ago. -mtime -60 means less than 60 days. -mtime 60 If you skip + or - it means exactly 60 days.

    find / -mtime 9 -mtime -10
> 24 hours



## grep
grep is an amazing tool for getting efficiently finding text, <http://www.gnu.org/software/grep/manual/grep.html>

### grep parameters and examples explained

    cat access.log | grep -v "bingbot"
> exclude from output lines that match bingbot

    grep -r -i -w -n -A2 -B1 'hidden' /tmp

- search the /tmp directory and subdirectories recursively
- case insensitive
- only match the whole word, so "thidden" would not be returned as a match
- print the line number in the file where it was found
- print the two lines after the grep match
- print the one line before the grep match
- start the search in the /tmp directory


| command | notes |
|---|---|
| `grep -c 'hidden' ./myfile `| *only display the number of matches in the file* |
| `grep -r -l 'hidden' /tmp ` | *recursively search /tmp and only display the file names which contain "hidden"*|
|`grep "hidden treasure" /home/ubuntu/*.txt` | *search only txt files* |
| `grep ab.d file` | *find a single character wildcard*|
| `grep "ab.*e" file`| *find a infinite repitions of a single character, word ends in e*|
| `grep "ab.*e." file` | *find a infinite repitions of a single character, word ends with a single character* |
| `grep "ab[c-e]f" file `| *find with a wildcard of a subset of range of characters* |


#### Useful parameters for grep

- `-v` = invert the match so do NOT show lines that match (typically | grep -v 'myexclude')
- `-x` = whole line match only
- `-C 2` = print two lines before and two lines after a match

    grep ubuntu /etc/passwd | cut -d: -f3
>  only print the user id by piping the match to cut which delimits by colon and outputs the 3rd column

    ls -t -d -1 -r path/directory/ >> oldest.m3u
> list reverse order by timestamp
    ls -t -d -1 path/directory/ | grep -v DONOTLIKE >> newest.m3u
> list by timestamp (sort by modification time, newest first), list directories themselves, not their contents, only 1 level deep
> pipe to grep and ignore matches of DONOTLIKE, then append output to the newest.m3u file

#### grep files without match

    grep -L 'foobar' *
> --files-without-match , display filenames that do not contain the string foobar

- <https://en.wikipedia.org/wiki/Grep>
- <http://www.gnu.org/software/grep/manual/grep.html>
- <http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_04_02.html>


## cut

    ps auxwwww | grep someappname | tr -s [:space:] | cut -d\  -f11-
> filter to only view someappname from all processes (wide) THEN shorten all whitespace to a single space THEN cut delimited by a single space (escaped by the slash) and then only prints all after the 11th field/column

    cat sometext.txt | cut -f1 -d"["
> delimiter of square bracket , only take after the first "field" token, so essentially print everything after the first occurence of a left square bracket

- <http://ss64.com/bash/cut.html>
- <http://linux.die.net/man/1/cut>


### cut to only display a part of a path

    :::bash
    #!/bin/bash
    # iterate through the list of subdirectories
    # cut out each subdirectory name (using forward slash delimiter)
    # compare a text file within to a similarly organized TEMP directory
    
    DIRECTORY=/var/lib/tomcat6/webapps/*
    
    for dir in $DIRECTORY
    do
      if [ -d $dir ]; then
        echo $dir
        NAME=`echo $dir | cut -d "/" -f 6 `
        diff $dir/WEB-INF/app.properties /var/lib/tomcat6/TEMP/$NAME/WEB-INF/app.properties
      fi
    done

## awk

awk to parse columns of data , some overlap with cut

    awk -F"," '{ print $2 }' results.txt
> csv parsing , set the delimiter to a comma and print the second column

    awk '{$1=""; print $0}' results.txt
> assuming space delimited and remove the first column but print all else in results.txt

    ps aux | grep someappname | awk '{$1=$2=$3=$4=$5=$6=$7=$8=$9=$10=""; print $0}'
> print everything after the nth (10th) column

    cat sometext.txt | cut -f1 -d"("
> using cut can be more effective: deleting everything after the first occurence of a left parenthesis

    grep -r 'beta/dists/precise/main/binary-amd64' | grep -v 1.2.3.4 | grep -v AccessDenied | awk '{print $5}' | sort -u

    grep --exclude-dir=.git -r 'foo' .  # recursively search this directory for foo but ignore the .git directory

> recursive search for a string, pipe the output to exclude lines that contain IP 1.2.3.4 , pipe to exclude AccessDenied, print the 5th column, sort for uniqueness

If the 5th column of results.txt contains numbers then ...

    cat results.txt | awk '{total = total + $5} END{print total}'
    
    ls -tahl | awk '{print $5,$6,$7,$8}'
    
    awk <search pattern> {<program actions>}
    
    1.5K 2009-07-14 12:14 backupCHECKUP.sh
    5.2K 2009-07-14 12:03 email-backup.txt
    4.0K 2009-07-14 10:06 .
    330 2009-07-14 09:55 test.sh
    253 2009-07-14 08:54 daily-backup-projects.sh
    4.0K 2009-07-12 11:09 ..
    3.9K 2009-03-18 16:01 mtrac.ini
    5.0K 2008-11-25 11:50 CreateProject.sh
    
    awk '/2009/ {print $5,$6,$7,$8}' ls_output.txt

> Note that Awk recognizes the field variable $0 as representing the entire line, so this could also be written as:
    awk '/gold/ {print $0}'

- <http://www.grymoire.com/Unix/Awk.html>
- <https://www.gnu.org/software/gawk/manual/gawk.html>

## sed

sed does string substitution

    sed regular expression 's=start/olditem/newitem/g=end' filename

    sed -e 's/ /\t /g' email-backup.txt
> replace a space with a tab

    sed -i 's/\x85/.../g' *.md
> replace a UTF-8 character (in this case the single character horizontal ellipsis) with three dots

    cat /var/www/html/themes/bartik/css/style.css | tr '\n' '\r' | sed -e 's/#site-slogan {\r  font-size: 0.929em/#site-slogan {\r  font-size: 2.929em/' | tr '\r' '\n' > /var/www/html/themes/bartik/css/style.css.updated
> replace multiline with a newline using tr to translate \n to \r

REMEMBER

    \t = tab
    \n = newline
    \r = carriage return

    sed -e 's/$/\r/' inputfile > outputfile                # UNIX to DOS  (adding CRs)
    sed -e 's/\r$//' inputfile > outputfile                # DOS  to UNIX (removing CRs)
    perl -pe 's/\r\n|\n|\r/\r\n/g' inputfile > outputfile  # Convert to DOS
    perl -pe 's/\r\n|\n|\r/\n/g'   inputfile > outputfile  # Convert to UNIX
    perl -pe 's/\r\n|\n|\r/\r/g'   inputfile > outputfile  # Convert to old Mac

- <http://www.grymoire.com/Unix/Sed.html>
- <https://www.gnu.org/software/sed/manual/sed.txt>

## dd

dd can delete things very quickly (dangerous!)

But a useful tool for testing upload limits or compression or any other miscellaneous file tasks is to generate a file of a specified length:

    dd if=/dev/zero of=a.log bs=1M count=2        
> zero filled 2MB file

    dd if=/dev/urandom of=random.txt bs=1M count=2
> random contents 2MB file

    hexdump random.txt | head

Notes about randomness (on linux):

    /dev/urandom 
> semi-random data generated by a PRNG which is fed by the trickle of real entropy from `/dev/random` (which blocks until the entropy pool has some randomness)

    watch -n 0 'cat /proc/sys/kernel/random/entropy_avail'

    cat /dev/random > /dev/null
> Drain the entropy from your system

    cpuid | grep -i rand
> Look for RDRAND <http://en.wikipedia.org/wiki/RdRand>

    cat /dev/urandom | rngtest -c 1000
> how good is your non blocking urandom?

- <https://en.wikipedia.org/wiki//dev/random>
- <http://linuxcommand.org/man_pages/rngtest1.html>
    

