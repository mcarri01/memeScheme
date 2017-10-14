#include <iostream>
#include <cstdlib>

using namespace std;

int main(int argc, char *argv[]) {

	string file = argv[1];

	string command = "python meme_int.py ";
	command.append(file); 
	const char* conv_command = command.c_str();
	system(conv_command);
	return 0; 

}