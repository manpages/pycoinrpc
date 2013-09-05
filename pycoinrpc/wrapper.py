import json
import binascii

from pycoin.wallet import Wallet

class Wrapper(object):
  def rpc(mpi):
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
      w = Wallet.from_master_secret(bytes(entropy, encoding='ascii'), is_test=testnet)
      return {'result': wallet_to_json(w)}
  return {'result': "chain_path: " + chain_path + " | " + "source_key: " + source_key}

def reply(result, msgid):
  return '{"result":' + result + ',"error":null,"id":"' + msgid + '"}'
def error(error, msgid):
  return '{"result":null,"error":' + error + ',"id":"' + msgid + '"}'

def wallet_to_json(w):
  return json.dumps(
   {'is_test': w.is_test,
    'is_private': w.is_private,
    'secret': w.secret_exponent if w.is_private else None,
    'public_pair': w.public_pair,
    'depth': w.depth,
    'self': b2h(w.fingerprint()),
    'parent':b2h(w.parent_fingerprint),
    'child_number': w.child_number,
    'chain_code': b2h(w.chain_code),
    'wif': w.wif() if w.is_private else None,
    'uncompressed_wif': w.wif(compressed=False),
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
