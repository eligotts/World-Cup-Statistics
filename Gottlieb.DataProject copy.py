##Eli Gottlieb
##Honors Precalc, Period 4, Dr. Butler
##This program will have the user choose a statistic. The program will 
##create a bar chart that shows the likelihood that the team with the more number 
##of given statistic will win, lose, or tie.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data=pd.read_csv('SoccerStats.csv')

Scored=data['Goal Scored']
Possession=data['Ball Possession %']
Attempts=data['Attempts']
onTarget=data['On-Target']
freeKicks=data['Free Kicks']
Blocks=data['Blocked']
Saves=data['Saves']
PAccuracy=data['Pass Accuracy %']
Passes=data['Passes']
DCovered=data['Distance Covered (Kms)']
Fouls=data['Fouls Committed']
Offsides=data['Offsides']
Corners=data['Corners']
MOTM=data['Man of the Match']


'''
#SCATTER PLOTS
plt.scatter(freeKicks,Possession)
coeff=np.corrcoef(freeKicks,Possession)
#Not much, some positive trend, coeff=0.27
'''

#This scatter plot is interesting as it shows that the more a team passes,
#the higher the team's pass accuracy. 
'''
plt.scatter(Passes,PAccuracy)
plt.title("Number of Passes versus Pass Accuracy for every 2018 World Cup Game")
coeff=np.corrcoef(Passes,PAccuracy)
plt.ylabel("Percentage of Passes That Were Completed")
plt.xlabel("Passes")
#positive trend, coeff=0.693
plt.show()
'''
'''
plt.scatter(Passes,Possession)
coeff=np.corrcoef(Passes,Possession)
#very good, coeff=0.88, but pretty obvious

plt.scatter(Possession,Attempts)
coeff=np.corrcoef(Possession,Attempts)
#pretty good, coeff=0.54

plt.scatter(Fouls,PAccuracy)
#alright


print(coeff)
plt.show()
'''

'''
#HISTOGRAMS
Scored.hist(bins=6)
Possession.hist(bins=10)
PAccuracy.hist(bins=20)
DCovered.hist(bins=20)
'''
'''
#This histogram is very interesting because of the outliers that represent the 
#games that went into extra time. What statistics do we show?
DCovered.hist(bins=16)
plt.title("Distrobution of Distance Covered per Game for every 2018 World Cup Game")
plt.xlabel("Distance Covered (Km)")
plt.ylabel("Number of Games")
print(DCovered.mean())
print(DCovered.median())
plt.show()
'''

'''
Fouls.hist(bins=20)
Corners.hist(bins=11)
'''

'''
#BOXPLOTS
plt.boxplot(DCovered, vert=False)
plt.boxplot(Passes, vert=False)
plt.boxplot(PAccuracy, vert= False)
plt.boxplot(Possession, vert=False)
plt.boxplot(Attempts, vert=False)

plt.show()
'''


#MANIPULATION OF DATA
#FUNCTIONS

#This function gives us a list of numbers that represent the result of the game for each team
##2=Win, 1=Draw, 0=loss
length=len(Scored)
ii=0
result=np.array([])
while ii<length:
    if Scored[ii]>Scored[ii+1]:
        result=np.append(result,np.array([2,0]))
    elif Scored[ii]==Scored[ii+1]:
        result=np.append(result,np.array([1,1]))
    else:
        result=np.append(result,np.array([0,2]))
    ii=ii+2
    

#This function is just me comparing who won the game vs. who won man of the match
#Didn't end up doing anything with it
##4=Win and MOTM or loss and no MOTM, 3=Draw and MOTM, 2=Draw and no MOTM, 1=Win and no MOTM 0=loss and MOTM  
bb=0
motmWinner=np.array([])
while bb<length:
    if result[bb]==2:
        if MOTM[bb]=='Yes':
            motmWinner=np.append(motmWinner, np.array([4,4]))
        else:
            motmWinner=np.append(motmWinner, np.array([1,0]))
    elif result[bb]==1:
        if MOTM[bb]=='Yes':
            motmWinner=np.append(motmWinner, np.array([3,2]))
        else:
            motmWinner=np.append(motmWinner, np.array([2,3]))
    elif result[bb]==0:
        if MOTM[bb]=='Yes':
            motmWinner=np.append(motmWinner, np.array([0,1]))
        else:
            motmWinner=np.append(motmWinner, np.array([4,4]))
    bb=bb+2

