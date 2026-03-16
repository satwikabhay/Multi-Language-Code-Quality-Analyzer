#include <iostream>
int a=17;
int b=27;
void f() {
    a=a+12;
    b=b*10;
}
int main() {
    f();
    std::cout<<a+b;
}
