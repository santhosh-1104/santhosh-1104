# num1=float(input("enter first number:"))
# num2=float(input("enter second number:"))

# sum_result=num1+num2
# minus=num1-num2
# multiply=num1*num2
# divide=num1/num2

# print("sum="+sum_result)
# print("minus=",minus)
# print("multiply=",multiply)
# print("divide=",divide)

# num1=float(input("enter first number:"))
# num2=float(input("enter second number:"))
# print("operations:+,-,*,/")
# operation=input("enter operation:")
# if operation =="+":
#     result=num1+num2
# elif operation=="-":
#     result=num1-num2
# elif operation=="*":
#     result=num1*num2
# elif operation=="/":
#     if num2!=0:
#         result=num1/num2
#     else:
#         result="error"
# else:
#      result= "invalid operation"
# print("result=",result)
# import getpass
# username="santhosh"
# password="1234"
# user_name=input("enter the username:")
# user_pw=getpass.getpass("enter password")
# if username==user_name and password==user_pw:
#     print("login successful")
# else:
#     print("username or password is incorrect")
#

# correct_pin = 1234
# balance = 5000
# attempts = 3

# while attempts > 0:
#     user_pin = int(input("Please enter your PIN: "))

#     if user_pin == correct_pin:
#         print("Welcome, user!")

#         while True:
#             print("\nOptions:")
#             print("1. Check balance")
#             print("2. Withdraw money")
#             print("3. Deposit money")
#             print("4. Exit")

#             choice = input("Choose an option (1-4): ")

#             if choice == "1":
#                 print(f"Your bank balance is {balance}")

#             elif choice == "2":
#                 amount = int(input("Enter the amount you want to withdraw: "))
#                 if amount <= balance:
#                     balance -= amount
#                     print(f"{amount} withdrawn. Your remaining balance is {balance}")
#                 else:
#                     print("Insufficient balance.")

#             elif choice == "3":
#                 amount = int(input("Enter the amount you want to deposit: "))
#                 balance += amount
#                 print(f"{amount} credited. Your new balance is {balance}")

#             elif choice == "4":
#                 print("Thank you for using our service!")
#                 break  # Exiting the menu loop

#             else:
#                 print("Invalid option. Please try again.")

#         break  # Exit after successful login

#     else:
#         attempts -= 1
#         print(f"Incorrect PIN. Attempts left: {attempts}")

# if attempts == 0:
#     print("Too many failed attempts. Your card is locked.")

# import random
# choices=["rock","paper","scissors"]
# while True:
#     user_choice=input("choose rock,paper,scissors(or type exit to quit):").lower()
#     if user_choice=="exit":
#         print("thanks for playing!Goodbye!")
#         break
#     if user_choice not in choices:
#         print("invalid choice")
#         continue
#     computer_choice = random.choice(choices)
#     print(f"Computer chose: {computer_choice}")

#     if user_choice == computer_choice:
#         print("It's a tie!")
#     elif (user_choice == "rock" and computer_choice == "scissors") or \
#          (user_choice == "scissors" and computer_choice == "paper") or \
#          (user_choice == "paper" and computer_choice == "rock"):
#         print("You win!")
#     else:
#         print("You lose!")
    
      

# for x in range(1,11):
#             print(x)

# for x in range(1,20):
#  if x%2==0:
#    print(x)

# user_input=int(input("please enter a number"))
# i=1
# while i<=10:
#     print(f"{user_input} x {i} = {user_input*i}")
#     i+=1

# tuples=(1,2,3,4,5)
# print(tuples[2])

# print(len(tuples))
# print(3 in tuples)

# set={1,2,3,4,5}
# set.add(6)
# print(set)
# set.remove(3)
# print(set)
# print(5 in set)

# def is_even(number):
#     return number % 2 == 0

# # Testing the function
# print(is_even(4))  # True
# print(is_even(7))  # False
# print(is_even(10)) # True

# with open("new text document.txt", "r") as file:  # Open the file in read mode
#     content = file.read()  # Read file content
#     print(content)  # Print the content

# import csv
# with open("data.csv","w",newline="") as file:
#   writer=csv.writer(file)
#   writer.writerow(["Name", "Age", "Country"])

#   writer.writerow(["Alice", 25, "USA"])
#   writer.writerow(["Bob", 30, "Canada"])
#   writer.writerow(["Charlie", 22, "UK"])

# print("CSV file created successfully!")
# with open("data.csv","r") as file1:
#  content=file1.read()
#  print(content)

# import csv

# with open("data.csv", "r") as file:
#     reader = csv.reader(file)
#     for row in reader:
#         print(row)  # Print each row
# import csv

# with open("data.csv", "r") as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         print(row)  # Each row is a dictionary



with open("binary_file.bin", "rb") as f:
    content = f.read()
    print("Binary Data:", content)



