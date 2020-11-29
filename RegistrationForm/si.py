def simple_interest(p,t=5,r=10): 
    si = (p * t * r)/100
    print(f'The Principal is,{p}') 
    print(f'The Time period is, {t} years') 
    print(f'The Rate of interest is, {r} %')
    print('The Simple Interest is', si) 
    print(f'The Final amount will be, {si+p}')
    
    return si 
    
simple_interest(1000)
