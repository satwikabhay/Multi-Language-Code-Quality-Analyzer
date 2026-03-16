#include <iostream>
int a=29;
int b=39;
void f() {
    a=a+24;
    b=b*22;
}
int main() {
    f();
    std::cout<<a+b;
}
