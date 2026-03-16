"""
Generate Bad Code Examples
Creates intentionally poor-quality code in Python, Java, C++, and C
"""

import os
from pathlib import Path


def generate_bad_python_code(output_dir, count=30):
    """Generate bad Python code examples"""
    
    templates = [
        # No comments, magic numbers, single-letter vars
        """x=10
y=20
z=30
def a(b,c):
    return b*{n1}+c*{n2}
print(a(x,y))
""",
        # No error handling
        """f=open('file{i}.txt','r')
d=f.read()
f.close()
for l in d.split('\\n'):
    print(l)
""",
        # Poor naming, no docstrings
        """def f(a,b,c):
    x=a+b
    y=x*c
    z=y/{n}
    return z
r=f(10,20,30)
""",
        # Magic numbers everywhere
        """data=[{n1},{n2},{n3},{n4},{n5}]
result=[]
for i in data:
    if i>{n6}:
        result.append(i*{n7})
print(sum(result))
""",
        # No structure
        """a={n1}
b={n2}
c=a+b
d=c*{n3}
e=d-{n4}
f=e/{n5}
print(f)
"""
    ]
    
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(count):
        template = templates[i % len(templates)]
        code = template.format(
            i=i,
            n=2+i, n1=10+i, n2=20+i, n3=30+i,
            n4=40+i, n5=50+i, n6=15+i, n7=3+i
        )
        
        filepath = Path(output_dir) / f"bad_python_{i+1:02d}.py"
        with open(filepath, 'w') as f:
            f.write(code)
        
        print(f"  Created: bad_python_{i+1:02d}.py")


def generate_bad_java_code(output_dir, count=30):
    """Generate bad Java code examples"""
    
    templates = [
        # No comments, poor naming
        """public class C{i} {{
    public static void main(String[] a) {{
        int x={n1};
        int y={n2};
        int z=x+y;
        System.out.println(z);
    }}
}}
""",
        # Magic numbers, no error handling
        """public class T{i} {{
    public int c(int a,int b) {{
        return a*{n1}+b*{n2};
    }}
    public static void main(String[] x) {{
        T{i} t=new T{i}();
        System.out.println(t.c({n3},{n4}));
    }}
}}
""",
        # Poor structure
        """public class P{i} {{
    int x={n1};
    int y={n2};
    void m() {{
        x=x+{n3};
        y=y*{n4};
    }}
    public static void main(String[] a) {{
        P{i} p=new P{i}();
        p.m();
    }}
}}
""",
    ]
    
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(count):
        template = templates[i % len(templates)]
        code = template.format(
            i=i+1,
            n1=10+i, n2=20+i, n3=5+i, n4=2+i
        )
        
        filepath = Path(output_dir) / f"Bad{i+1:02d}.java"
        with open(filepath, 'w') as f:
            f.write(code)
        
        print(f"  Created: Bad{i+1:02d}.java")


def generate_bad_cpp_code(output_dir, count=20):
    """Generate bad C++ code examples"""
    
    templates = [
        # No comments, magic numbers
        """#include <iostream>
using namespace std;
int main() {{
    int x={n1};
    int y={n2};
    int z=x*{n3}+y*{n4};
    cout<<z<<endl;
    return 0;
}}
""",
        # Poor naming, no structure
        """#include <iostream>
int a={n1};
int b={n2};
void f() {{
    a=a+{n3};
    b=b*{n4};
}}
int main() {{
    f();
    std::cout<<a+b;
}}
""",
        # Magic numbers everywhere
        """#include <iostream>
int c(int x) {{
    return x*{n1}+{n2};
}}
int main() {{
    int r=c({n3});
    std::cout<<r;
}}
""",
    ]
    
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(count):
        template = templates[i % len(templates)]
        code = template.format(
            n1=10+i, n2=20+i, n3=5+i, n4=3+i
        )
        
        filepath = Path(output_dir) / f"bad_cpp_{i+1:02d}.cpp"
        with open(filepath, 'w') as f:
            f.write(code)
        
        print(f"  Created: bad_cpp_{i+1:02d}.cpp")


def generate_bad_c_code(output_dir, count=20):
    """Generate bad C code examples"""
    
    templates = [
        # No comments, magic numbers
        """#include <stdio.h>
int main() {{
    int x={n1};
    int y={n2};
    int z=x+y*{n3};
    printf("%d",z);
    return 0;
}}
""",
        # Poor naming, global variables
        """#include <stdio.h>
int a={n1};
int b={n2};
void f() {{
    a=a+{n3};
    b=b*{n4};
}}
int main() {{
    f();
    printf("%d",a+b);
}}
""",
        # No error handling, magic numbers
        """#include <stdio.h>
int c(int x,int y) {{
    return x*{n1}+y*{n2};
}}
int main() {{
    int r=c({n3},{n4});
    printf("%d",r);
}}
""",
    ]
    
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(count):
        template = templates[i % len(templates)]
        code = template.format(
            n1=10+i, n2=20+i, n3=5+i, n4=2+i
        )
        
        filepath = Path(output_dir) / f"bad_c_{i+1:02d}.c"
        with open(filepath, 'w') as f:
            f.write(code)
        
        print(f"  Created: bad_c_{i+1:02d}.c")


def main():
    print("=" * 70)
    print("GENERATING BAD CODE EXAMPLES")
    print("=" * 70)
    
    output_dir = "cloned_repos/bad/generated_bad_code"
    
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerating files...\n")
    
    print("📝 Python files:")
    generate_bad_python_code(output_dir, count=30)
    
    print("\n📝 Java files:")
    generate_bad_java_code(output_dir, count=30)
    
    print("\n📝 C++ files:")
    generate_bad_cpp_code(output_dir, count=20)
    
    print("\n📝 C files:")
    generate_bad_c_code(output_dir, count=20)
    
    total_files = 30 + 30 + 20 + 20
    
    print("\n" + "=" * 70)
    print("GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\n✅ Created {total_files} bad code examples")
    print(f"   Python: 30 files")
    print(f"   Java:   30 files")
    print(f"   C++:    20 files")
    print(f"   C:      20 files")
    print(f"\nLocation: {output_dir}/")
    print("\n" + "=" * 70)
    print("NEXT STEP:")
    print("=" * 70)
    print("Run: python 1_collect_multilang_data.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
