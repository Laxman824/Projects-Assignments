#filter funtion 
def numbergreater(num):
  if num > 5 :
    return True
  else:
    return False 
l =[2,4,5,7,8,9]
# can apply lambda here that is 
hel = lambda num :num >5
print(list(filter(numbergreater, l)))
