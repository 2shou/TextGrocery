
#include "util.c"

int main(int argc, const char* argv[]){
	INT64 offsets[1000];
	INT64 error_code = 0;
	merge_problems(&argv[1], argc-2, &offsets[0], argv[argc-1], 1, &error_code);

	for(int i = 0; i < argc-1; i++) 
		printf("%ld ", offsets[i]);
	puts("");
	return 0;
}

