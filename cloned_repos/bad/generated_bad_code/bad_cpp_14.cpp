#include <iostream>
int a=23;
int b=33;
void f() {
    a=a+18;
    b=b*16;
}
int main() {
    f();
    std::cout<<a+b;
}
