data=[38,48,58,68,78]
result=[]
for i in data:
    if i>43:
        result.append(i*31)
print(sum(result))