##RELATIONSHIP BETWEEN RUNNING AND WINNING MOTM
#Another function that is just comparing two statistics
#Didn't up doing anything with this
##1=More d covered wins man of the match, 0=other way, 2=same d covered
##DOESN'T REALLY WORK
cc=0
motmRun=np.array([])
while cc<length:
    if DCovered[cc]>DCovered[cc+1]:
        if MOTM[cc]=='Yes':
            motmRun=np.append(motmRun,1)
        else:
            motmRun=np.append(motmRun,0)
    elif DCovered[cc]<DCovered[cc+1]:
        if MOTM[cc]=='Yes':
            motmRun=np.append(motmRun,0)
        else:
            motmRun=np.append(motmRun,1)
    else:
        motmRun=np.append(motmRun,2)
    cc=cc+2

##START OF REAL PROGRAM
#This function is fed a list that represents when a certain comparison results in
#a win, loss, or tie. It counts them all up and returns them. 
def CHECKWINLOSS(series):
    dd=0
    Works=0
    DoesntWork=0
    Tie=0
    length2=len(series)
    while dd<length2:
        if series[dd]==1:
            Works=Works+1
            dd=dd+1
        elif series[dd]==0:
            DoesntWork=DoesntWork+1
            dd=dd+1
        elif series[dd]==2:
            Tie=Tie+1
            dd=dd+1
        else:
            dd=dd+1
    return (Works, DoesntWork, Tie)
    

#This function is fed a step (example: one team has 100 more passes than the other, step=100)
#and a series. It creates a list of 0,1,2,3 (see below for meaning), then sums up the results
#using function above. Returns probablity that you either win, lose, or tie given that 
#condition is met (note: called possession, but works for any statistic)

#3=Condition not met, 2=draw, 1=more of statistic and win and less of statistic and lose
#0=less and win and more and lose
def PossessionWin(step,possession):
    ee=0
    length=len(possession)
    posWin=np.array([])
    while ee<length:
        if possession[ee]>possession[ee+1]:
            if (possession[ee]-step)>=possession[ee+1]:
                if result[ee]==2:
                    posWin=np.append(posWin,1)
                    ee=ee+2
                elif result[ee]==0:
                    posWin=np.append(posWin,0)
                    ee=ee+2
                else:
                    posWin=np.append(posWin,2)
                    ee=ee+2
            else:
                posWin=np.append(posWin,3)
                ee=ee+2
        elif possession[ee]==possession[ee+1]:
            posWin=np.append(posWin,3)
            ee=ee+2
        else:
            if (possession[ee+1]-step)>=possession[ee]:
                if result[ee+1]==2:
                    posWin=np.append(posWin,1)
                    ee=ee+2
                elif result[ee+1]==0:
                    posWin=np.append(posWin,0)
                    ee=ee+2
                else:
                    posWin=np.append(posWin,2)
                    ee=ee+2
            else:
                posWin=np.append(posWin,3)
                ee=ee+2
        
    #Run our list through previous function to see if it works
    WinandPossession=CHECKWINLOSS(posWin)
    chanceWin=WinandPossession[0]/(WinandPossession[0]+WinandPossession[1]+WinandPossession[2])
    chanceLose=WinandPossession[1]/(WinandPossession[0]+WinandPossession[1]+WinandPossession[2])
    chanceTie=WinandPossession[2]/(WinandPossession[0]+WinandPossession[1]+WinandPossession[2])
    return(chanceWin,chanceLose,chanceTie)

#This function's purpose is to feed different steps into the previous function.
#start=first step, finish=last step, series=statistic, 
#gap=change in step (example: if gap=20, it would calculate probablities for 200 more passes than opponent, then 220 more passes)
def LOOP(start,finish,series,gap):
    ff=start
    steps=np.array([])   
    chancesWin=np.array([])
    chancesLose=np.array([])
    chancesTie=np.array([])
    while ff<finish:
        chance1=PossessionWin(ff,series)
        steps=np.append(steps,ff)
        chancesWin=np.append(chancesWin,chance1[0])
        chancesLose=np.append(chancesLose,chance1[1])
        chancesTie=np.append(chancesTie,chance1[2])
        ff=ff+gap
    return (steps, chancesWin, chancesLose, chancesTie)
    

