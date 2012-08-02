a=(5,2,3)
for i,j in enumerate(a[:-1]):
    if a[i+1] <= j:
        print 'x'
