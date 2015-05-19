Title: Can't delete FTP folder in Drupal - Filezilla hidden files
Date: 2010-07-13 18:30
Tags: drupal, filezilla

I couldn't delete a folder in FTP (which can be pretty frustrating) until I realized that Filezilla (my FTP/SFTP application with UI of choice) has an option to "force showing hidden files"

In Filezilla 3 = Server -> Force showing hidden files

I could then see the .htaccess file and delete it.

(Right click on a folder/file and File Attributes shows me the permissions e.g. Read / Write / Execute)...

