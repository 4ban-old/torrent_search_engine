from komunist.tools import pickle_bytes
import pickle

t = [[-12, 25, 140], [12346, 34, 34343], [4321, 1111, 2222]]
print t


a = pickle_bytes.dumps(t, (3,3,5))
print a
print
print len(a), len(pickle.dumps(t))

b = pickle_bytes.loads(a)
print b