#function that creates 3 of every x coordinate for graphing purposes   
def NewSteps(steps):
    newsteps=np.array([])
    gg=0
    finish=len(steps)
    while gg<finish:
        newsteps1=steps[gg]
        newsteps=np.append(newsteps, np.array([newsteps1,newsteps1,newsteps1]))
        gg=gg+1
    return newsteps

#function that creates list of where each bar should start, graphing purposes
def Bottoms(steps, chancesWin, chancesLose, chancesTie):
    bottoms=np.array([])
    hh=0
    finish=len(steps)
    while hh<finish:
        bottoms=np.append(bottoms,np.array([0,chancesWin[hh],(chancesWin[hh]+chancesTie[hh])]))
        hh=hh+1
    return bottoms

#function that creates of list of how high each bar should be, just probablities
def Heights(steps, chancesWin, chancesLose, chancesTie):
    heights=np.array([])
    jj=0
    finish=len(steps)
    while jj<finish:
        heights=np.append(heights, np.array([chancesWin[jj],chancesTie[jj],chancesLose[jj]]))
        jj=jj+1
    return heights

#just creates list of colors, g=win, gray=tie, r=lose
def Colors(steps):
    colors=np.array([])
    kk=0
    length=len(steps)
    while kk<length:
        colors=np.append(colors,np.array(['g','gray','r']))
        kk=kk+1
    return colors
    
#compiles all graphing information
def FINAL(series) :    
    seriessteps=NewSteps(series[0])
    seriesbottoms=Bottoms(series[0],series[1],series[2],series[3])
    seriesheights=Heights(series[0],series[1],series[2],series[3])
    seriescolors=Colors(series[0])
    return (seriessteps,seriesheights,seriesbottoms,seriescolors)
    
#MAIN PROGRAM
    
print("Welcome to the World Cup 2018 Statistic Program!")
print("1. Ball Possession")
print("2. Attempts")
print("3. On-Target")
print("4. Free Kicks")
print("5. Blocked")
print("6. Saves")
print("7. Pass Accuracy")
print("8. Passes")
print("9. Distance Covered (Kms)")
print("10. Fouls Committed")
print("11. Offsides")
print("12. Corners")
Stat=int(input("Choose a statistic: "))
START=int(input("Choose a start: "))
FINISH=int(input("Choose a finish: "))
Gap=int(input("Choose a gap: "))


if Stat==1:
    WhichSeries=LOOP(START,FINISH,Possession,Gap)
elif Stat==2:
    WhichSeries=LOOP(START,FINISH,Attempts,Gap)
elif Stat==3:
    WhichSeries=LOOP(START,FINISH,onTarget,Gap)
elif Stat==4:
    WhichSeries=LOOP(START,FINISH,freeKicks,Gap)
elif Stat==5:
    WhichSeries=LOOP(START,FINISH,Blocks,Gap)
elif Stat==6:
    WhichSeries=LOOP(START,FINISH,Saves,Gap)
elif Stat==7:
    WhichSeries=LOOP(START,FINISH,PAccuracy,Gap)
elif Stat==8:
    WhichSeries=LOOP(START,FINISH,Passes,Gap)
elif Stat==9:
    WhichSeries=LOOP(START,FINISH,DCovered,Gap)
elif Stat==10:
    WhichSeries=LOOP(START,FINISH,Fouls,Gap)
elif Stat==11:
    WhichSeries=LOOP(START,FINISH,Offsides,Gap)
elif Stat==12:
    WhichSeries=LOOP(START,FINISH,Corners,Gap)
    
#PassAccuracy=LOOP(1,16,PAccuracy,1)


#BallPossession=LOOP(1,30,Possession,1)


#ShotsonTarget=LOOP(1,8,onTarget,1)


#DistanceCovered=LOOP(1,10,DCovered,1)

#Foulscom=LOOP(1,12,Fouls,1)

#gap=20
#Passescom=LOOP(20,340,Passes,gap)

#WhichSeries=Passescom


SeriesChosen=FINAL(WhichSeries)
    
plt.bar(SeriesChosen[0], SeriesChosen[1], width=(Gap*0.8), bottom=SeriesChosen[2], align='center', color=SeriesChosen[3])
plt.xticks(WhichSeries[0])
plt.xlabel("Number of Statistic More Than Opponent")
plt.ylabel("Percentage")
plt.show



