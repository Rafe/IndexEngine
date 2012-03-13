#include <stdio.h>
#include <string.h>
#include "zlib.h"

#define TABLE_SIZE 50000

struct _Word {
	char *word;
	uInt count;
};
typedef struct _Word Word;

uInt getHash(char *key, size_t len) {
   uInt hash = 5831;
	 int i = 0;
   for(i = 0; i < len; ++i)
      hash = 31 * hash + key[i];
   return hash % TABLE_SIZE;
}

void resetTable(Word* words, size_t len){
	int i;
	for(i=0; i < len; i++){
		words[i].count = 0;
	}
}

int main(int argc,char* argv){
	char test[] = "abc abc abc der feg ghi dfi abc";
	Word* wordTable = (Word*) malloc(sizeof(Word) * TABLE_SIZE);
	int len = strlen(test);
	char *word;
	int i,l = 0;
	Word WordCnt;
	uInt hash = 0;

	resetTable(wordTable,TABLE_SIZE);

	word = strtok(test," ");
	while(word!=NULL){
		
		l = strlen(word);
		hash = getHash(word,l);
		if (wordTable[hash].count == 0){
			wordTable[hash].word = word;
		}
		wordTable[hash].count += 1;
		//printf(": %d , hash: %d \n", l , hash);
		word = strtok(NULL," ");

	}
	for(i = 0; i < TABLE_SIZE; i++){
		if(wordTable[i].count != 0){
			printf("%s : %d \n",wordTable[i].word,wordTable[i].count);
		}
	}
	
	free(wordTable);
}
