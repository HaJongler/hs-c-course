#include "acronym.h"
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

char *abbreviate(const char *phrase) {
	if (phrase == NULL || strlen(phrase) == 0) return NULL;
	int mylen = strlen(phrase);
	int index = 0;
	char *abbvs = malloc(mylen);
	char last_char = 0;
	for (int i = 0; i < mylen; i++) {
		if (i == 0 || last_char == ' ' || last_char == '-') {
			abbvs[index] = toupper(phrase[i]);
			index++;
		}
		last_char = phrase[i];
	} 
	return abbvs;
}
