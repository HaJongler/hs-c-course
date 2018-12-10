#include "word_count.h"
#include <string.h>
#include <stdio.h>
#include <ctype.h>

int word_count(const char *input_text, word_count_word_t * words) {
	memset(words, 0, sizeof *words);
	char word[MAX_WORD_LENGTH + 1] = {0};
	int j = 0;
	for (unsigned int i = 0; i < strlen(input_text); i++) {
		if (isalpha(input_text[i]) || isdigit(input_text[i]) || input_text[i] == '\'') {
			word[j] = tolower(input_text[i]);
			j++;
		}
		else {
			j = 0;
			for (int k = 0; k < MAX_WORDS; k++) {
				if ( strcmp(words[k].text, word) == 0 ) {
					words[k].count++;
				}
				else { 
					if ( strlen(words[k].text) == 0 ) {
						strncpy(words[k].text, word,strlen(word));
						words[k].count = 1;
						break;
					}
				}
			}
			memset(word, 0, sizeof word);
		}
	}
	for (int k = 0; k < MAX_WORDS; k++) {
                                if ( strcmp(words[k].text, word) == 0 ) {
                                        words[k].count++;
                                }
                                else { 
                                        if ( strlen(words[k].text) == 0 ) {
                                                strncpy(words[k].text, word,strlen(word));
                                                words[k].count = 1;
                                                break;
                                        }
                                }
                        }
	int count = 0;
	for (int k = 0; k < MAX_WORDS; k++) {
		if ( strlen(words[k].text) != 0 ) {
			count++;
			printf( "%s\n", words[k].text );
		}
	}
	return count;
}
