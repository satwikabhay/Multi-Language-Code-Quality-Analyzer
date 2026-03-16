#include <iostream>
int a=26;
int b=36;
void f() {
    a=a+21;
    b=b*19;
}
int main() {
    f();
    std::cout<<a+b;
}
