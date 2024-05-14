from mip import*
import time
import math

filesporco= open('10n2m2a.txt', 'r')
file=filesporco.read()
file = file.replace('level 1:', '')
file = file.replace('level 2:', '')
file = file.replace('level 3:', '')
righe= file.splitlines()

filescrittura= open('risultati_10n2m2a_T con algoritmo.txt', 'w')
print('Dati iniziali da file 10n2m2a.txt                  Modello 1\n\nLegenda:\ncolonna 1 istanza;\ncolonna 2 valore funzione obbiettivo;\ncolonna 3 stato della soluzione;\ncolonna 4 tempo di calcolo;\ncolonna 5 miglior LB.\n\n', file=filescrittura)
print('Parametri:   Max_second = 60    Max_gap = 0     T = determinato con algoritmo euristico\n\n', file=filescrittura)

istanza = 0
contatorerighexlevel = 7
contatorerighexistanze = 6

J =int(righe[0])    
JD=J       
n = J
macchine = int(righe[1])    

for i in range(5):
    pj = [int(numero) for numero in righe[contatorerighexistanze].split()]
    contatoresetup = 0

    for i in range(3):
        istanza = istanza + 1
        contatoresetup = contatoresetup + 1
        sj=[int(numero) for numero in righe[contatorerighexlevel+contatoresetup].split()]
        tj = [x+y for x, y in zip(pj, sj)]
        tj = tj + tj 
        
        T = 0
        Tm = list(0 for c in range(macchine))
        contatorejob = 0
        for j in range(0, (math.ceil(J/macchine)*macchine), macchine):
            for c in range(macchine):
                 if contatorejob < J:
                       Tm[c] += sj[contatorejob]
                       for s in range(macchine):
                            if s != c:
                                 if Tm[s] < Tm[c]:
                                     Tm[s] = Tm[c]
                       Tm[c] += pj[contatorejob]
                 contatorejob += 1          
        T = max(Tm)+1

        m = Model('Time-Indexed Formulations TIFs')  
        y =[[m.add_var(name='y({})({})'.format(i, t), var_type=BINARY) for t in range(T-tj[i])] for i in range(J+JD)]  
        Cmax = m.add_var(name='Cmax')

        for i in range(J):
            m+= xsum(y[i][t] for t in range(T-tj[i])) == 1, '(1b)'

        for t in range(T-1):   
            m+= xsum(y[i][s] for i in range(J) for s in range(max(0, (t-tj[i]+1)), min(t+1, (T-tj[i])))) <= macchine, '(1c)'
          
        for i in range(JD):
           m+= xsum(y[i+n][t] for t in range(T-sj[i]) if t < T-tj[i]) == 1, '(1d)'

        for t in range(T-1): 
                   m+= xsum(y[i+n][s] for i in range(JD) for s in range(max(0, (t-sj[i]+1)), min(t+1,(T-tj[i])))) <= 1, '(1e)'

        for i in range(J):
            m+= Cmax >= xsum((t + tj[i])*y[i][t] for t in range(T-tj[i])), '(1f)'

        for i in range(J):
           for t in range(T-tj[i]):
               m+= y[i][t] == y[i+n][t], '(1g)'

        
        m.objective = minimize(Cmax)             
        start_time = time.time()                
        status = m.optimize(max_seconds=60)    
        m.max_mip_gap = 0
        end_time = time.time()                  
        runtime = end_time - start_time         

        print(istanza, '        ', m.objective_value, '        ', file=filescrittura, end='')
        if status == OptimizationStatus.OPTIMAL:
            print('OPTIMAL', '        ', file=filescrittura, end='')
        elif status == OptimizationStatus.FEASIBLE:
         print('FEASIBLE', '        ', file=filescrittura, end='')
        elif status == OptimizationStatus.NO_SOLUTION_FOUND:
            print('NO SOLUTION FOUND', '        ', file=filescrittura, end='')
        print(runtime, '        ', m.objective_bound, '        ', file=filescrittura)
     
    contatorerighexistanze = contatorerighexistanze + 8
    contatorerighexlevel = contatorerighexlevel + 8

filescrittura.close()
filesporco.close()