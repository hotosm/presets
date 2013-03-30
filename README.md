# Spot to store and version working versions of JOSM Humanitarian Data Model presets

See the https://github.com/hotosm/scripts for tools to help process these.

====================================
HOWTO-XMLLINT (on ubuntu)

XMLLINT will auto indent your xml files.

This is extremely useful for doing multiple line find-replace functions.

First you can find-replace all occurances of tab(\t) with nothing(blank) in the file to unindent it. 
Then you can do multiple line find-replace to add or delete code.

\n is line return
\t is tab


-----------
INSTALL XMLLINT:

sudo apt-get install libxml2-utils
-----------

XMLLINT by defualt uses to spaces(  ) to index instead of tab(\t).

----------
To change this to tab run:

gedit ~/.bashrc

once in this file add these lines onto the end of the file:

# set tab as default for xmllint --format
export XMLLINT_INDENT=$'\t'

save the file
----------

To run XMLLINT run this command

xmllint --format [FILE_NAME] > [NEW_FILE_NAME]

to not create a new file run:

xmllint --format [FILE_NAME] > temp; mv temp [FILE_NAME]
----------
Job done.
====================================
