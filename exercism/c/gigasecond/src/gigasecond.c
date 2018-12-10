#include "gigasecond.h"
#include <time.h>

time_t gigasecond_after(time_t arg) {
	return arg + 1000000000;
}
