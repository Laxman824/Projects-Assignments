#include<stdio.h>
#include<sys/types.h>
#include<unistd.h>
#include<sys/wait.h>
#include<stdlib.h>

int main(int argc, char *argv[])
{
	int status;
    int* ptr;
    ptr = (int*)malloc(4096 * sizeof(int));
	for (int i = 0; i < 40000; i++) 
	{
		int pid = fork();
		if (pid < 0) return -1;
		if (pid == 0) return 0;
		waitpid(pid, &status, 0);
	}
    free(ptr);
	return 0;
}
