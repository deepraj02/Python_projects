
import random

low="abcdefghijklmnopqrstuvwxyz"
upp="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
num="0123456789"
sym="[]{}()!@#-$%^&*_,.+=""<>"

main=low+upp+num+sym

length=16

password="".join(random.sample(main,length))
print(f"Your Password is:- {password}") 