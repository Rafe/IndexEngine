#include <sys/time.h>
#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>


/************************************************************************/
/* makeinput.c makes a random input file for testing                    */
/*                                                                      */
/* usage:  ./makeinput recsize numrecs outfile                          */
/*             where                                                    */
/*               recsize:  size of a record in bytes - must be mult(4)  */
/*               numrecs:  number of records created                    */
/*               outfile:  name of the output file that is created      */
/************************************************************************/
int main(int argc, char* argv[])
{
  FILE *fout;
  int recSize, numRecs; 
  int i, j;
  int val;
  double range;
  double msrandom();
  int s = 123;
  int *seed = &s;

  /* initialize values */
  range = pow(2.0, 31) - 1;
  recSize = atoi(argv[1]);
  numRecs = atoi(argv[2]);
  
  fout = fopen64(argv[3], "w");
  for (i = 0; i < numRecs; i++)
    for (j = 0; j < recSize; j +=4)
    {
      val = (int) (range * msrandom(seed));
      fwrite(&val, sizeof(int), 1, fout);  
    }
  fclose(fout);
}

double msrandom(int *seed)

{
  int lo;
  int hi;
  int test;

  hi=(*seed)/127773;
  lo=(*seed) % 127773;
  test=16807*lo-2836*hi;
  if (test>0) *seed=test;
  else *seed=test+2147483647;
  return((double)(*seed)/(double)2147483647);
}

