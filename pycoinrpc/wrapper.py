import json
import binascii

from pycoin.wallet import Wallet

class Wrapper(object):
  def rpc(_self, mpi):
    try:
      mpi = json.loads(mpi)
    except:
      return badarg()
    if not dispatch().get(mpi.get('method', None), None):
      return nomethod(mpi.get('method', 'NOTSUPPLIED'), mpi.get('id', 'NOTSUPPLIED'))
    else:
      result_maybe = dispatch()[mpi.get('method', None)](mpi.get('params', None))
      if(result_maybe.get('result', None)):
        return reply(result_maybe['result'], mpi['id'])
      else:
        return error(result_maybe['error'], mpi['id'])

def badarg():
  return '{"result":null,"error":"badarg","id":null}'
def nomethod(f, msgid):
  return '{"result":null,"error":"function_not_found (' + f + ')","id":"' + msgid + '"}'

def dispatch():
  return {'info': get_info }
def vector1():
  return "000102030405060708090a0b0c0d0e0f"

def get_info(params):

  chain_path = params.get('chain_path', None)
  source_key = params.get('source_key', None)
  entropy = params.get('entropy', None)
  testnet = params.get('testnet', 0)

  return get_info_do(chain_path, source_key, entropy, testnet)

def get_info_do(chain_path, source_key, entropy, testnet):
  if(source_key == None and chain_path == None):
    if(entropy == None):
      return {'error': '"no_entropy"'}
    else:
      try: # Python 3
        w = Wallet.from_master_secret(bytes(entropy, encoding='ascii'), is_test=testnet)
        return {'result': wallet_to_json(w)}
      except: # Python 2.7
        w = Wallet.from_master_secret(bytes(entropy).encode('ascii'), is_test=testnet)
        return {'result': wallet_to_json(w)}
  elif(source_key == None):
    return {'error': '"no_source_key"'}
  else:
    w = Wallet.from_wallet_key(source_key)
    if(chain_path == None):
      return {'result': wallet_to_json(w)}
    else:
      return {'result': wallet_to_json(w.subkey_for_path(chain_path))}
  return {'error': '"unexpected (chain_path: "' + chain_path + '"; source_key: "' + source_key + '")"'}

def reply(result, msgid):
  return '{"result":' + result + ',"error":null,"id":"' + msgid + '"}'
def error(error, msgid):
  return '{"result":null,"error":' + error + ',"id":"' + msgid + '"}'

def wallet_to_json(w):
  return json.dumps(
   {'extended_key': w.wallet_key(as_private=w.is_private),
    'is_test': w.is_test,
    'is_private': w.is_private,
    'secret': w.is_private and w.secret_exponent or None,
    'public_pair': w.public_pair,
    'depth': w.depth,
    'self': b2h(w.fingerprint()),
    'parent':b2h(w.parent_fingerprint),
    'child_number': w.child_number,
    'chain_code': b2h(w.chain_code),
    'wif': w.is_private and w.wif() or None,
    'uncompressed_wif': w.is_private and w.wif(compressed=False) or None,
    'address': w.bitcoin_address(),
    'uncompressed_address': w.bitcoin_address(compressed=False)})

def b2h(b):
    return binascii.hexlify(b).decode("utf8")

if __name__ == '__main__':
  print('what are you looking at?')
  print(badarg())
  print(nomethod('herp','derp'))
  print(reply('hurr','durr'))
  print(rpc('{"method":"info","params":{"source_key":"tprv8ZgxMBicQKsPeW3EvNhpf6HxtFNx48RgzRjH3MP9G8Q4QjiH9P7NWMcDspbfBPxbj5msW3sSZAjJy65e4KDrdMydgHCj5gp6j9qEH9DvDNi","chain_path":".pub"},"id":"foo"}'))
  print(rpc('{"method":"info","params":{"entropy":"' + vector1() + '"},"id":"foo"}'))
