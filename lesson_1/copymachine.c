#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    FILE *f, *g;
    char fp[256] = {};
	char gp[256] = {};
    char buf[1024];

    printf("Enter file name to copy: ");
    scanf("%255s", fp);

    f = fopen(fp, "r");
    while(!feof(f)) {
        memset(buf, 0, 1024);
        fread(buf, 1, 1024, f);
    }
    fclose(f);
	
	printf("Enter new file name: ");
    scanf("%255s", gp);

	g = fopen(gp, "w");
	fprintf(g, buf);
	fclose(g);
    return 0;
}