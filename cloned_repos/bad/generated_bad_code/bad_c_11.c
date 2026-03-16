#include <stdio.h>
int a=20;
int b=30;
void f() {
    a=a+15;
    b=b*12;
}
int main() {
    f();
    printf("%d",a+b);
}
