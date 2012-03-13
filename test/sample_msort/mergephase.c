#include <sys/time.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

/* data structure for one input/output buffer */
typedef struct {FILE *f; char* buf; int curRec; int numRec;} buffer;
typedef struct {int *arr; char *cache; int size; } heapStruct;
#define KEY(z) (*(int *)(&(heap.cache[heap.arr[(z)]*recSize])))

buffer *ioBufs;          /* array of structures for in/output buffers */
heapStruct heap;         /* heap structure */
int recSize;             /* size of record (in bytes) */
int bufSize;             /* # of records that fit in each buffer */ 


/*************************************************************************/
/* mergephase.c implements the merge phase of an I/O-efficient mergesort */
/*      It is assumed that the first 4 bytes of each record contain an   */
/*      integer key by which sorting occurs, and that records are of a   */
/*      fixed size that is a multiple of 4 bytes. It reads the names of  */
/*      the files that have to be merged from a file, and then merges    */
/*      each group of up to d consecutive files into one, where d is     */
/*      given as part of the command line input. Output files again have */
/*      filenames created by adding a running number to a given prefix,  */
/*      and the list of these filenames is written to another file.      */
/*                                                                       */
/* usage:  ./mergephase recsize memsize finlist outfileprefix foutlist   */
/*             where                                                     */
/*               recsize:  size of a record in bytes - must be mult(4)   */
/*               memsize:  size of available memory in bytes             */
/*               degree:   merge degree d: max # files merged into one   */
/*               finlist:  name of file containing a list of input files */
/*               outfileprefix:  prefix (including path and name) used   */
/*                               to generate numbered temp output files  */
/*               foutlist:  file to which names of temp files written    */
/*************************************************************************/
int main(int argc, char* argv[])
{
  FILE *finlist, *foutlist;  /* files with lists of in/output file names */
  int memSize;             /* available memory for merge buffers (in bytes) */
  int maxDegree, degree;   /* max allowed merge degree, and actual degree */
  int numFiles = 0;        /* # of output files that are generated */
  char *bufSpace;
  char filename[1024];
  void heapify();
  void writeRecord();
  int nextRecord();
  int i;

  recSize = atoi(argv[1]);
  memSize = atoi(argv[2]);
  bufSpace = (unsigned char *) malloc(memSize);
  maxDegree = atoi(argv[3]);
  ioBufs = (buffer *) malloc((maxDegree + 1) * sizeof(buffer));
  heap.arr = (int *) malloc((maxDegree + 1) * sizeof(int));
  heap.cache = (void *) malloc(maxDegree * recSize);
  
  finlist = fopen64(argv[4], "r");
  foutlist = fopen64(argv[6], "w");

  while (!feof(finlist))
  {
    for (degree = 0; degree < maxDegree; degree++)
    {
      fscanf(finlist, "%s", filename);
      if (feof(finlist)) break;
      ioBufs[degree].f = fopen64(filename, "r");
    }
    if (degree == 0) break;

    /* open output file (output is handled by the buffer ioBufs[degree]) */
    sprintf(filename, "%s%d", argv[5], numFiles);
    ioBufs[degree].f = fopen64(filename, "w");

    /* assign buffer space (all buffers same space) and init to empty */
    bufSize = memSize / ((degree + 1) * recSize);
    for (i = 0; i <= degree; i++)
    {
      ioBufs[i].buf = &(bufSpace[i * bufSize * recSize]);
      ioBufs[i].curRec = 0;
      ioBufs[i].numRec = 0;
    }

    /* initialize heap with first elements. Heap root is in heap[1] (not 0) */
    heap.size = degree;
    for (i = 0; i < degree; i++)  heap.arr[i+1] = nextRecord(i);
    for (i = degree; i > 0; i--)  heapify(i);

    /* now do the merge - ridiculously simple: do 2 steps until heap empty */
    while (heap.size > 0)
    {
      /* copy the record corresponding to the minimum to the output */
      writeRecord(&(ioBufs[degree]), heap.arr[1]); 

      /* replace minimum in heap by the next record from that file */
      if (nextRecord(heap.arr[1]) == -1)
        heap.arr[1] = heap.arr[heap.size--];     /* if EOF, shrink heap by 1 */
      if (heap.size > 1)  heapify(1);
    }
    
    /* flush output, add output file to list, close in/output files, and next */
    writeRecord(&(ioBufs[degree]), -1); 
    fprintf(foutlist, "%s\n", filename);
    for (i = 0; i <= degree; i++)  fclose(ioBufs[i].f);
    numFiles++;
  }

  fclose(finlist);
  fclose(foutlist);
  free(ioBufs);
  free(heap.arr);
  free(heap.cache);
}


/* standard heapify on node i. Note that minimum is node 1. */
void heapify(int i)

{ 
  int s, t;

  s = i;
  while(1)
  {
    /* find minimum key value of current node and its two children */
    if (((i<<1) <= heap.size) && (KEY(i<<1) < KEY(i)))  s = i<<1;
    if (((i<<1)+1 <= heap.size) && (KEY((i<<1)+1) < KEY(s)))  s = (i<<1)+1;

    /* if current is minimum, then done. Else swap with child and go down */
    if (s == i)  break;
    t = heap.arr[i];
    heap.arr[i] = heap.arr[s];
    heap.arr[s] = t;
    i = s;
  }
}


/* get next record from input file into heap cache; return -1 if EOF */
int nextRecord(int i)

{
  buffer *b = &(ioBufs[i]);

  /* if buffer consumed, try to refill buffer with data */
  if (b->curRec == b->numRec)
    for (b->curRec = 0, b->numRec = 0; b->numRec < bufSize; b->numRec++)
    {
      fread(&(b->buf[b->numRec*recSize]), recSize, 1, b->f);
      if (feof(b->f))  break;
    }

  /* if buffer still empty, return -1; else copy next record into heap cache */
  if (b->numRec == 0)  return(-1);
  memcpy(heap.cache+i*recSize, &(b->buf[b->curRec*recSize]), recSize);
  b->curRec++;
  return(i);
}


/* copy i-th record from heap cache to out buffer; write to disk if full */
/* If i==-1, then out buffer is just flushed to disk (must be last call) */
void writeRecord(buffer *b, int i)

{
  int j;

  /* flush buffer if needed */
  if ((i == -1) || (b->curRec == bufSize))
  { 
    for (j = 0; j < b->curRec; j++)
      fwrite(&(b->buf[j*recSize]), recSize, 1, b->f);
    b->curRec = 0;
  }

  if (i != -1)
    memcpy(&(b->buf[(b->curRec++)*recSize]), heap.cache+i*recSize, recSize);
}

