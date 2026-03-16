#include <stdio.h>
int a=11;
int b=21;
void f() {
    a=a+6;
    b=b*3;
}
int main() {
    f();
    printf("%d",a+b);
}
