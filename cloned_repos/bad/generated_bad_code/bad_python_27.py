f=open('file26.txt','r')
d=f.read()
f.close()
for l in d.split('\n'):
    print(l)
