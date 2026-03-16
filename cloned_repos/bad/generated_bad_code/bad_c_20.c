#include <stdio.h>
int a=29;
int b=39;
void f() {
    a=a+24;
    b=b*21;
}
int main() {
    f();
    printf("%d",a+b);
}
