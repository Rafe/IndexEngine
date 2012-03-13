
This directory contains a simple example implementation of an I/O-efficient
mergesort in C. It consists of the following files:

 - sortphase.c  implements the first phase, where chunks of the input are
                read into main memory, and then output in sorted form to disk

 - mergephase.c implements the merge of several sorted files

 - makeinput.c  allows you to make some random input for testing

 - checkoutput.c  allows you to check if the result is sorted

NOTE: this is fairly simple code to demonstrate the algorithm. It is not
super-efficient, but reasonably fast. It has only been tested (very lightly)
under Linux, and is for illustration rather than use. It assumes that each 
record to be sorted is of a fixed size S that is a multiple of 4 bytes, and 
that the first 4 bytes of the record are an integer key that we need to 
sort by.

COMPILE:

  gcc -O2 -o sortphase sortphase.c
  gcc -O2 -o mergephase mergephase.c
  gcc -O2 -lm -o makeinput makeinput.c
  gcc -O2 -o checkoutput checkoutput.c

TO RUN THE CODE:

For example, to sort 100 million records of size 8 byte each (800MB total):

(1) First, run  
       makeinput 8 100000000 data"  
    to create a file "data" with 100 million random records of size 8 bytes

(2) Next, if you have up to 20 MB of main memory available for sorting, run 
       sortphase 8 20000000 data temp list
    This will create 40 sorted files of size 20MB each, called temp0, temp1,
    ... temp39. The list of generated files is also written to file "list"

(3) To merge the 40 files in one phase, assuming you have again 20MB of main
    memory available, type
       mergephase 8 20000000 40 list result list2
    This will merge the 40 files listed in "list", merge them into one
    result file called "result0", and write the filename "result0" into file
    "list2".

    To first do an 5-way merge, followed by an 8-way merge, type
       mergephase 8 20000000 5 list temptemp list2
    which merges any 5 consecutive files in list into one (with resulting
    files temptemp0 to temptemp7 listed in "list2"), and then type
       mergephase 8 20000000 8 list2 result list3
    to get a sorted result in file "result0" (file "list3" will contain the
    name of the single output file "result0"). Note that the output files of 
    each phase must have different names than the input files, so you cannot
    directly overwrite the input files (i.e., the temp or list files)

(4) If you need to check correctness, type
       checkoutput 8 result0       

This is sloppy code but might sort of work. Send corrections to suel@poly.edu

