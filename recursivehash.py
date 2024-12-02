from hashlib import sha256

def hash(value):
    return sha256(value.encode('utf-8')).hexdigest()


"""
def getcheckpoints(prevblockhash, hashsubmitted):
    checkpoints = []
    h = hash(prevblockhash + hashsubmitted)

    for i in range(0, 64, 4):
        s = h[i:i+4]
        checkpoints.append((s[:2], s[-2:]))
    return checkpoints
"""
  
class memozation:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]

def getrecurhashfunc(blockhash, startnonce=0):
    @memozation
    def recursivehash(nonce):
        if nonce == 0:
            return blockhash
        else:
            return hash(recursivehash(nonce - 1) + str(nonce+startnonce))

    return recursivehash

def verify(hash0, hash1, startnonce=0):
    f = getrecurhashfunc(hash0, startnonce)
    return f(256) == hash1

if __name__ == "__main__":
    prevblockhash = "e80b3da968979a57c449f8f8bc6f9a679602592c87918d787b6504393edeb242"

    f = getrecurhashfunc(prevblockhash)
    submit_checkpoints = []

    #for i in range(2**12):
    for i in range(2**10):
        h = f(i)

        if i % 256 == 0:
            print(str(i).zfill(10), h)
            submit_checkpoints.append(h)

    print(len(submit_checkpoints))

    submittedhash = submit_checkpoints[-1]

    assert verify(submit_checkpoints[0], submit_checkpoints[1], 0)
    assert verify(submit_checkpoints[1], submit_checkpoints[2], 256)
    assert verify(submit_checkpoints[2], submit_checkpoints[3], 512)
  