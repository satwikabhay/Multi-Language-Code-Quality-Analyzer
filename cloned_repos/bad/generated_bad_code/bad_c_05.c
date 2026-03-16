#include <stdio.h>
int a=14;
int b=24;
void f() {
    a=a+9;
    b=b*6;
}
int main() {
    f();
    printf("%d",a+b);
}
