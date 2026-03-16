#include <iostream>
int a=20;
int b=30;
void f() {
    a=a+15;
    b=b*13;
}
int main() {
    f();
    std::cout<<a+b;
}
