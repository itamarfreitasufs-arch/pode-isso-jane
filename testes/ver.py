import json,sys
for x in json.load(open(sys.argv[1])):
    if len(sys.argv)>2 and x['id'] not in sys.argv[2:]: continue
    print('==',x['id'],x['perfil'] or '-','|',x['q'][:110],'→',x['tipo'],x['ids'])
    print('   S:',x['status'][:230])
    for f in x['fichas']: print('   F:',f[:150])
    if x['erro']: print('   ERRO',x['erro'][:300])
