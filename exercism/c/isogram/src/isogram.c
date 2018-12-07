#include "isogram.h"
#include "string.h"
#include "stdio.h"
#include <ctype.h>


bool is_isogram(const char phrase[]) {
	if (phrase == NULL) return false;
	int counter[256] = {0};
	for (unsigned int i = 0; i < strlen(phrase); i++) {
		if (isalpha(phrase[i])) {
			counter[(int) tolower(phrase[i])]++;
			if (counter[(int) phrase[i]] == 2) {
				return false;
			}
		}
	}
	return true;
}
