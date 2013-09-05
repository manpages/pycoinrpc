import json
from pycoin import wallet

def badarg():
  return '{"result":null,"error":"badarg","id":null}'
def nomethod(f, msgid):
  return '{"result":null,"error":"function_not_found (' + f + ')","id":"' + msgid + '"}'

def dispatch():
  return {'priv': get_priv,
          'pub':  get_pub}

def rpc(mpi):
  try:
    mpi = json.loads(mpi)
  except:
    return badarg()
  if not dispatch()[mpi['method']]:
    return nomethod(mpi['method'], mpi['id'])
  else:
    return reply(dispatch()[mpi['method']](mpi['params']), mpi['id'])

def get_priv(params):
  return "tprivXXX"

def get_pub(params):
  return "tpubYYY"

def reply(result, msgid):
  return '{"result":"' + result + '","error":null,"id":"' + msgid + '"}'

if __name__ == '__main__':
  print('what are you looking at?')
  print(badarg())
  print(nomethod('herp','derp'))
  print(reply('hurr','durr'))
  print(rpc('{"method":"priv","params":{"name":"value"},"id":"foo"}'))
