#include <iostream>
int a=14;
int b=24;
void f() {
    a=a+9;
    b=b*7;
}
int main() {
    f();
    std::cout<<a+b;
}
