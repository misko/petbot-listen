
#include <stdio.h>
#include <stdlib.h>
#include "model.h"

#define BUFFER_SIZE	1024*64

void run_file(char * fn, int length) {
	FILE * fptr = fopen(fn,"r");
	if (fptr==NULL) {
		fprintf(stdout,"failed to open file %s\n",fn);
		exit(1);
	}	
	
	char * line = (char*)malloc(sizeof(BUFFER_SIZE));
	if (line==NULL) {
		fprintf(stdout, "failed to malloc buffer\n");
		exit(1);
	}



	fgets(line,BUFFER_SIZE,fptr); //get rid of header
	while (fgets(line,BUFFER_SIZE,fptr)) {
		double v[length];
		//lets read in the v and then get the score
		char * c, *p;
		c=line;
		p=line;
		int i=0;
		while (*p!='\0') {
			while (*c!='\0' || *c!='\n' || *c!=',') {
				c++;
			}
			if (*c=='\n') {
				c='\0';
			}

			char t=*c;
			c='\0';
			if (i>=length) {
				fprintf(stdout,"failed to read in model, length is off!\n");
				exit(1);
			}
			v[i++]=atof(p);
	
			if (t!='\0') {
				c++;
			}
			p=c;	
		}
	}	
}

int main(int argc, char ** argv) {
	if (argc!=3) {
		fprintf(stdout, "%s model data\n",argv[0]);
		exit(1);
	}

	char * model_filename=argv[1];
	char * data_filename=argv[2];
	
	
	int length = read_model(model_filename);
	run_file(data_filename,length);
			
	return 0;
}
