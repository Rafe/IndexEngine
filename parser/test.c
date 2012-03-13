#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "parser.h"

void usage()
{
	printf("usage: test sample.html\n");
	exit(1);
}

int main(int argc, char* argv[])
{
	char *page;
	char *pool;
	FILE *fd;
	int len;
	int ret;
	char url[] = "http://cis.poly.edu/cs912/";

	if (argc != 2)
		usage();

	fd = fopen(argv[1], "r");
	if (fd == NULL)
	{
		printf("%s can not be opened!\n", argv[1]);
		exit(1);
	}

	fseek(fd, 0, SEEK_END);
	len = ftell(fd);
	fseek(fd, 0, SEEK_SET);

	page = (char*)malloc(len);
	fread(page, 1, len, fd);
	fclose(fd);
	pool = (char*)malloc(2*len+1);

	// parsing page
	ret = parser(url, page, pool, 2*len+1);

	// output words and their contexts
	if (ret > 0)
		printf("%s", pool);

	free(pool);
	free(page);
}
