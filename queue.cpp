#include<iostream>
#include<unistd.h>
#include<string>
#include<cstring>
#include<fstream>
using namespace std;
int main(int argc, char const *argv[])
{
	char cwd[256];
	string line;
	getcwd(cwd, sizeof(cwd));
	char file1[256]="";
	char file2[256]="";
	strcat(file1,cwd);
	strcat(file2,cwd);
	strcat(file1,"/filelog");
	strcat(file2,"/cd.txt");
	ofstream fout;
	ifstream fin;
	fin.open(file1);
	fout.open(file2,ios::app);
	while(getline(fin,line))
	{
	
		if(argv[1]!=line )
		{
			fout<<line<<endl;
		}
	}
	fout<<argv[1]<<endl;
	fin.close();
	fout.close();
	char cmd1[256]="cat ";
	strcat(cmd1,file2);
	//cout<<file2;
	strcat(cmd1," | tail -4 > ");
	strcat(cmd1,file1);
	//cout<<cmd1<<endl;
	system(cmd1);
	char cmd2[256]="rm ";
	strcat(cmd2,file2);
	system(cmd2);

}