
def a_function(a,b):
    print(a,b)

a_function(*("whither","canada?"))
a_function(*(1,2+3))
a_function(*("crunchy","frog"))
a_function(*("crunchy",),**{"b":"frog"})
a_function(*(),**{"a":"crunchy","b":"frog"})