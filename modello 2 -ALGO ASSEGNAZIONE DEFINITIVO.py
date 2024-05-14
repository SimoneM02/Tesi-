from mip import*
import time
import math

filesporco= open('75n4m1a.txt', 'r')
file=filesporco.read()                      
file = file.replace('level 1:', '')         
file = file.replace('level 2:', '')
file = file.replace('level 3:', '')
righe= file.splitlines()

filescrittura= open('risultati_75n4m1a_ALGORITMO DI ASSEGNAZIONE.txt', 'w')
print('Dati iniziali da file 75n4m1a.txt                  Modello 2\n\nLegenda:\ncolonna 1 istanza;\ncolonna 2 valore funzione obbiettivo;\ncolonna 3 stato della soluzione;\ncolonna 4 tempo di calcolo;\ncolonna 5 miglior LB.\n\n', file=filescrittura)
print('Parametri:   Max_second = 300    Max_gap = 0     T = determinato con algoritmo euristico\n ALGORITMO DI ASSEGNAZIONE JOB\n\n', file=filescrittura)

istanza = 0
contatorerighexlevel = 7
contatorerighexistanze = 6

J =int(righe[0])    
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

        combined_data = list(zip(pj, sj, tj))
        sorted_combined_data = sorted(combined_data, key=lambda x: (x[1], -x[0]))

        s_pj = [data[0] for data in sorted_combined_data]
        s_sj = [data[1] for data in sorted_combined_data]
        s_tj = [data[2] for data in sorted_combined_data]
        
        arr = 0.1

        var_assegnare = math.ceil(arr * J)

        tempo_server = 0
        tempo_macchina = []
        for a in range(macchine):
            tempo_macchina.append(0)

        job_ass = 0

        m = Model('Time-Indexed Formulations TIFs')         
        y =[[m.add_var(name='y({})({})'.format(i, t), var_type=BINARY) for t in range(T-s_tj[i])] for i in range(J)]  
        Cmax = m.add_var(name='Cmax')
        w = [m.add_var(name='w({})'.format(t), var_type=INTEGER, lb=0, ub= macchine) for t in range(T)]

        for mm in range(0, macchine*(math.ceil(var_assegnare/macchine)), macchine):
            for macch in range(macchine):
                if job_ass < var_assegnare:
                    y[job_ass][max(tempo_server, tempo_macchina[macch])] = 1
                    tempo_macchina[macch] = max(tempo_server, tempo_macchina[macch]) + s_sj[job_ass]
                    tempo_server =  tempo_macchina[macch]
                    tempo_macchina[macch] += s_pj[job_ass] 
                    job_ass +=1
            tempo_server = max(tempo_server, min(tempo_macchina))

        for i in range(J):
           m+= xsum(y[i][t] for t in range(T-s_tj[i])) == 1, '(1b)'
        for t in range(T-1):
            m+= xsum(y[i][s] for i in range(J) for s in range(max(0, t-s_tj[i]+1), min(t+1, T-s_tj[i]))) + w[t] == macchine, '(2b)'
        for t in range(T-1):
            m+= xsum(y[i][s] for i in range(J) for s in range(max(0, t-s_sj[i]+1), min(t+1, T-s_tj[i]))) <= 1, '(2c)'
        for i in range(J):
            m+= Cmax >= xsum((t + s_tj[i])*y[i][t] for t in range(T-s_tj[i])), '(1f)'

        m.objective = minimize(Cmax)             
        start_time = time.time()                
        status = m.optimize(max_seconds=300)   
        m.max_mip_gap = 0
        end_time = time.time()                 
        runtime = end_time - start_time         

        print(istanza, '        ', m.objective_value, '        ', file=filescrittura, end='')
        if status == OptimizationStatus.OPTIMAL:
            print('OPTIMAL', '        ', file=filescrittura, end='')
        elif status == OptimizationStatus.FEASIBLE:
         print('FEASIBLE', '        ', file=filescrittura, end='')
        elif status == OptimizationStatus.NO_SOLUTION_FOUND:
            print('NO SOLUTION FOUND',T, '        ', file=filescrittura, end='')
        print(runtime, '        ', m.objective_bound, '        ', file=filescrittura)

    contatorerighexistanze = contatorerighexistanze + 8
    contatorerighexlevel = contatorerighexlevel + 8

filescrittura.close()
filesporco.close()