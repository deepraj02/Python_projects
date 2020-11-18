
import random

low="abcdefghijklmnopqrstuvwxyz"
upp="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
num="0123456789"
sym="[]{}()!@#-$%^&*_,.+=""<>"

main=(low+upp+num+sym)

length=int(input("Enter the Length for your Password:--\n"))

password="".join(random.sample(main,length))
print(f"Your Password is:- {password}") 