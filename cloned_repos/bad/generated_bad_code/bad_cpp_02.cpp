#include <iostream>
int a=11;
int b=21;
void f() {
    a=a+6;
    b=b*4;
}
int main() {
    f();
    std::cout<<a+b;
}
