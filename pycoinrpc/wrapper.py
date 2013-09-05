import json
from pycoin import wallet

def badarg():
  return '{"result":null,"error":"badarg","id":null}'
def nomethod(f, msgid):
  return '{"result":null,"error":"function_not_found (' + f + ')","id":"' + msgid + '"}'

def dispatch():
  return {'info': get_info }

def rpc(mpi):
  try:
    mpi = json.loads(mpi)
  except:
    return badarg()
  if not dispatch()[mpi['method']]:
    return nomethod(mpi['method'], mpi['id'])
  else:
    return reply(dispatch()[mpi['method']](mpi['params']), mpi['id'])

def get_info(params):
  chain_path = None
  source_key = None

  if(params['chain_path']):
    chain_path = params['chain_path']

  if(params['source_key']):
    source_key = params['source_key']

  return get_info_do(chain_path, source_key)

def get_info_do(chain_path, source_key):
  return "chain_path: " + chain_path + " | " + "source_key: " + source_key

def reply(result, msgid):
  return '{"result":"' + result + '","error":null,"id":"' + msgid + '"}'

if __name__ == '__main__':
  print('what are you looking at?')
  print(badarg())
  print(nomethod('herp','derp'))
  print(reply('hurr','durr'))
  print(rpc('{"method":"info","params":{"source_key":"tprv8ZgxMBicQKsPeW3EvNhpf6HxtFNx48RgzRjH3MP9G8Q4QjiH9P7NWMcDspbfBPxbj5msW3sSZAjJy65e4KDrdMydgHCj5gp6j9qEH9DvDNi","chain_path":".pub"},"id":"foo"}'))
