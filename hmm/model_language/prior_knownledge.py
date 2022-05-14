
shengmu = ['b' ,'p' ,'m' ,'f' ,'d' ,'t' ,'n' ,'l' ,'g' ,'k' ,'h' ,'j' ,'q' ,'x' ,'zh' ,'ch' ,'sh' ,'z' ,'c' ,'s' ,'y'
           ,'w' ,'r']
yunmu = ['a' ,'o' ,'e' ,'i' ,'u' ,'v' ,'ai' ,'ei' ,'ui' ,'ao' ,'ou' ,'iu' ,'ie' ,'ve' ,'er' ,'an' ,'en' ,'in' ,'un'
         ,'vn' ,'ang' ,'eng' ,'ing' ,'ong']
shengmu_metrix = {
    'b' :['p'],
    'p' :['b'],
    'z' :['c' ,'s'],
    'c' :['z' ,'s','ch'],
    's' :['c' ,'z','sh','x','h','f'],
    'd' :['t'],
    't' :['d'],
    'n' :['l'],
    'l' :['n'],
    'zh' :['ch' ,'sh'],
    'ch' :['zh' ,'sh','c'],
    'sh' :['zh' ,'ch','x','s','f','h'],
    'j':['q','x'],
    'q':['j','x'],
    'x':['j','q','h','sh','s','f'],
    'g':['k'],
    'k':['g'],
    'f':['s','sh','h'],
    'h':['f']
}
yunmu_metrix = {
    'en':['eng','ueng'],
    'eng':['en','ueng','ui'],
    'iu':['iao'],
    'iao':['iu','ian','ing'],
    'uo':['uan','ua','ui','u'],
    'in':['ing','ian'],
    'ing':['in'],
    'ian':['iao'],
    'i':['ie'],
    'u':['ou','o']
}














