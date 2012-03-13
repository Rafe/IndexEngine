CC = gcc
CFLAGS = -O2 -g

test: test.c parser.o
	$(CC) $(CFLAGS) -o test test.c parser.o

parser.o: parser.c
	$(CC) $(CFLAGS) -c parser.c

cleanup:
	rm -f *.o
	rm -f test
