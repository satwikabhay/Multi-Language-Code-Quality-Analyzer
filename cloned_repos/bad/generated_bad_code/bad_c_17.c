#include <stdio.h>
int a=26;
int b=36;
void f() {
    a=a+21;
    b=b*18;
}
int main() {
    f();
    printf("%d",a+b);
}
