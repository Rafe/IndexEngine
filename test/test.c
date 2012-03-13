#include <stdio.h>

struct s{
	int t;
};
typedef struct s some;

int main(){

	some* c = (some*) malloc(3 * sizeof(some));
	c[0].t =12; 
	printf("%d",c[0].t);
	printf("\ntest %d\n",c[1].t);
	free(c);

}
