#!/usr/bin/python3
import random,os

def get_random_hping3_params():
    cmd=''
    optional_params=['n','q','V','z','Z','0','1','2','W','r','f','x','y','k','Q','b','F','S','R','P','A','U','X','Y','j','J','u','T','G','-rand-source']
    interval_params=[\
            {'name':'count','min':1,'max':1000,'pre':''},\
            {'name':'interval','min':0,'max':30, 'pre':'u'},\
            {'name':'ttl','min':1,'max':255, 'pre':''},\
            {'name':'fragoff','min':0,'max':8191, 'pre':''},\
            {'name':'mtu','min':68,'max':65535, 'pre':''},\
            {'name':'win','min':0,'max':65535, 'pre':''},\
            {'name':'tcpoff','min':4,'max':60, 'pre':''},\
            {'name':'icmpcode','min':0,'max':255, 'pre':''},\
            {'name':'data','min':0,'max':65495, 'pre':''},\
            ]
    discret_params=[\
            {'name': 'tos', 'values':['02','04','08','10']},\
            {'name': 'icmptype', 'values':[0,3,4,5,8,11,13,14,17,18]},\
            ]
    dependent_params=[\
            {'parent': ' --data ','name':'file','values':['/dev/random']},\
            ]
    oparams=random.sample(optional_params,random.randint(0,len(optional_params)))
    iparams=random.sample(interval_params,random.randint(0,len(interval_params)))
    dparams=random.sample(discret_params,random.randint(0,len(discret_params)))
    depparams=random.sample(dependent_params,random.randint(0,len(dependent_params)))
    for param in oparams:
        cmd=cmd+' -'+param
    for param in iparams:
        cmd=cmd+' --'+param['name']+' '+param['pre']+str(random.randint(param['min'],param['max']))
    for param in dparams:
        cmd=cmd+' --'+param['name']+' '+str(random.choice(param['values']))
    for depparam in depparams:
        if depparam['parent'] in cmd:
            cmd=cmd+' --'+depparam['name']+' '+str(random.choice(depparam['values']))
    return cmd

hostname='127.0.0.127'
cmd='hping3 -p 80 -c 1' + get_random_hping3_params()+' '+hostname
print(cmd)
os.system(cmd)
