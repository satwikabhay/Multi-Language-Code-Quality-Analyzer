#include <stdio.h>
int a=17;
int b=27;
void f() {
    a=a+12;
    b=b*9;
}
int main() {
    f();
    printf("%d",a+b);
}
