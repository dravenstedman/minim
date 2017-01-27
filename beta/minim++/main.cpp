#include <iostream>
#include <string>
#include <cstring>
#include <vector>

/*  MINIM 1.1
/   C++ IMPLEMENTATION
/   This is highly experimental and as such should definitely not
/   be considered the reference implementation. The reference
/   implementation is the original Python version, which even
/   after this reaches completion will remain the single reference
/   implementation of MINIM. In the future this /may/ become the
/   reference but time will tell.
/
/
/   This, along with all the other source code for the Minim project,
/   is licenced under the Modified BSD Licence. See LICENCE for details. */

std::vector<std::string> tokenize(std::string s, std::string d=" ") {
  // tokenize (string s, string d)
  // s - string you want to tokenize
  // d - delimiters to be used, defaults to space
  // returns a vector with the tokenized form of the string s passed to it.
  // also effectively a string-split function implementation
  std::vector<std::string> newS;
  char * bar;
  char foo[s.length()];
  std::strcpy(foo, s.c_str());
  bar = std::strtok(foo, d.c_str());
  while (bar != NULL)
  {
    newS.push_back(std::string(bar));
    bar = std::strtok(NULL, d.c_str());
  }
  delete [] bar;
  return newS;
}

void print_vector(std::vector<std::string> v){
  // I'm including this function solely for debug purposes so that I can
  // see what my vectors got inside them.
  for(int i=0; i < v.size(); ++i){
    std::cout << v[i] << "\n";
  };
}

bool is_whitespace(std::string& str)
{
    std::size_t first = str.find_first_not_of(' ');
    if (first == std::string::npos)
        return "";
    size_t last = str.find_last_not_of(' ');
    std::string fbar = str.substr(first, (last-first+1));
    return fbar.empty();
}

bool is_newline(std::string& str)
{
    std::size_t first = str.find_first_not_of('\n');
    if (first == std::string::npos)
        return "";
    size_t last = str.find_last_not_of('\n');
    std::string fbar = str.substr(first, (last-first+1));
    return fbar.empty();
}

std::string strip(std::string str, const char* delimiter)
{
    // strip (string, delimiter)
    // Strips the string of whatever delimiter you said and then returns the
    // new string.
    size_t first = str.find_first_not_of(delimiter);
    if (first == std::string::npos)
        return "";
    size_t last = str.find_last_not_of(delimiter);
    return str.substr(first, (last-first+1));
}

std::vector<std::string> separate_lines(std::string code){
  // Separates lines of code, presumably taken from a file.
  std::vector<std::string> x = tokenize(code, "\n");  // First we'll just separate by line.
  std::vector<std::string> iil;
  for(int i=0; i < x.length(); i++){
    // So we'll need to get rid of comments and get rid of whitespace.
    // Not entirely sure how we'll do that but I'll figure out a way.
    std::string baz = x[i];
    // First we'll find comments:
    if(baz.find("//") != std::string::npos or is_newline(baz) or is_whitespace(baz)){
      // this is a comment or it's whitespace, so we'll skip over it
    } else {
      // this is the tough part.
      // We need to strip the line of any newlines, tabs, etc.
      std::string fbaz = strip(strip(baz, "\n"), "\t"); // uhh this should work
    }
  }
}



int main(){}
