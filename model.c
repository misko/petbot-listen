
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

double intercept;
double * w;
int model_size;

#define MAX_V_SIZE	4096


double logit(double * v) {
	double c = intercept;
	//fprintf(stdout,"%lf intercept\n",intercept);
	int i;
	double tmp[model_size/2];
	/*for (i=0; i<model_size; i++) {
		//fprintf(stdout, "%d %lf\n",i,w[i]);

		
		//regulat
		c+=w[i]*abs(v[i]);

		//fold back
		if (i<model_size/2) {
			c+=w[i]*(abs(v[i]) + abs(v[model_size-1-i]));
		}

		//fold back - with trim
		if (i<model_size/2) {
			if (i>=20 && i<150) {
				c+=w[i-20]*(abs(v[i]) + abs(v[model_size-1-i]));
			}
		}
	}*/


	//for (i=20; i<80; i++) {
	//	c+=w[i-20]*(abs(v[i]) + abs(v[model_size-1-i]));
	//}

	
	//reduce by half
	for (i=0; i<model_size/2; i++) {
		tmp[i]=abs(v[i])+abs(v[model_size-1-i]);
	}

	//blur and put back
	for (i=0; i<model_size/2; i++) {
		if (i>1 && i<((model_size/2)-2)) {
			c+=w[i]*(tmp[i-2]*0.1+tmp[i-1]*0.2+tmp[i]*0.4+tmp[i+1]*0.2+tmp[i+2]*0.1);
		} else {
			c+=0;
		}
	}

	/*for (i=0; i<model_size/2; i++) {
		//if (i>=3 || i<(model_size/2 - 3)) 
		if (i>1 && i<(model_size-2)) {
			c+=w[i]*(abs(v[i]) + abs(v[model_size-1-i]));
		} else {
			assert(abs(w[i])<0.00000000001);
		}
		//}
	}*/
	


	return 1.0/(1+exp(c));
}

int read_model(char * filename) {
	model_size=0;
	FILE * fptr = fopen(filename,"r");
	if (fptr==NULL) {
		fprintf(stderr, "Failed to open model %s\n", filename);
		exit(1);
	}

	w = (double*)malloc(sizeof(double)*MAX_V_SIZE);
	if (w==NULL) {
		fprintf(stderr, "Failed to alloc mem for mdel vec\n");	
		exit(1);
	}
	memset(w,0,sizeof(double)*MAX_V_SIZE); 

	char line[1024];
	if (fgets(line, 1024, fptr)) {
		int r = sscanf(line,  "%lf\n", &intercept);
		if (r!=1) {
			fprintf(stderr,"Failed to read header model\n");
			exit(1);
		}
	} else {
		fprintf(stderr,"Failed to read header model\n");
		exit(1);
	}
	while (fgets(line, 1024, fptr)) {
		int index;
		double value;
		int r =sscanf(line, "%d %lf\n",&index, &value);
		if (r!=2) {
			fprintf(stderr, "Failed to load model!\n");
			exit(1);
		}
	 	if (index>=MAX_V_SIZE) {
			fprintf(stderr, "Model is in apprpriate\n");
			exit(1);
		}
		w[index]=value;
		if ((index+1)>model_size) {
			model_size=index+1;
		}
	}
	fclose(fptr);
	return model_size;
}
