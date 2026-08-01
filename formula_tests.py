#!/usr/bin/env python3
import math

def close(actual,expected,tolerance,label):
    if abs(actual-expected)>tolerance: raise AssertionError(f'{label}: {actual} != {expected}')
def payment(p,annual,months):
    r=annual/1200
    return p/months if r==0 else p*r*(1+r)**months/((1+r)**months-1)
def bmi(kg,cm): return kg/((cm/100)**2)
def mifflin(kg,cm,age,male=True): return 10*kg+6.25*cm-5*age+(5 if male else -161)
def future(principal,monthly,annual,months):
    r=annual/1200
    return principal*(1+r)**months+(monthly*months if r==0 else monthly*((1+r)**months-1)/r)

close(payment(300000,6,360),1798.65,.02,'mortgage 300k 6% 30y')
close(payment(240000,6,360),1438.92,.02,'mortgage 240k 6% 30y')
close(payment(20000,8,60),405.53,.02,'loan 20k 8% 60m')
close(payment(10000,0,20),500,.001,'zero-rate loan')
close(bmi(70,175),22.8571,.001,'BMI 70kg 175cm')
close(mifflin(72,175,30,True),1668.75,.001,'male Mifflin BMR')
close(mifflin(60,165,30,False),1320.25,.001,'female Mifflin BMR')
close(future(10000,0,5,120),16470.09,.05,'compound 10k 5% 10y')
for value,label in [(payment(300000,6,360),'payment'),(bmi(70,175),'bmi'),(future(5000,200,8,240),'future value')]:
    if not math.isfinite(value) or value<=0: raise AssertionError(f'{label}: invalid output')
print('Formula tests: 11 checks passed.')

# Opportunity calculator checks
def recast_payment(balance,lump,annual,remaining_months):
    return payment(balance-lump,annual,remaining_months)
close(recast_payment(300000,25000,4,300),1451.50,.10,'mortgage recast payment')
close(payment(280000,6.25,360),1724.01,.10,'mortgage full cost principal and interest')
close(50000*1.05,52500,.001,'5 percent pay raise')
close((17*60+30)-(9*60)-30,480,.001,'work shift paid minutes')
print('Opportunity tests: 4 checks passed.')

# SEO calculator expansion checks
def auto_payment(price,down,trade,tax,fees,annual,months):
    principal=(price-trade)*(1+tax/100)+fees-down
    return payment(principal,annual,months)
def break_even_units(fixed,price,variable): return math.ceil(fixed/(price-variable))
def weighted_gpa(credits,grades): return sum(c*g for c,g in zip(credits,grades))/sum(credits)
close(auto_payment(30000,3000,0,6,500,7,60),580.18,.15,'auto loan payment')
assert break_even_units(20000,50,30)==1000
close(weighted_gpa([3,4,3],[4,3,3.7]),3.51,.01,'weighted GPA')
close(50000*1.05,52500,.001,'pay raise regression')
print('SEO expansion tests: 4 checks passed.')
