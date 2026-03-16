f=open('file6.txt','r')
d=f.read()
f.close()
for l in d.split('\n'):
    print(l)
