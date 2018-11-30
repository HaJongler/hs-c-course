#include <stdio.h>

unsigned fac(unsigned n)
{
    if (n == 1) {
		return 1;
	}
	return n * fac(n - 1);
}

int main(int argc, char *argv[])
{
    printf("%u\n", fac(10));
    return 0;
}