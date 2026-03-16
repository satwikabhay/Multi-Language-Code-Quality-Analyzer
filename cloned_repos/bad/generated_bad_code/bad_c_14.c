#include <stdio.h>
int a=23;
int b=33;
void f() {
    a=a+18;
    b=b*15;
}
int main() {
    f();
    printf("%d",a+b);
}
