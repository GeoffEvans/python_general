
import random
import numpy 
import matplotlib.pyplot as pyplot
import copy
import time

t0 = time.time()

N_= 7
T = 4
epsilon = (float(T)/float(N_)) 
def e_vals(epsilon, N_):
    e = numpy.zeros(N_)
    fine = numpy.linspace(-(N_-1)/2*epsilon, False, (len(e)+1)/2)
    for i in range(len(fine)):
        e[i] = fine[i]
    for i in range((len(e)+1)/2):
        e[i+(len(e)-1)/2] = epsilon*i
    return e
e = e_vals(epsilon, N_)

def path_1(N, x): 
    timespace = numpy.zeros(N)
    timespace[0] = x
    timespace[-1] = x 
    points = e
    for i in range(N-2):
        timespace[i+1] = 0 #points[random.randint(0,len(e)-1)]# points[random.randint(0,10)] #here we need to account for all space by finding all combinations of points
    return timespace

def many_paths(path_numb,N, x):
    paths = []
    for i in range(path_numb):
        paths.append(path_1(N, x))     
    return paths
 
def Gvalsofx(path_numb, N):
    
    xvals = e # [0] # numpy.array(( -5*epsilon,-4*epsilon, -3*epsilon, -2*epsilon, -1*epsilon ,0, epsilon, 2*epsilon, 3*epsilon, 4*epsilon, 5*epsilon))
    acceptance = 0
    total = 0
    total_paths =[]
    for ix in range(len(xvals)):
        paths = many_paths(path_numb, N , xvals[ix])
        ncor= 15
        G = 0
        for path in paths:
            for i in range(40*ncor):
                for k in range(1,len(path)-1): 
                                    #for each thermalisation sweep
                    En=0
                    Enp=0
                    
                    p = random.choice((-epsilon,epsilon))
                    pathP = numpy.copy(path)
                    pathP[k]+=p
                    for n in range(0,len(path)-1):
                        En += (0.5/epsilon**2)* (path[n+1]-path[n])**2 + 0.5*(0.5*(path[n]+path[n+1]))**2
                        Enp += (0.5/epsilon**2)* (pathP[n+1]-pathP[n])**2 + 0.5*(0.5*(pathP[n]+pathP[n+1]))**2
                    
                    deltaE = En-Enp
                    if float(deltaE) > float(0)  or numpy.random.uniform(0,1.3)<numpy.exp(deltaE):          
                        path = pathP
                        acceptance += 1
                        total +=1
                    else:
                        total +=1 
                        
                
                    if  i%ncor==ncor-1 and i>(20*ncor-2): #and k == len(path)-2:
                        for n in range(1,len(path)-1):
                            total_paths += [path[n]]
                    #maybe i do need to run through the whole path....
                    
        #Phasorarray[ix] = G
    #Z = numpy.sum(Phasorarray)
                
        
    #for i in range(len(Phasorarray)):
        #Pvals[i]= (Phasorarray[i]/Z)
    values = numpy.zeros(len(e))
    for n in range(len(e)):
        for i in range(len(total_paths)):
            if -0.001 <total_paths[i] - e[n] < 0.001:
                values[n] += 1
         
    Z = numpy.sum(values)
    cool_vals = numpy.zeros(len(values))
    for i in range(len(values)):
        cool_vals[i] = float(values[i]) / Z
    okay = numpy.sum(cool_vals)
    return  total_paths   , float(acceptance)/float(total), cool_vals, values, Z, okay
    
    
def analytical(xMin, xMax):
    xvals = e
    Gamplitude = numpy.zeros(len(xvals))
    Pamplitude = numpy.zeros(len(xvals))
    for i in range(len(xvals)):
       Gamplitude[i] = (numpy.exp(-(xvals[i]*xvals[i])/2)/(numpy.pi)**0.25)**2
    Z = numpy.sum(Gamplitude)
    for i in range(len(xvals)):
        Pamplitude[i] = float((Gamplitude[i]))/Z
    return Pamplitude, Z , Gamplitude
#print (Gvalsofx(2, 7))[0]
#print (Gvalsofx(2, 7))[1]
#print (Gvalsofx(2, 7))[2]
#print (Gvalsofx(2, 7))[3]
#print (Gvalsofx(2, 7))[4]
#print (Gvalsofx(2, 7))[5]
#print  sum(analytical(-2,2)[0])
#print e
#print sum(abs(Gvalsofx(2, 7)[2] - (analytical(-2,2)[0])))
#print  analytical(-2,2, 11)[1]
#print  analytical(-2,2, 11)[2]
#print len(analytical(-2,2, 11)[0])
#print len((Gvalsofx(1, 7,7))[2])
#print numpy.arange(-5*epsilon, 3, epsilon)
#pyplot.hist(Gvalsofx(2, 7,7)[0], align = 'mid') 
pyplot.plot( e, Gvalsofx(1, 7)[2]) 
#pyplot.plot(numpy.linspace(0,2,7), Gvalsofx(1, 7,7)[0])
pyplot.plot(e, analytical(-2,2)[0])
pyplot.show()
t1 = time.time()
total = t1-t0
print total
    
    