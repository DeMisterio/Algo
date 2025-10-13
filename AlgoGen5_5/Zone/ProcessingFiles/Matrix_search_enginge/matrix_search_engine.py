import numpy as np
import random as gandon
import time  # модуль для измерения времени

rows, cols = 3, 3 # размер матрицы
matrices = [] #All our matrixased matrices
info_ready_list = [] #Non-matrixised, randomly/personaly generated lists.


def the_kernel(): # The head of the programm
    global type_check 
    start_time = time.time() #Starting to count
    def stat_num(z): #This is clear intager matrixising, only for 9 lengh intagers at the moment!
        global end_time, total_duration, check_algorithm_int, Total_weight #Globalising , 
        
        try:
            Total_weight = 0
            for indx_matrix in str(info_ready_list[z]): #Going for each element in the number [z] from list of ready, randomly generated numbers
               values = [bin(int(x)) for x in str(info_ready_list[z])] #Making the list of binary separated numbers [z]
               matrix_3x3 = np.array(values).reshape(rows, cols) #Matrixising.
               matrices.append(matrix_3x3) #Addding the matrix to the list of matrixes. (at the moment!)
               Total_weight += matrix_3x3.itemsize #Adding the weight of the number to the total weight
            if diagnostic_status == True: # If diagnostic works,
                check_algorithm_int = True #It means the number upside rearranged successfuly!
        except ValueError: # Or
            if diagnostic_status == True: #If number not rearranged succesfuly (due the test of CLEARLY intagers, there cannot be strings)
                check_algorithm_int = False #The test failed, something wrong with the rearranging algorithms
            else: #If this Value Error (cannot be matrixised) happens away from diagnostic:
                print("Ошибка: Введённое значение не может быть преобразовано в целые числа.", ValueError) #Notify user
            return #Return
            
    for z in range(0, len(info_ready_list) - 1): # Going through all elements in ready, randomly generated elements
        if isinstance(info_ready_list[z], int): #If this element is intager,
            stat_num(z) #Then we do the matrixising of the element z             
        else: #Or if it is not the int (due the diagnostics or not)
            if diagnostic_status == True: #We check for diagnostics status
                type_check = True #And wrong tpe determination test succesfully passed! Algorithm works!
    end_time = time.time()#We stop counting the time 
    total_duration = end_time - start_time #And estimate total time spent.
    if diagnostic_status != True: #If due the kernel function diagnostics if off:
        print(f"Все операции выполнены за {total_duration:.6f} секунд.")
        print(f"total weight of all matrixies: ~{(Total_weight/8) / (1024 * 1024)} mb") #Notify user

def value_giver(): #This is the randomaser of numbers to be put into th list of info_ready_list
    global hi_pick_for_rearranger
    hi_pick_for_rearranger = int(input("Enter the amount of number to rearrange!"))
    print(f"The compilation estimated time: {((predictedtimeend - predictedtimestart) * hi_pick_for_rearranger) / diagn_hi_pick_for_rearranger} seconds")
    for i in range(1, hi_pick_for_rearranger):
        info = gandon.randint(100000000, 999999999)
        info_ready_list.append(info)
    print("Compilation finished! rearranging! ")
    the_kernel()

def initializer(): #Diagnostics
    global diagnostic_status, type_check, check_algorithm_int, predictedtimestart, predictedtimeend, diagn_hi_pick_for_rearranger
    print("wait until we check utility please...")
    hi_pick_for_rearranger = 696 #We need to make 100 checks (for the type checking only)
    diagn_hi_pick_for_rearranger = hi_pick_for_rearranger#We need to make 100 checks (for the type checking only)
    diagnostic_status = True #Since now
    type_check = False #They havent been checked before
    check_algorithm_int = False #They also havent been checked before
    try:
        for c in range(1, hi_pick_for_rearranger): #Type checking diagnistics
            info = gandon.randint(100000000, 999999999) #9 times generate 9 lengh numbers end send each one to the kernel as always.
            info_ready_list.append(info) #For the kernel / matrixising
            the_kernel() #Initializing the kernel
        print("Type_checking finished!")
        info_ready_list.clear() #Before next check
        matrices.clear() #Before next check
        predictedtimestart = time.time() #We start counting the time
        for n in range(1, hi_pick_for_rearranger - 6): #Transcriptability diagnostics (if str can be transcripted into intager)
            info = str(gandon.randint(100000000, 999999999)) #We generate intagers, but make them str, so it cannot be matrixised
            info_ready_list.append(info)
            the_kernel()
        predictedtimeend = time.time() #We stop counting the time
        print("Check_int_transcriptability finished!")
        if type_check == True:
            if check_algorithm_int == True:
                print("Everything works!", "We start working!")
                info_ready_list.clear()
                matrices.clear()
                diagnostic_status = False
                value_giver()
            else:
                print("sorry, checking integer showed an errror, please check the code :(")
        else:
            print("Something wrong with type check... Please reatart algorithm either check the code")
    except:
        ValueError
    

initializer()

# Запускаем цикл в 99 итераций

# Засекаем время после завершения цикла