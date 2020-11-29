import random

while True:    
    def game():
        print('Select Your Object:-')
        print("1.Rock")
        print("2.Paper")
        print("3.Scissor")
        print("Press ~ to quit the game")
        a=int(input("Enter Your desired Selection:- "))
        rps=['Rock','Paper','Scissor']
        comp=rps[random.randint(0,2)]
        if a==comp:
            return (f"Both Computer and you Choosed the Same i.e: {comp}")
        elif a=='1':
            if comp=='Paper':
                return (f"Computer Won!, Computer choosed:- {comp}")
            else:
                return(f"You Won!, Computer Chosed:- {comp}")
        
        elif a=='2':
            if comp=='Scissor':
                return(f"Computer Won!, Computer choosed:- {comp}")
            else:
                return(f"You Won!, Computer Chosed:- {comp}")
            
        elif a=='3':
            if comp=="Rock":
                return(f"Computer Won!, Computer choosed:- {comp}")
            else:
                return(f"You Won!, Computer Chosed:- {comp}")
        
    game()