
import time
start=time.clock()
print "Evaluating fenvs.py.."

#default values (see PlasmConfig)
DEFAULT_TOLERANCE=1e-6
DEFAULT_MAX_NUM_SPLIT=10
DEFAULT_USE_OCTREE_PLANES=True

import sys,types,math

# set this to True if you want to do a self test
self_test=False

print __file__

from pyplasm.xge import *

	
#===================================================== 
# Configuration for plasm
#
# EXAMPLE:
# plasm_config.push(<tolerance you want to use::float>)
# <your code>
# plasm_config.pop()
#
#===================================================== 
class PlasmConfig:

	def __init__(self):
		self.stack=[]
		self.push(DEFAULT_TOLERANCE,DEFAULT_MAX_NUM_SPLIT,DEFAULT_USE_OCTREE_PLANES)

	# return actual tolerance
	def tolerance(self):
		return self.stack[-1].tolerance

	# return actual num try
	def maxnumtry(self):
		return self.stack[-1].maxnumtry
		
	def useOctreePlanes(self):
		return self.stack[-1].useoctreeplanes

	# push a config
	def push(self,tolerance,maxnumtry=-1,useoctreeplanes=True):
		class T:pass
		obj=T()
		obj.tolerance=tolerance
		obj.maxnumtry=maxnumtry if maxnumtry>=0 else self.maxnumtry()
		obj.useoctreeplanes=useoctreeplanes
		self.stack+=[obj]

	# pop a config
	def pop(self):
		if len(self.stack)==1:
			raise Exception("Cannot pop the default configuration")
		self.stack=self.stack[:-1]

plasm_config=PlasmConfig()


#===================================================== 
# Every
#===================================================== 
def every (predicate, iterable):
    for x in iterable:
        if not(predicate(x)):return False
    return True



if self_test: 
	assert(every(lambda x: x>=0,[1,2,3,4]) and not every(lambda x: x>0,[1,-2,3,4]))

#===================================================== 
# from http://www.daniweb.com/code/snippet564.html
#===================================================== 
def curry(fn, *cargs, **ckwargs):
    def call_fn(*fargs, **fkwargs):
        d = ckwargs.copy()
        d.update(fkwargs)
        return fn(*(cargs + fargs), **d)
    return call_fn

def C (fun):
    return lambda arg1: lambda arg2: fun([arg1,arg2])


#===================================================== 
# Define CONStants
#===================================================== 
PI = math.pi
SIN = math.sin
SINH = math.sinh
ASIN = math.asin
COS = math.cos
COSH = math.cosh
ACOS = math.acos
TAN = math.tan

TANH = math.tanh
ATAN = math.atan
ATAN2 = math.atan2
SQRT = math.sqrt
EXP = math.exp
LN = math.log
CEIL = math.ceil
FLOOR = math.floor
ABS = abs
CHAR = chr
ORD = ord
FALSE = False
TRUE = True


def ATAN2(l): 
	return math.atan2(l[1],l[0])


def MOD(l): 
	return float(l[0] % l[1])

# ===================================================== 
# CAT
# =====================================================

def CAT (args):  return reduce(lambda x, y: x + y, args)

if self_test: 
	assert(CAT([[1,2],[3,4]])==[1,2,3,4])



# ===================================================== 
# Matrix inverse
# ===================================================== 

def INV (mat):
    dim=len(mat)
    mat=Matf(CAT(mat)).invert()
    return [ [mat.get(i,j) for j in range(0,dim) ] for i in range(0,dim) ]



if self_test: 
	assert((Matf([1,2,3,4])*Matf(CAT(INV([[1,2],[3,4]]))) ).almostIdentity(0.01))

# ===================================================== 
# AND
# =====================================================
 
def AND (list):
    """ and of all arguments in a list """
    for i in list:
        if not(i):return False
    return True



if self_test: 
	assert(AND([True,True])==True and AND([True,False])==False)

#===================================================== 
# hpc type
#===================================================== 

pol_type = Hpc

def is_polyhedra_complex (obj):
    return isinstance(obj, pol_type)

def ISPOL (obj):
    return isinstance(obj, pol_type)

if self_test: 
	assert(ISPOL(Plasm.cube(2))==True)

#===================================================== 
# FL IDentity Function 
#===================================================== 

def ID (anyValue):
    """IDentity function. For any argument retruns the argument"""
    return anyValue

if self_test: 
	assert(ID(True)==True)


#===================================================== 
# FL CONStant Function 
#===================================================== 

def K(AnyValue):
    def K0 (obj): return AnyValue
    return K0



TT = K(TRUE)

if self_test: 
	assert(K(1)(2)==1)

# ===================================================
# DISTL
# ===================================================

def DISTL(args):
    Element, List = args
    return [ [Element, e] for e in List ]
    


if self_test: 
	assert(DISTL([1,[2,3,4]])==[[1,2],[1,3],[1,4]])

# ===================================================
# DISTR
# ===================================================

def DISTR(args):
    List, Element = args
    return [ [e,Element] for e in List ]



if self_test: 
	assert(DISTR([[1,2,3],0])==[[1,0],[2,0],[3,0]])


# ===================================================
# Composition
# ===================================================

def COMP(Funs):
   def compose(f,g):
      def h(x): return f(g(x))
      return h
   return reduce(compose,Funs)



if self_test: 
	assert(COMP([lambda x: x+[3],lambda x: x+[2],lambda x: x+[1]])([0])==[0,1,2,3])


# ===================================================
# Apply-to-all 
# ===================================================

def AA (f):
    def AA0 (args): return map(f, args)
    return AA0



if self_test: 
	assert(AA(lambda x: x*2)([1,2,3])==[2,4,6])



# ===================================================
# PLASM  Comparison operators 
# ===================================================

def Eq (x,y): return x == y

def EQ(List):
    for i in List:
       if not i==List[0]: return False
    return True

def NEQ(List): 
    return not EQ(List)


if self_test: 
	assert(EQ([1,1,1]) and not EQ([1,1,2]))
	assert(NEQ([1,1,2])==True and NEQ([1,1,2/2])==False)

def LT (a):return lambda b: b<a
def LE (a):return lambda b: b<=a
def GT (a):return lambda b: b>a
def GE (a):return lambda b: b>=a

if self_test: assert(LT(2)(1) and LE(2)(2) and  GT(2)(3) and  GE(2)(2))

def ISGT (args):A , B = args;return GT(A)(B)
def ISLT (args):A , B = args;return LT(A)(B)
def ISGE (args):A , B = args;return GE(A)(B)
def ISLE (args):A , B = args;return LE(A)(B)


def BIGGER (args): 
	A , B = args
	return A if A>=B else B

def SMALLER (args):
	A , B = args
	return A if A<=B else B


# ===================================================
# FILTER
# ===================================================

def FILTER(predicate):
	def FILTER0(sequence):
		ret=[]
		for item in sequence:
			if predicate(item): ret+=[item]
		return ret
	return FILTER0

if self_test:
	assert FILTER(LE(0))([-1,0,1,2,3,4])==[-1,0]
	assert FILTER(GE(0))([-1,0,1,2,3,4])==[0,1,2,3,4]


# ===================================================
# Apply 
# ===================================================

def APPLY(args):
    f,x = args
    return apply(f,[x])



if self_test: 
	assert(APPLY([lambda x:x*2,2])==4)

# ===================================================
# INSR
# ===================================================

def INSR(f):
    def INSR0(seq):
        length=len(seq)
        res = seq[-1]
        for i in range(length - 2,-1,-1): res = f([seq[i], res])
        return res
    return INSR0 

  

if self_test: 
	assert(INSR(lambda x: x[0]-x[1])([1,2,3])==2)

# ===================================================
# INSL
# ===================================================
def INSL(f):
    def INSL0 (seq):
        res = seq[0]
        for item in seq[1:]: res = f([res,item])
        return res
    return INSL0   

   

if self_test: 
	assert(INSL(lambda x: x[0]-x[1])([1,2,3])==-4) 


# ===================================================
# CONS
# ===================================================

def CONS (Funs): return lambda x : [f(x) for f in Funs]



if self_test: 
	assert(CONS( [lambda x : x+1,lambda x : x+2])(0)==[1,2])



# ===================================================
# IF THEN ELSE purely functional 
# ===================================================

def IF (funs):
    def IF1 (arg):
        f1, f2, f3 = funs
        return f2(arg) if f1(arg) else f3(arg)
    return IF1
        
 

if self_test: 
	assert(IF([lambda x: x, K(True),K(False)])(True)==True)
	assert(IF([lambda x: x, K(True),K(False)])(False)==False)



# ===================================================
# FL LIFT and RAISE functions 
# ===================================================

def LIFT (f):
    return lambda funs: COMP([f, CONS(funs)])


def RAISE (f):
    #raise NameError('Command RAISE is available starting with Basic Plan.')
    def RAISE0 (args):
        return IF([ISSEQOF(ISFUN), LIFT(f), f])(args)
    return RAISE0



# ===================================================
# PLASM  predicates 
# ===================================================

def ISNUM (x): 
	return  isinstance(x, int) or isinstance(x, long) or  isinstance(x, float) or  isinstance(x, complex) or (sys.platform=='cli' and type(x) == System.Single)
		
		
if self_test: 
	assert(ISNUM(0.0))

def NUMBER_FROM_ZERO_TO_ONE_P (x):  return  ISNUM(x) and x >= 0 and x <= 1

def ISFUN (x): return callable(x)

if self_test: 
	assert(ISFUN(lambda x:x) and ISFUN(abs) and not ISFUN(3))

def ISNUMPOS (x): return ISNUM(x) and x > 0
def ISNUMNEG (x): return ISNUM(x) and x < 0
def ISINT (x): return isinstance(x,int)
def ISLONG (x): return isinstance(x,long)
def ISINTPOS (x): return isinstance(x,int) and x > 0
def ISINTNEG (x): return isinstance(x,int) and x < 0
def ISREAL (x): return isinstance(x,float)
def ISREALPOS (x): return isinstance(x,float) and x > 0
def ISREALNEG (x): return isinstance(x,float) and x < 0
def ISCOMPLEX (x): return isinstance(x,complex)
def ISSEQ (x): return isinstance(x,list)
def ISSEQ_NOT_VOID (x): return True if (isinstance(x,list) and (len(x) >= 1)) else False

def ISSEQOF (type_checker):
    def ISSEQOF0 (arg):
        if not isinstance(arg, list): return False
        for item in arg:
           if not type_checker(item): return False
        return True
    return ISSEQOF0

if self_test: 
	assert(ISSEQOF(lambda x: isinstance(x,int))([1,2,3])==True)
	assert(ISSEQOF(lambda x: isinstance(x,int))([1,2,3.0])==False)

def ISNULL (x): return isinstance(x,list) and len(x) == 0
def ISBOOL (x): return isinstance(x,bool)
def ISPAIR (x): return isinstance(x,list) and len(x) == 2
def ISCHAR (x): return isinstance(x,str) and len(x) == 1
def ISSTRING (x): return isinstance(x,str)
def ISMAT(x): return  isinstance(x, list) and AND([isinstance(e,list) for e in x])
def ISEVEN (N): return isinstance(N,int) and (N%2)==1
def ISNAT(N): return isinstance(N,int) and N>=0
def ISZERO(N): return N==0
def ISODD(N): return not ISEVEN(N)

if self_test: 
	assert(ISMAT([[1,2],[3,4]])==True and not ISMAT([1,2,3,4]))

def VECTSUM(vects):  return map(sum,zip(*vects))
def VECTDIFF(vects): return map(lambda l: l[0]-sum(l[1:]),zip(*vects))

if self_test: 
	assert(VECTDIFF([[10,11,12],[0,1,2],[1,1,1]])==[9,9,9])
	assert(VECTSUM([[10,11,12],[0,1,2],[1,1,1]])==[11,13,15])

def IS_PLASM_POINT_2D (obj): 
	return isinstance(obj, list) and (len(obj) == 2) 


# ===================================================
# MEANPOINT
# ===================================================

def MEANPOINT (points):
	coeff=1.0/len(points)
	return map(lambda x:coeff*x,VECTSUM(points))


if self_test:
	assert MEANPOINT([[0,0,0],[1,1,1],[2,2,2]])==[1,1,1]

# ===================================================
# n-ary addition
# ===================================================

def SUM(args):


	if isinstance(args,list) and ISPOL(args[0]): 
		return PLASM_UNION(args)
	
	if isinstance(args,list) and ISNUM(args[0]): 
		return sum(args)

	if isinstance(args,list) and isinstance((args[0]),list): 

		#matrix sum
		if isinstance(args[0][0],list):
			return AA(VECTSUM)(zip(*args))

		# vector sum
		else:
			return VECTSUM(args)

	raise Exception("\'+\' function has been applied to %s!" % repr(args))        


ADD = SUM

if self_test: 
	assert(ADD([1,2,3])==6 and ADD([[1,2,3],[4,5,6]])==[5,7,9])
	assert SUM([ [[1,2],[3,4]],  [[10,20],[30,40]],  [[100,200],[300,400]] ])==[[111,222],[333,444]]
	assert(LIFT(ADD)([math.cos,math.sin])(PI/2)==1.0)
	assert(RAISE(ADD)([1,2])==3)
	assert(RAISE(ADD)([math.cos,math.sin])(PI/2)==1.0)





# ===================================================
# n-ary DIFFerence 
# ===================================================

def PLASM_NDIFF(args):

	if isinstance(args,list) and ISPOL(args[0]): 
		return  PLASM_DIFFERENCE(args)

	if ISNUM(args): 
		return -1 * args

	if isinstance(args,list) and  ISNUM(args[0]): 
			return reduce(lambda x,y: x - y, args)

	if isinstance(args,list) and  isinstance(args[0],list): 

		#matrix difference
		if isinstance(args[0][0],list):
			return AA(VECTDIFF)(zip(*args))

		# vector diff
		else:
			return VECTDIFF(args)
	
	raise Exception("\'-\' function has been applied to %s!" % repr(args))     



if self_test: 
	assert( PLASM_DIFF(2)==-2 and  PLASM_DIFF([1,2,3])==-4 and  PLASM_DIFF([[1,2,3],[1,2,3]])==[0,0,0])

# ===================================================
# n-ary PRODuct 
# ===================================================

def PROD(args):        
    raise NameError('Command PROD is available starting with Basic Plan.')
    if isinstance(args,list) and ISPOL(args[0]): return  PLASM_POWER(args)
    if isinstance(args,list) and ISSEQOF(ISNUM)(args): return reduce(lambda x,y: x * y, args)
    if isinstance(args,list) and len(args) == 2 and ISSEQOF(ISNUM)(args[0]) and ISSEQOF(ISNUM)(args[1]): return  Vecf(args[0])*Vecf(args[1])
    raise Exception("PROD function has been applied to %s!" % repr(args))



if self_test: 
	assert(PROD([1,2,3,4])==24 and PROD([[1,2,3],[4,5,6]])==32)

SQR = RAISE(RAISE(PROD))([ID,ID])


# ===================================================
# n-ary DIVision 
# ===================================================

def DIV(args):
    return reduce(lambda x,y: x/float(y), args)


if self_test: 
	assert(DIV([10,2,5])==1.0)

# ===================================================
# REVERSE
# ===================================================

def REVERSE(List): 
   ret=[x for x in List]
   ret.reverse()
   return ret



if self_test: 
	assert(REVERSE([1,2,3])==[3,2,1] and REVERSE([1])==[1] )

LEN = len


# ===================================================
# TRANS
# ===================================================

def TRANS (List): 
	return map(list, zip(*List))


if self_test: 
	assert(TRANS([[1,2],[3,4]])==[[1,3],[2,4]])

def FIRST (List): return List[0]
def LAST (List): return List[-1]
def TAIL (List): return List[1:]
def RTAIL (List): return List[:-1]
def AR (args): return args[0] + [args[-1]]
def AL (args): return [args[0]] + args[-1]
def LIST(x): return [x]


if self_test: 
	assert(AR([ [1,2,3],0,])==[1,2,3,0])

if self_test: 
	assert(AL([ 0,[1,2,3]])==[0,1,2,3])


# ===================================================
# FL CONStruction 
# ===================================================

greater=max
BIGGEST=max
SMALLEST = min


if self_test: 
	assert(greater(1,2)==2 and BIGGEST([1,2,3,4])==4)
	

# ===================================================
# PLASM  logical operators 
# ===================================================

And=all
AND=And 
Or=any
OR=Or

def Not(x): 
	return not x

NOT = AA(Not) 

if self_test: 
	assert(AND ([True,True,True])==True and AND ([True,False,True])==False)
	assert(OR ([True,False,True])==True and OR ([False,False,False])==False)


# ===================================================
# PROGRESSIVESUM
# ===================================================

def PROGRESSIVESUM(arg):
	ret,acc=[],0
	for value in arg:
		acc+=value
		ret+=[acc]
	return ret



if self_test:
	assert PROGRESSIVESUM([1,2,3,4])==[1,3,6,10]

# ===================================================
# PLASM range builders 
# ===================================================

def INTSTO (n): 
    return range(1,n+1)


if self_test: 
	assert(INTSTO(5)==[1,2,3,4,5])


def FROMTO (args):   
    return range(args[0],args[-1]+1)


if self_test: 
	assert(FROMTO ([1,4])==[1,2,3,4])

# ===================================================
# PLASM  selectors
# ===================================================

def SEL (n): 
    return lambda lista: lista[int(n)-1]


S1 = SEL(1)
S2 = SEL(2)
S3 = SEL(3)
S4 = SEL(4)
S5 = SEL(5)
S6 = SEL(6)
S7 = SEL(7)
S8 = SEL(8)
S9 = SEL(9)
S10 = SEL(10)

if self_test: 
	assert(S1([1,2,3])==1 and S2([1,2,3])==2)

# ===================================================
# PLASM  repeat operators 
# ===================================================

def N (n): 
    """
    N: Standard core of PyPLaSM
    repetition operator. Returns the sequence with n repetitions of arg
    (n::isintpos)(arg::tt) -> (isseq)
    """
    return lambda List: [List]*int(n)


if self_test: 
	assert(N(3)(10)==[10,10,10])

def DIESIS (n): 
    """
    N: Standard core of PyPLaSM
    repetition operator. Returns the sequence with n repetitions of arg
    (n::isintpos)(arg::tt) -> (isseq)
    """
    return lambda List: [List]*int(n)


if self_test: 
	assert(DIESIS(3)(10)==[10,10,10])

def NN (n): 
    """
    NN:   Standard core of PyPLaSM
    sequence repetition operator. Returns the sequence CAT(N(seq))
    (n::isintpos)(seq::tt) -> (isseq)
    """
    return lambda List: List*int(n)


if self_test: 
	assert(NN (3)([10])==[10,10,10])


def DOUBLE_DIESIS (n): 
    """
    NN:   Standard core of PyPLaSM
    sequence repetition operator. Returns the sequence CAT(N(seq))
    (n::isintpos)(seq::tt) -> (isseq)
    """
    return lambda List: List*int(n)

# NEW DEFINITION:
def REPEAT(n, args):
    return DOUBLE_DIESIS(n)(args)

if self_test: 
	assert(DOUBLE_DIESIS  (3)([10])==[10,10,10])



# ===================================================
# Curryfing function 
# ===================================================

def C (fun):
    return lambda arg1: lambda arg2: fun([arg1,arg2])

# ===================================================
# Miscellanea (1/3) of "standard" functions 
# ===================================================

def AS(fun):
    return lambda args: COMP([CONS, AA(fun)])(args)


if self_test: assert(AS(SEL)([1,2,3])([10,11,12])==[10,11,12])

def AC(fun):
    return lambda args: COMP(AA(fun)(args))


if self_test: assert(AC(SEL)([1,2,3])([10,11,[12,[13]]])==13)

def CHARSEQ (String):
    return [String[i] for i in range(len(String))]

if self_test: assert(CHARSEQ('hello')==['h','e','l','l','o'])

def STRING (Charseq): return reduce(lambda x,y: x+y,Charseq)

if self_test: 
	assert(STRING(CHARSEQ('hello'))=='hello')

def RANGE (Pair):
    if ( (Pair[-1]-Pair[0]) >= 0 ): return range(Pair[0], Pair[-1] + 1)
    return range(Pair[0], Pair[-1] - 1, -1)



if self_test: 
	assert(RANGE ([1,3])==[1,2,3] and RANGE ([3,1])==[3,2,1])

def SIGN (Number): return +1 if Number>=0 else -1

if self_test: assert(SIGN(10)==1 and SIGN(-10)==-1)

def PRINT (AnyValue):
    print(AnyValue)
    return AnyValue


def PRINTPOL (PolValue):
    Plasm.Print(PolValue)
    sys.stdout.flush()
    return PolValue



# ===================================================
# TREE
# ===================================================

def TREE (f):
    def TREE_NO_CURRIED (fun,List):
        length = len(List)
        if length == 1: return List[0]
        k = int(len(List)/2)
        return f([TREE_NO_CURRIED(f, List[:k])] + [TREE_NO_CURRIED(f, List[k:])])
    return lambda x: TREE_NO_CURRIED(f,x)
    

if self_test: 
	assert(TREE(lambda x: x[0] if x[0]>=x[-1] else x[-1])([1,2,3,4,3,2,1])==4)
	assert(TREE(lambda x: x[0] if x[0]>=x[-1] else x[-1])([1,2,3,4,3,2])==4)

# ===================================================
# MERGE
# ===================================================

def MERGE (f):
    def MERGE_NO_CURRIED (f, List):
        list_a, list_b = List
        if len(list_a) == 0: return list_b
        if len(list_b) == 0: return list_a
        res = f(list_a[0], list_b[0])
        if not(res):
            return [list_a[0]] + MERGE_NO_CURRIED(f,[list_a[1:], list_b])
        else:
            return [list_b[0]] + MERGE_NO_CURRIED(f,[list_a, list_b[1:]])
    return lambda x: MERGE_NO_CURRIED(f,x)


if self_test: 
	assert(MERGE(lambda x,y:x>y)([[1,3,4,5],[2,4,8]])==[1,2,3,4,4,5,8])

# ===================================================
# CASE
# ===================================================

def CASE (ListPredFuns):
    def CASE_NO_CURRIED (ListPredFuns, x):
        for p in ListPredFuns:
           if p[0](x): return p[1](x)
    return lambda arg: CASE_NO_CURRIED(ListPredFuns, arg)

if self_test: 
	assert(CASE([[LT(0),K(-1)],[C(EQ)(0),K(0)],[GT(0),K(+1)]])(-10)==-1)
	assert(CASE([[LT(0),K(-1)],[C(EQ)(0),K(0)],[GT(0),K(+1)]])(   0)==0)
	assert(CASE([[LT(0),K(-1)],[C(EQ)(0),K(0)],[GT(0),K(+1)]])(10)==+1)

# ===================================================
# GEOMETRIC FUNCTION 
# ===================================================

def VIEW (obj,Background=True):
	if self_test: Background=False
	Plasm.View(obj,Background) 
	return obj


# ===================================================
# CUBOID
# ===================================================

def CUBOID (sizes_list):
    dim = len(sizes_list)
    pol = Plasm.scale(Plasm.cube(dim), Vecf([0.0] + sizes_list))
    return pol

if self_test: 
	assert(Plasm.limits(CUBOID([1,2,3]))==Boxf(Vecf(1,0,0,0),Vecf(1,1,2,3)))

def CUBE (side):
    return CUBOID([side, side, side])

def SQUARE (side):
    raise NameError('Command SQUARE is available starting with Basic Plan.')
    return CUBOID([side, side])

def SQUARE3D (a):
    raise NameError('Command SQUARE3D is available starting with Basic Plan.')
    # height is kept the same for add these thin objects,
    # so that logical operations with them work:
    h = 0.001
    return CUBOID([a, a, h])

def BRICK (a, b, c):
    raise NameError('Command BRICK is available starting with Basic Plan.')
    return
    return CUBOID([a, b, c])

def RECTANGLE (a, b):
    raise NameError('Command RECTANGLE is available starting with Basic Plan.')
    return CUBOID([a, b])

def RECTANGLE3D (a, b):
    raise NameError('Command RECTANGLE3D is available starting with Basic Plan.')
    # height is kept the same for add these thin objects,
    # so that logical operations with them work:
    h = 0.001
    return CUBOID([a, b, 0.001])

HEXAHEDRON=Plasm.cube(3,-1.0/math.sqrt(3.0),+1.0/math.sqrt(3.0))


# ===================================================
# SIMPLEX
# ===================================================

def SIMPLEX (dim):
    raise NameError('Command SIMPLEX is available starting with Basic Plan.')
    return Plasm.simplex(dim)

if self_test: 
	assert(Plasm.limits(SIMPLEX(3))==Boxf(Vecf(1,0,0,0),Vecf(1,1,1,1)))


# ===================================================
# PRINT POL
# ===================================================

def PRINTPOL (obj):
    Plasm.Print(obj)
    return obj

def PRINT(obj):
    print obj
    return obj


# ===================================================
# POL DIMENSION
# ===================================================

def RN (pol): return Plasm.getSpaceDim(pol)
def DIM (pol):return Plasm.getPointDim(pol)

def ISPOLDIM (dims):
    def ISPOLDIM1(pol):
        d = dims[0]
        n = dims[1]
        return  (d == DIM(pol)) and (n == RN(pol))
    return ISPOLDIM1

if self_test: 
	assert(RN(Plasm.cube(2))==2 and DIM(Plasm.cube(2))==2)

# ===================================================
# MKPOL
# ===================================================

def MKPOL (args_list):
   points, cells, pols = args_list
   dim = len(points[0])
   return Plasm.mkpol(dim, CAT(points), map(lambda x: [i-1 for i in x], cells),plasm_config.tolerance())

if self_test: 
	assert(Plasm.limits(MKPOL([  [[0,0],[1,0],[1,1],[0,1]] , [[1,2,3,4]] , None ]))==Boxf(Vecf(1,0,0),Vecf(1,1,1)))


# mkpol of a single point
MK = COMP([MKPOL, CONS([LIST, K([[1]]), K([[1]])])])

# convex hull of points
def PLASM_CONVEXHULL (points):
    return MKPOL([points, [range(1,len(points)+1)], [[1]]])

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
def CONVEXHULL(*args):
    raise NameError('Command CONVEXHULL is available starting with Basic Plan.')
    return PLASM_CONVEXHULL(list(args))

CHULL = CONVEXHULL
CH = CONVEXHULL

# ===================================================
# UKPOL
# ===================================================

def UKPOL (pol):  
    v= StdVectorFloat()
    u = StdVectorStdVectorInt()
    pointdim=Plasm.ukpol(pol, v, u) 
    points=[]
    for i in xrange(0, len(v), pointdim):points+=[[v[i] for i in range(i,i+pointdim)]]
    hulls=map(lambda x: [i + 1 for i in x], u)
    pols=[[1]]
    return  [points, hulls, pols]

if self_test: 
	assert(UKPOL(Plasm.cube(2))==[[[0,1],[0,0],[1,1],[1,0]],[[4,2,1,3]],[[1]]])

# return first point of a ukpol
UK = COMP([COMP([S1, S1]), UKPOL])



# ===================================================
# OPTIMIZE
# ===================================================

# not supported in new Python Plasm
def OPTIMIZE(pol): return pol

# ===================================================
# UKPOLF
# ===================================================

def UKPOLF (pol):  
	f = StdVectorFloat()
	u = StdVectorStdVectorInt()
	pointdim=Plasm.ukpolf(pol, f, u) 
	faces=[]
	for i in xrange(0, len(f), pointdim+1):
		faces+=[[f[i] for i in range(i,i+pointdim+1)]]
	hulls=map(lambda x: [i + 1 for i in x], u)
	pols=[[1]]
	return  [faces, hulls, pols]

if self_test:
	temp=UKPOLF(Plasm.cube(3))
	assert len(temp[0])==6 and len(temp[0][0])==4 and len(temp[1])==1 and len(temp[1][0])==6 and len(temp[2])==1


# ===================================================
# TRANSLATE
# ===================================================

def PLASM_TRANSLATE (axis):
    def PLASM_TRANSLATE1 (axis,values):
        def PLASM_TRANSLATE2 (axis,values,pol):
            axis    = [axis    ] if ISNUM(axis    ) else axis
            values= [values] if ISNUM(values) else values
            vt= Vecf(max(axis))
            for a,t in zip(axis,values):vt.set(a,t)
            return Plasm.translate(pol, vt)
        return lambda pol: PLASM_TRANSLATE2(axis,values,pol)    
    return lambda values: PLASM_TRANSLATE1(axis,values)
PLASM_T = PLASM_TRANSLATE


if self_test: 
	assert(Plasm.limits(PLASM_TRANSLATE([1, 2, 3])([0, 0, 2])(Plasm.cube(2)))==Boxf(Vecf(1,0,0,2),Vecf(1,1,1,2)))
	assert(Plasm.limits(PLASM_TRANSLATE([1, 2, 3])([1, 0, 2])(Plasm.cube(2)))==Boxf(Vecf(1,1,0,2),Vecf(1,2,1,2)))

# NEW DEFINITION:
def TRANSLATE(obj, t1, t2, t3):
    return PLASM_TRANSLATE([1, 2, 3])([t1, t2, t3])(obj)
T = TRANSLATE

# ===================================================
# SCALE
# ===================================================

def PLASM_SCALE (axis):
    def PLASM_SCALE1 (axis,values):
        def PLASM_SCALE2 (axis,values,pol):
            axis    = [axis    ] if ISNUM(axis    ) else axis
            values= [values] if ISNUM(values) else values
            dim=max(axis)
            vs = Vecf([1 for x in range(dim+1)]);vs.set(0,0.0)
            for a,t in zip(axis,values):vs.set(a,t)
            return Plasm.scale(pol, vs)
        return lambda pol: PLASM_SCALE2(axis,values,pol)    
    return lambda values: PLASM_SCALE1(axis,values)
PLASM_S = PLASM_SCALE

if self_test: 
	assert(Plasm.limits(PLASM_S(3)(2)(Plasm.cube(3)))==Boxf(Vecf(1,0,0,0),Vecf(1,1,1,2)))
	assert(Plasm.limits(PLASM_S([3,1])([4,2])(Plasm.cube(3)))==Boxf(Vecf(1,0,0,0),Vecf(1,2,1,4)))

# NEW DEFINITION:
def SCALE(obj, a, b, c):
    return PLASM_SCALE([1, 2, 3])([a, b, c])(obj)
S = SCALE

# ===================================================
# ROTATE
# ===================================================

def PLASM_ROTATE (plane_indexes):
    def PLASM_ROTATE1 (angle):
        def PLASM_ROTATE2 (pol):
            dim = max(plane_indexes)
            return Plasm.rotate(pol, dim, plane_indexes[0] , plane_indexes[1], angle)
        return PLASM_ROTATE2    
    return PLASM_ROTATE1
PLASM_R = PLASM_ROTATE

if self_test: 
	assert(Plasm.limits(PLASM_ROTATE([1,2])(PI/2)(Plasm.cube(2))).fuzzyEqual(Boxf(Vecf(1,-1,0),Vecf(1,0,+1))))

# NEW DEFINITION
def ROTATE(obj, axis, angle):
    if axis == 1: plane_indexes = [2, 3]
    elif axis == 2: plane_indexes = [1, 3]
    else: plane_indexes = [1, 2]
    def PLASM_ROTATE2 (pol):
        dim = max(plane_indexes)
	return Plasm.rotate(pol, dim, plane_indexes[0] , plane_indexes[1], angle)
    return PLASM_ROTATE2(obj)    

R = ROTATE
RRAD = ROTATE

def RDEG(obj, axis, angle_deg):
    angle_rad = angle_deg * PI / 180.0
    return ROTATE(obj, axis, angle_rad)

# ===================================================
#; Applica uno shearing con vettore shearing-vector-list sulla variabile
#; i-esima del complesso poliedrale pol-complex
# ===================================================

def SHEARING (i):
    def SHEARING1 (shearing_vector_list):
        def SHEARING2 (pol):
            raise Exception("shearing not implemented!")
        return SHEARING2    
    return SHEARING1
H = SHEARING
       
# ===================================================
# generic matrix
# ===================================================
def MAT (matrix):
    def MAT0 (pol):
        vmat= Matf(CAT(matrix))
        return Plasm.transform(pol,vmat,vmat.invert() )
    return MAT0   

if self_test: 
	assert(Plasm.limits(MAT([[1,0,0],[1,1,0],[2,0,1]])(Plasm.cube(2)))==Boxf(Vecf(1,1,2),Vecf(1,2,3)))

# ===================================================
# EMBED
# ===================================================

def EMBED (up_dim):
    def EMBED1 (pol):
        new_dim_pol = Plasm.getSpaceDim(pol) + up_dim
        return Plasm.embed(pol,new_dim_pol)
    return EMBED1    

# NEW DEFINITION:
def FOOTPRINT(obj):
    return EMBED(1)(BOX([1,2])(obj))

# ===================================================
# STRUCT
# ===================================================

def PLASM_STRUCT(seq,nrec=0):

	if not isinstance(seq,list) : 
		raise Exception("PLASM_STRUCT must be applied to a list")
	
	if (len(seq)==0):
		raise Exception("PLASM_STRUCT must be applied to a non-empty list")
	
	# avoid side effect
	if (nrec==0): seq=[x for x in seq] 
	
	# accumulate pols without transformations
	pols=[]
	while len(seq)>0 and ISPOL(seq[0]):
		pols+=[seq[0]]; seq=seq[1:]
	
	# accumulate transformations for pols
	transformations=[]
	while len(seq)>0 and ISFUN(seq[0]): 
		transformations+=[seq[0]]; seq=seq[1:]
	
	# avoid deadlock, i.e. call the recursion on invalid arguments
	if len(seq)>0 and not ISPOL(seq[0]) and not ISFUN(seq[0]):
		raise Exception("PLASM_STRUCT arguments not valid, not all elements are polygons or transformations")
	
	if len(seq)>0:
		assert ISPOL(seq[0]) # eaten all trasformations, the next must be a pol!
		child=PLASM_STRUCT(seq,nrec+1)
		assert ISPOL(child)
		if (len(transformations)>0): child=COMP(transformations)(child)
		pols+=[child]
	
	if len(pols)==0:
		raise Exception("Cannot find geometry in PLASM_STRUCT, found only transformations")
	
	return Plasm.Struct(pols)     

if self_test: 
	assert(Plasm.limits(PLASM_STRUCT([Plasm.cube(2)  ,  PLASM_TRANSLATE([1, 2, 3])([1, 1, 0]) ,  PLASM_TRANSLATE([1, 2, 3])([1, 1, 0]) ,  Plasm.cube(2),Plasm.cube(2,1,2)  ])).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,4,4))))
	assert(Plasm.limits(PLASM_STRUCT([ PLASM_TRANSLATE([1, 2, 3])([1, 1, 0]), PLASM_TRANSLATE([1, 2, 3])([1, 1, 0]), Plasm.cube(2)  ,  PLASM_TRANSLATE([1, 2, 3])([1, 1, 0])  ,PLASM_TRANSLATE([1, 2, 3])([1, 1, 0]),  Plasm.cube(2),Plasm.cube(2,1,2)  ])).fuzzyEqual(Boxf(Vecf(1,2,2),Vecf(1,6,6))))

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
def STRUCT(*args):
    raise NameError('Command STRUCT is available starting with Basic Plan.')
    return PLASM_STRUCT(list(args))

# ===================================================
# BOOLEAN OP
# ===================================================

#also +, or SUM, can be used to indicates UNION
def PLASM_UNION(objs_list):
        return Plasm.boolop(BOOL_CODE_OR, objs_list,plasm_config.tolerance(),plasm_config.maxnumtry(),plasm_config.useOctreePlanes())

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
def UNION(*args):
    return PLASM_UNION(list(args))

U = UNION


#also ^ can be used to indicates INTERSECTION
def PLASM_INTERSECTION (objs_list):
        return Plasm.boolop(BOOL_CODE_AND, objs_list,plasm_config.tolerance(),plasm_config.maxnumtry(),plasm_config.useOctreePlanes())
PLASM_I = PLASM_INTERSECTION

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
def INTERSECTION(*args):
    return PLASM_INTERSECTION(list(args))
I = INTERSECTION


#also -, or DIFF, can be used to indicates DIFFERENCE
def PLASM_DIFFERENCE (objs_list):
        return Plasm.boolop(BOOL_CODE_DIFF, objs_list,plasm_config.tolerance(),plasm_config.maxnumtry(),plasm_config.useOctreePlanes())
PLASM_DIFF = PLASM_DIFFERENCE        


# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
def DIFFERENCE(*args):
    return PLASM_DIFFERENCE(list(args))
DIFF = DIFFERENCE

# xor
def PLASM_XOR(objs_list):
        return Plasm.boolop(BOOL_CODE_XOR, objs_list,plasm_config.tolerance(),plasm_config.maxnumtry(),plasm_config.useOctreePlanes())

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
def XOR(*args):
    return PLASM_XOR(list(args))

if self_test: 
	assert(Plasm.limits(PLASM_UNION([Plasm.cube(2,0,1),Plasm.cube(2,0.5,1.5)])).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,1.5,1.5))))
	assert(Plasm.limits(PLASM_INTERSECTION([Plasm.cube(2,0,1),Plasm.cube(2,0.5,1.5)])).fuzzyEqual(Boxf(Vecf(1,0.5,0.5),Vecf(1,1,1))))
	assert(Plasm.limits(PLASM_DIFFERENCE([Plasm.cube(2,0,1),Plasm.cube(2,0.5,1.5)])).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,1,1))))
	assert(Plasm.limits(PLASM_XOR([Plasm.cube(2,0,1),Plasm.cube(2,0.5,1.5)])).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,1.5,1.5))))


# ===================================================
# JOIN
# ===================================================
def PLASM_JOIN (pol_list):
   if  ISPOL(pol_list): pol_list=[pol_list]
   return Plasm.join(pol_list,plasm_config.tolerance())
   
if self_test: 
	assert(Plasm.limits(PLASM_JOIN([Plasm.cube(2,0,1)])).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,1,1))))

# NEW DEFINITION (ALLOWS OMITTING BRACKETS FOR TWO OBJECTS)
def JOIN(a, b = None):
    raise NameError('Command JOIN is available starting with Basic Plan.')
    if b != None:
        return PLASM_JOIN([a, b])
    else: # single argument must be list
        return PLASM_JOIN(a)


# ===================================================
# also ** can be used to indicates POWER
# ===================================================
def PLASM_POWER (objs_list):
     
     if not isinstance(objs_list,list) or len(objs_list)!=2:
        raise Exception("POWER can only be applied to a list of 2 arguments") 

     if ISNUM(objs_list[0]) and ISNUM(objs_list[1]):
        return math.pow(objs_list[0], objs_list[1])

     return Plasm.power(objs_list[0], objs_list[1])
        
if self_test: 
	assert(PLASM_POWER([2,2])==4)
	assert(Plasm.limits(PLASM_POWER([Plasm.cube(2),Plasm.cube(1)])).fuzzyEqual(Boxf(Vecf(1,0,0,0),Vecf(1,1,1,1))))

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
def POWER(*args):
    raise NameError('Command POWER is available starting with Basic Plan.')
    return PLASM_POWER(list(args))



# ===================================================
# Skeleton
# ===================================================
def SKELETON (ord):
    def SKELETON_ORDER (pol):
        return Plasm.skeleton(pol, ord)
    return SKELETON_ORDER

SKEL_0 =  SKELETON(0)
SKEL_1 =  SKELETON(1)
SKEL_2 =  SKELETON(2)
SKEL_3 =  SKELETON(3)
SKEL_4 =  SKELETON(4)
SKEL_5 =  SKELETON(5)
SKEL_6 =  SKELETON(6)
SKEL_7 =  SKELETON(7)
SKEL_8 =  SKELETON(8)
SKEL_9 =  SKELETON(9)

if self_test: 
	assert( Plasm.limits(SKELETON(0)(Plasm.cube(2))).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,1,1))) )


# ===================================================
# GRID
# ===================================================

def GRID (sequence):
    cursor,points,hulls= (0,[[0]],[])
    for value in sequence:
        points = points + [[cursor + abs(value)]] 
        if value>=0: hulls += [[len(points)-2,len(points)-1]]
        cursor = cursor + abs(value)
    return  Plasm.mkpol(1, CAT(points), hulls,plasm_config.tolerance())   

QUOTE = GRID

if self_test: 
	assert(Plasm.limits(QUOTE([1,-1,1]))==Boxf(Vecf([1,0]),Vecf([1,3])))
	assert(Plasm.limits(QUOTE([-1,1,-1,1]))==Boxf(Vecf([1,1]),Vecf([1,4])))


Q = COMP([QUOTE, IF([ISSEQ, ID, CONS([ID])])])

# ===================================================
# INTERVALS 
# ===================================================

def PLASM_INTERVALS (A):
    def PLASM_INTERVALS0 (N):
        return QUOTE([float(A)/float(N) for i in range(N)])
    return PLASM_INTERVALS0

if self_test:
    assert Plasm.limits(PLASM_INTERVALS(10)(8))==Boxf(Vecf([1,0]),Vecf([1,10]))

# NEW DEFINITION:
def INTERVALS(a, n):
    return PLASM_INTERVALS(a)(n)

# NEW COMMAND FOR REFERENCE DOMAIN:
def REF_DOMAIN(a, b, n, m):
    return POWER(INTERVALS(a, n), INTERVALS(b, m))

def UNIT_SQUARE(n, m):
    return POWER(INTERVALS(1.0, n), INTERVALS(1.0, m))

# ===================================================
# SIZE
# ===================================================

def PLASM_SIZE (List):
    def PLASM_SIZE1 (pol): 
        size = Plasm.limits(pol).size()
        return [size[i] for i in List] if isinstance(List,list) else size[List]
    return PLASM_SIZE1

if self_test: 
	assert(PLASM_SIZE(1)(Plasm.cube(2))==1)
	assert(PLASM_SIZE([1,3])(PLASM_SCALE([1, 2, 3])([1, 2, 3])(Plasm.cube(3)))==[1,3])

# NEW_DEFINITION:
def SIZE(pol, List):
    return PLASM_SIZE(List)(pol)

# ===================================================
# MIN/MAX/MID
# ===================================================
def MIN  (List):
    def MIN1 (pol):
        box = Plasm.limits(pol)
        return [box.p1[i] for i in List] if isinstance(List,list) else box.p1[List]
    return MIN1
    
def MAX  (List):
    def MAX1 (pol):
        box = Plasm.limits(pol)
        return [box.p2[i] for i in List] if isinstance(List,list) else box.p2[List]
    return MAX1


def MID  (List):
    def MID1 (pol):
        center = Plasm.limits(pol).center()
        return [center [i] for i in List] if isinstance(List,list) else center[List]
    return MID1

if self_test: 
	assert(MIN(1)(Plasm.cube(2))==0)
	assert(MIN([1,3])(PLASM_TRANSLATE([1, 2, 3])([10, 20, 30])(Plasm.cube(3)))==[10,30])
	assert(MAX(1)(Plasm.cube(2))==1)
	assert(MAX([1,3])(PLASM_TRANSLATE([1, 2, 3])([10, 20, 30])(Plasm.cube(3)))==[11,31])
	assert(MID(1)(Plasm.cube(2))==0.5)
	assert(MID([1,3])(Plasm.cube(3))==[0.5,0.5])



# ======================================
# identity matrix
# ======================================
def IDNT (N):
    return [ [ 1 if r==c else 0 for c in range(0,N) ] for r in range(0,N)]

if self_test: 
	assert(IDNT(0)==[] and IDNT(2)==[[1,0],[0,1]])

# =============================================
# split 2PI in N parts
# =============================================

def SPLIT_2PI(N):
   delta=2*PI/N
   return [i*delta for i in range(0,N)]

if self_test: 
	assert(SPLIT_2PI(4)[2]==PI)

# =============================================
# alignment
# =============================================

def PLASM_ALIGN (args):
    def PLASM_ALIGN0 (args,pols):
        pol1 , pol2 = pols
        box1,box2=(Plasm.limits(pol1),Plasm.limits(pol2))
        if isinstance(args,list) and len(args)>0 and ISNUM(args[0]): 
                args=[args] # if I get something like [index,pos1,pos2]... i need [[index,pos1,pos2],[index,pos1,pos2],...]
        max_index=max([index for index,pos1,po2 in args])
        vt=Vecf(max_index) 
        for index,pos1,pos2 in args:
                p1=box1.p1 if pos1 is MIN else (box1.p2 if pos1 is MAX else box1.center());p1=p1[index] if index<=p1.dim else 0.0
                p2=box2.p1 if pos2 is MIN else (box2.p2 if pos2 is MAX else box2.center());p2=p2[index] if index<=p2.dim else 0.0                
                vt.set(index,vt[index]-(p2-p1))
        return Plasm.Struct([pol1,Plasm.translate(pol2,vt)])
    return lambda pol: PLASM_ALIGN0(args,pol)

PLASM_TOP = PLASM_ALIGN([[3, MAX, MIN], [1, MID, MID], [2, MID, MID]])
PLASM_BOTTOM = PLASM_ALIGN([[3, MIN, MAX], [1, MID, MID], [2, MID, MID]])
PLASM_LEFT = PLASM_ALIGN([[1, MIN, MAX], [3, MIN, MIN]])
PLASM_RIGHT = PLASM_ALIGN([[1, MAX, MIN], [3, MIN, MIN]])
PLASM_UP = PLASM_ALIGN([[2, MAX, MIN], [3, MIN, MIN]])
PLASM_DOWN = PLASM_ALIGN([[2, MIN, MAX], [3, MIN, MIN]])

if self_test: 
   assert(Plasm.limits(ALIGN([3,MAX,MIN])([Plasm.cube(3),Plasm.cube(3)]))==Boxf(Vecf(1,0,0,0),Vecf(1,1,1,2)))
   assert(Plasm.limits(PLASM_TOP([Plasm.cube(3),Plasm.cube(3)]))==Boxf(Vecf(1,0,0,0),Vecf(1,1,1,2)))
   assert(Plasm.limits(PLASM_BOTTOM([Plasm.cube(3),Plasm.cube(3)]))==Boxf(Vecf(1,0,0,-1),Vecf(1,1,1,1)))
   assert(Plasm.limits(PLASM_LEFT([Plasm.cube(3),Plasm.cube(3)]))==Boxf(Vecf(1,-1,0,0),Vecf(1,1,1,1)))
   assert(Plasm.limits(PLASM_RIGHT([Plasm.cube(3),Plasm.cube(3)]))==Boxf(Vecf(1,0,0,0),Vecf(1,2,1,1)))
   assert(Plasm.limits(PLASM_UP([Plasm.cube(3,0,1),Plasm.cube(3,5,6)]))==Boxf(Vecf(1,0,0,0),Vecf(1,6,2,1)))
   assert(Plasm.limits(PLASM_DOWN([Plasm.cube(3,0,1),Plasm.cube(3,5,6)]))==Boxf(Vecf(1,0,-1,0),Vecf(1,6,1,1)))

# NEW DEFINITIONS:
def TOP(pol1, pol2):
    return PLASM_TOP([pol1, pol2])
def BOTTOM(pol1, pol2):
    return PLASM_BOTTOM([pol1, pol2])
def LEFT(pol1, pol2):
    return PLASM_LEFT([pol1, pol2])
def RIGHT(pol1, pol2):
    return PLASM_RIGHT([pol1, pol2])
def UP(pol1, pol2):
    return PLASM_UP([pol1, pol2])
def DOWN(pol1, pol2):
    return PLASM_DOWN([pol1, pol2])

def ALIGN(obj1, obj2, align1 = None, align2 = None, align3 = None):
    L = []
    if align1 != None: L.append(align1) 
    if align2 != None: L.append(align2) 
    if align3 != None: L.append(align3) 
    return PLASM_ALIGN(L)([obj1, obj2])

# ===================================================
# BOX of a pol complex
# ===================================================

def BOX (List):
    def BOX0 (List,pol):
        if not isinstance(List,list): List=[List]
        dim = len(List) 
        box=Plasm.limits(pol)
        vt =Vecf([0] + [box.p1     [i] for i in List])
        vs=Vecf([0] + [box.size()[i] for i in List]) 
        return Plasm.translate(Plasm.scale(Plasm.cube(dim),vs),vt)
    return lambda pol: BOX0(List,pol)

if self_test: 
   assert(Plasm.limits(BOX([1,3])(Plasm.translate(Plasm.cube(3),Vecf(0,1,2,3))))==Boxf(Vecf(1,1,3),Vecf(1,2,4))) 
   assert(Plasm.limits(BOX(3)(Plasm.translate(Plasm.cube(3),Vecf(0,1,2,3))))==Boxf(Vecf([1,3]),Vecf([1,4])))

# ===================================================
# VECTORS 
# ===================================================

def VECTPROD (args):
    ret=Vec3f(args[0]).cross(Vec3f(args[1]))
    return [ret.x,ret.y,ret.z]

if self_test:
   assert VECTPROD ([[1,0,0],[0,1,0]])==[0,0,1]
   assert VECTPROD ([[0,1,0],[0,0,1]])==[1,0,0] 
   assert VECTPROD ([[0,0,1],[1,0,0]])==[0,1,0]


def VECTNORM(u):
   return Vecf(u).module()

if self_test: 
	assert VECTNORM([1,0,0])==1 


INNERPROD = COMP([COMP([RAISE(SUM), AA(RAISE(PROD))]), TRANS])

if self_test:
  assert INNERPROD ([[1,2,3],[4,5,6]])==32


def SCALARVECTPROD (args):
    s,l=args
    if not isinstance(l,list): s,l=l,s
    return [s*l[i] for i in range(len(l))]

if self_test:
  assert SCALARVECTPROD([2,[0,1,2]])==[0,2,4] and SCALARVECTPROD([[0,1,2],2])==[0,2,4]


def MIXEDPROD (args):
    A , B , C = args
    return INNERPROD([VECTPROD([A,B]),C])


if self_test:
	assert MIXEDPROD([[1,0,0],[0,1,0],[0,0,1]])==1.0
	
def UNITVECT(V):
	assert isinstance(V,list)
	v=Vecf(V).normalize()
	return [v[i] for i in range(len(V))]
	
if self_test:
	assert UNITVECT([2,0,0])==[1,0,0]
	assert UNITVECT([1,1,1])==UNITVECT([2,2,2])


def DIRPROJECT (E):
	E=UNITVECT(E)
	def DIRPROJECT0 (V):
		return SCALARVECTPROD([(INNERPROD([E,V])),E])
	return DIRPROJECT0

if self_test:
	assert DIRPROJECT([1,0,0])([2,0,0])==[2,0,0]
	assert DIRPROJECT([1,0,0])([0,1,0])==[0,0,0]

def ORTHOPROJECT (E):
    def ORTHOPROJECT0 (V):
        return VECTDIFF([V,DIRPROJECT((E))(V)])
    return ORTHOPROJECT0

if self_test:
	assert ORTHOPROJECT([1,0,0])([1,1,0])==[0,1,0]




# ===================================================
# PLASM_MAP
# ===================================================

def PLASM_MAP(fun):

	# speed up by caching points
	cache={}

	def PLASM_MAP0 (fun,pol):

		points, hulls, pols = UKPOL(pol)

		if isinstance(fun, list): 
			fun = CONS(fun)    

		# do not calculate the same points two times
		mapped_points=[]

		for point in points:

			key=str(point)

			if key in cache:
				# already calculated
				mapped_point=cache[key]
			else:
				# to calculate (slow!)
				mapped_point=fun(point)
				cache[key]=mapped_point

			mapped_points+=[mapped_point]

		return MKPOL([mapped_points, hulls, pols])

	return lambda pol: PLASM_MAP0(fun,pol)


if self_test: 
	assert( Plasm.limits(PLASM_MAP([S1,S2])(Plasm.cube(2)))==Boxf(Vecf(1,0,0),Vecf(1,1,1)))
	assert(Plasm.limits(PLASM_MAP(ID)(Plasm.cube(2)))==Boxf(Vecf(1,0,0),Vecf(1,1,1)))

# NEW DEFINITION:
def MAP(ref_domain, args):
    return PLASM_MAP(args)(ref_domain)

# ===================================================
# OTHER TESTS
# ===================================================

ISREALVECT = ISSEQOF(ISREAL)
ISFUNVECT = ISSEQOF(ISFUN)
ISVECT = COMP([OR, CONS([ISREALVECT, ISFUNVECT])])
ISPOINT = ISVECT
ISPOINTSEQ = COMP([AND, CONS([ISSEQOF(ISPOINT), COMP([EQ, AA(LEN)])])])
ISMAT = COMP([AND, CONS([COMP([OR, CONS([ISSEQOF(ISREALVECT), ISSEQOF(ISFUNVECT)])]), COMP([EQ, AA(LEN)])])])
ISSQRMAT = COMP([AND, CONS([ISMAT, COMP([EQ, CONS([LEN, COMP([LEN, S1])])])])])
def ISMATOF (ISTYPE): return COMP([COMP([AND, AR]), CONS([COMP([AA(ISTYPE), CAT]), COMP([ISMAT, (COMP([AA, AA]))((K(1)))])])])



# ===================================================
# FACT  
# ===================================================

def FACT (N):
    return PROD(INTSTO(N)) if N>0 else 1

if self_test: 
	assert FACT(4)==24 and FACT(0)==1


# =============================================
# circle 
# =============================================

def CIRCLE_POINTS(R,N):
   return [ [R*math.cos(i*2*PI/N),R*math.sin(i*2*PI/N)] for i in range(0,N) ]

def CIRCUMFERENCE (R):
    return lambda N: PLASM_MAP(lambda p: [R*math.cos(p[0]),R*math.sin(p[0]) ])(PLASM_INTERVALS(2*PI)(N))

def NGON (N):
    return CIRCUMFERENCE(1)(N)


if self_test:
    assert Plasm.limits(CIRCUMFERENCE(1)(8))==Boxf(Vecf(1,-1,-1),Vecf(1,+1,+1))
    assert len(  (UKPOL(CIRCUMFERENCE(1)(4)))[0]  )==4*2 

# =============================================
# RING 
# =============================================

def PLASM_RING (radius):
    R1 , R2 = radius
    def PLASM_RING0 (subds):
        N , M = subds
        domain= Plasm.translate(PLASM_POWER([PLASM_INTERVALS(2*PI)(N),PLASM_INTERVALS(R2-R1)(M)]),Vecf([0.0,0.0,R1]))
        fun=lambda p: [p[1]*math.cos(p[0]),p[1]*math.sin(p[0])]
        return PLASM_MAP(fun)(domain)
    return PLASM_RING0

if self_test:
    assert Plasm.limits(PLASM_RING([0.5,1])([8,8]))==Boxf(Vecf(1,-1,-1),Vecf(1,+1,+1))

# NEW DEFINITION
def RING(args, division = 64):
    return PLASM_RING(args)(division)

def PLASM_TUBE (args):
    r1 , r2 , height= args
    def PLASM_TUBE0 (N):
        return Plasm.power(PLASM_RING([r1, r2])([N, 1]),QUOTE([height]))
    return PLASM_TUBE0

# NEW DEFINITION
def TUBE(r1, r2, h, division = 64):
    return PLASM_TUBE([r1, r2, h])(division)



# =============================================
# CIRCLE 
# =============================================

def PLASM_CIRCLE (R):
    def PLASM_CIRCLE0 (subs):
        N , M = subs
        domain= PLASM_POWER([PLASM_INTERVALS(2*PI)(N), PLASM_INTERVALS(R)(M)])
        fun=lambda p: [p[1]*math.cos(p[0]),p[1]*math.sin(p[0])]
        return PLASM_MAP(fun)(domain)
    return PLASM_CIRCLE0

if self_test: 
    assert Plasm.limits(PLASM_CIRCLE(1.0)([8,8]))==Boxf(Vecf(1,-1,-1),Vecf(1,+1,+1))

# NEW DEFINITION
def CIRCLE(r, division = [64, 32]):
    if type(division) == list: 
        return PLASM_CIRCLE(r)(division)
    else:
        return PLASM_CIRCLE(r)([division, 32])
def CIRCLE3D(r, division = [64, 32]):
    # height is kept the same for add these thin objects,
    # so that logical operations with them work:
    h = 0.001
    if type(division) == list: 
        return PRISM(PLASM_CIRCLE(r)(division), h)
    else:
        return PRISM(PLASM_CIRCLE(r)([division, 32]), h)



# =============================================
# MY_CYLINDER 
# =============================================

def PLASM_MY_CYLINDER (args):
    raise NameError('Command CYLINDER is available starting with Basic Plan.')
    R , H = args
    def PLASM_MY_CYLINDER0 (N):
        points=CIRCLE_POINTS(R,N)
        circle=Plasm.mkpol(2,CAT(points),[range(N)])
        return Plasm.power(circle,Plasm.mkpol(1,[0,H],[[0,1]]))
    return PLASM_MY_CYLINDER0

PLASM_CYLINDER = PLASM_MY_CYLINDER 


if self_test: 
   assert(Plasm.limits(PLASM_CYLINDER([1.0,2.0])(8)).fuzzyEqual(Boxf(Vecf(1,-1,-1,0),Vecf(1,+1,+1,2))))

# NEW DEFINITION
def CYLINDER(r, h, division = 64):
    return PLASM_CYLINDER([r, h])(division)



# =============================================
# SPHERE
# =============================================


def PLASM_SPHERE (radius):
    raise NameError('Command SPHERE is available starting with Basic Plan.')
    def PLASM_SPHERE0 (subds):
        N , M = subds
        domain = Plasm.translate( Plasm.power(PLASM_INTERVALS(PI)(N) , PLASM_INTERVALS(2*PI)(M)), Vecf(0, -PI/2,0 ) )
        fx  = lambda p: radius * math.cos(p[0])  * math.sin  (p[1])
        fy  = lambda p: radius * math.cos(p[0]) * math.cos (p[1])
        fz  = lambda p: radius * math.sin(p[0]) 
        ret=  PLASM_MAP([fx, fy, fz])(domain)
        return ret
    return PLASM_SPHERE0

if self_test:
	assert Plasm.limits(PLASM_SPHERE(1)([8,8])).fuzzyEqual(Boxf(Vecf(1,-1,-1,-1),Vecf(1,+1,+1,+1)))
	plasm_config.push(1e-4)
	VIEW(PLASM_SPHERE(1)([16,16]))
	plasm_config.pop()

# NEW DEFINITION WITH NON-MANDATORY DIVISIONS:
def SPHERE_SURFACE(radius, divisions = [24, 48]):
    raise NameError('Command SPHERE_SURFACE is available starting with Basic Plan.')
    # This is a surface:
    return PLASM_SPHERE(radius)(divisions)

def SPHERE(radius, divisions = [24, 48]):
    # Making it s solid:
    return PLASM_JOIN(PLASM_SPHERE(radius)(divisions))


# =============================================
# TORUS - SURFACE
# =============================================

def PLASM_TORUS (radius):
    raise NameError('Command TORUS is available starting with Basic Plan.')
    r1 , r2 = radius
    def PLASM_TORUS0 (subds):
        N , M = subds
        a=0.5*(r2-r1)
        c=0.5*(r1+r2)
        domain=Plasm.power(  PLASM_INTERVALS(2*PI)(N),  PLASM_INTERVALS(2*PI)(M)  )
        fx =   lambda p: (c+a*math.cos(p[1])) * math.cos(p[0])
        fy =   lambda p: (c+a*math.cos(p[1])) * math.sin (p[0])
        fz =   lambda p: a*math.sin(p[1])
        return PLASM_MAP(([fx,fy,fz]))(domain)
    return PLASM_TORUS0


if self_test:
   assert Plasm.limits(PLASM_TORUS([1,2])([8,8])).fuzzyEqual(Boxf(Vecf(1,-2,-2,-0.5),Vecf(1,+2,+2,+0.5)))
   plasm_config.push(1e-4)
   VIEW(PLASM_TORUS([1,2])([20,20]))
   plasm_config.pop()

# NEW DEFINITION WITH NON-MANDATORY DIVISIONS:
def TORUS_SURFACE(r1, r2, divisions = [64, 32]):
    raise NameError('Command TORUS_SURFACE is available starting with Basic Plan.')
    return PLASM_TORUS([r1, r2])(divisions)

# =============================================
# TORUS - SOLID
# =============================================

def PLASM_SOLIDTORUS (radius):
    raise NameError('Command PLASM_SOLIDTORUS is available starting with Basic Plan.')
    r1 , r2 = radius
    def PLASM_TORUS0 (subdomains):
        N, M, P = subdomains
        a=0.5*(r2-r1)
        c=0.5*(r1+r2)
        domain = INSR(PROD)([PLASM_INTERVALS(2*PI)(N), PLASM_INTERVALS(2*PI)(M), PLASM_INTERVALS(1)(P)])
        fx =   lambda p: (c + p[2]*a*math.cos(p[1])) * math.cos(p[0])
        fy =   lambda p: (c + p[2]*a*math.cos(p[1])) * math.sin(p[0])
        fz =   lambda p: p[2]*a*math.sin(p[1])
        return PLASM_MAP(([fx,fy,fz]))(domain)
    return PLASM_TORUS0

if self_test:
	VIEW(SKELETON(1)(PLASM_SOLIDTORUS([1.5,2])([18,24,1])))

# NEW DEFINITION WITH NON-MANDATORY DIVISIONS:
def TORUS(r1, r2, divisions = [64, 32]):
    raise NameError('Command TORUS is available starting with Basic Plan.')
    return PLASM_SOLIDTORUS([r1, r2])([divisions[0], divisions[1], 1])


# =============================================
# CONE
# =============================================

def PLASM_CONE (args):
    raise NameError('Command PLASM_CONE is available starting with Basic Plan.')
    radius , height = args
    def PLASM_CONE0(N):
       basis = PLASM_CIRCLE(radius)([N,1])
       apex = PLASM_TRANSLATE([1, 2, 3])([0, 0, height])(SIMPLEX(0))
       return  PLASM_JOIN([basis, apex])
    return PLASM_CONE0

if self_test:
   assert Plasm.limits(PLASM_CONE([1.0,3.0])(16)).fuzzyEqual(Boxf(Vecf(1,-1,-1,0),Vecf(1,+1,+1,3)))

# NEW DEFINITION WITH NON-MANDATORY DIVISIONS:
def CONE(r, h, division = 64):
    raise NameError('Command CONE is available starting with Basic Plan.')
    return PLASM_CONE([r, h])(division)


# =============================================
# TRUNCONE
# =============================================

def PLASM_TRUNCONE (args):
        raise NameError('Command PLASM_TRUNCONE is available starting with Basic Plan.')
	R1 , R2 , H = args
	def PLASM_TRUNCONE0 (N):
		domain = Plasm.power( QUOTE([2*PI/N for i in range(N)]) , QUOTE([1])  )
		def fn(p):
			return [
				(R1+p[1]*(R2-R1))*math.cos(p[0]),	
				(R1+p[1]*(R2-R1))*math.sin(p[0]),
				(H*p[1])
			]
		return PLASM_MAP(fn)(domain)
	return PLASM_TRUNCONE0

# NEW DEFINITION WITH NON-MANDATORY DIVISIONS:
def TRUNCONE(r1, r2, h, divisions = 64):
    raise NameError('Command TRUNCONE is available starting with Basic Plan.')
    # Changing to a solid:
    return PLASM_JOIN(PLASM_TRUNCONE([r1, r2, h])(divisions))


# =============================================
# DODECAHEDRON
# =============================================

def DODECAHEDRON ():
        raise NameError('Command DODECAHEDRON is available starting with Basic Plan.')
	a = 1.0/(math.sqrt(3.0))
	g = 0.5*(math.sqrt(5.0)-1)
	top = MKPOL([[[1-g,1,0-g],[1+g,1,0-g]],[[1, 2]],[[1]]])
	basis = EMBED(1)(CUBOID([2, 2]))
	roof = PLASM_TRANSLATE([1, 2, 3])([-1,-1,-1])(PLASM_JOIN([basis, top]))
	roofpair = PLASM_STRUCT([roof, PLASM_ROTATE([2, 3])(PI), roof])
	return PLASM_S([1, 2, 3])([a, a, a])(PLASM_STRUCT([ 
		Plasm.cube(3,-1,+1),
		roofpair, 
		PLASM_R([1, 3])(PI/2), PLASM_R([1, 2])(PI/2), 
		roofpair, 
		PLASM_R([1, 2])(PI/2), PLASM_R([2, 3])(PI/2), 
		roofpair]))

#DODECAHEDRON = build_DODECAHEDRON()


# =============================================
# ICOSAHEDRON
# =============================================

def ICOSAHEDRON():
    raise NameError('Command ICOSAHEDRON is available starting with Basic Plan.')
    g = 0.5*(math.sqrt(5)-1)
    b = 2.0/(math.sqrt(5*math.sqrt(5)))
    rectx = PLASM_TRANSLATE([1, 2, 3])([-g, -1, 0])(CUBOID([2*g, 2]))
    recty = PLASM_R([1, 3])(PI/2)(PLASM_R([1, 2])(PI/2)(rectx))
    rectz = PLASM_R([2, 3])(PI/2)(PLASM_R([1, 2])(PI/2)(rectx))
    return PLASM_S([1, 2, 3])([b, b, b])(PLASM_JOIN([rectx, recty, rectz]))

#ICOSAHEDRON = build_ICOSAHEDRON()


# =============================================
# TETRAHEDRON
# =============================================

def PLASM_TETRAHEDRON():
        raise NameError('Command TETRAHEDRON is available starting with Basic Plan.')
	return PLASM_JOIN([  PLASM_TRANSLATE([1, 2, 3])([0, 0, -1.0/3.0])(NGON(3)),  MK([0, 0, 1])  ])

#PLASM_TETRAHEDRON = build_TETRAHEDRON()

# NEW DEFINITION:
def TETRAHEDRON(a, b, c, d):
    return PLASM_CONVEXHULL([a, b, c, d])

# =============================================
# TRIANGLE
# =============================================

# NEW DEFINITION:
def TRIANGLE(a, b, c):
    raise NameError('Command TRIANGLE is available starting with Basic Plan.')
    return PLASM_CONVEXHULL([a, b, c])
def TRIANGLE3D(a, b, c):
    raise NameError('Command TRIANGLE3D is available starting with Basic Plan.')
    # height is kept the same for add these thin objects,
    # so that logical operations with them work:
    h = 0.001
    ## Get maximum edge length:
    #e1 = sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
    #e2 = sqrt((c[0] - b[0])**2 + (c[1] - b[1])**2)
    #e3 = sqrt((c[0] - a[0])**2 + (c[1] - a[1])**2)
    #h = e1
    #if e2 > h: h = e2
    #if e3 > h: h = e3 
    # Get six points for the prism:
    a_low = [a[0], a[1], 0]
    a_high = [a[0], a[1], h]
    b_low = [b[0], b[1], 0]
    b_high = [b[0], b[1], h]
    c_low = [c[0], c[1], 0]
    c_high = [c[0], c[1], h]
    # Get the convex hull:
    return PLASM_CONVEXHULL([a_low, a_high, b_low, b_high, c_low, c_high])


# ===================================================
# POLYPOINT 
# ===================================================

def POLYPOINT (points):
	return Plasm.mkpol( len(points[0]),CAT(points),[ [i] for i in range(len(points))] )

# ===================================================
# POLYLINE 
# ===================================================

def POLYLINE (points):
	return Plasm.mkpol( len(points[0]),CAT(points),[[i,i+1] for i in range(len(points)-1)])




# ===================================================
# TRIANGLESTRIPE 
# ===================================================

def TRIANGLESTRIPE (points):
	cells=[ [i,i+1,i+2] if (i%2==0) else [i+1,i,i+2] for i in range(len(points)-2)]
	return Plasm.mkpol(len(points[0]),CAT(points),cells)


# ===================================================
# TRIANGLEFAN 
# ===================================================

def TRIANGLEFAN (points):
	cells=[[0,i-1,i] for i in range(2,len(points))]
	return Plasm.mkpol(len(points[0]),CAT(points),cells)

# ===================================================
# MIRROR 
# ===================================================

def MIRROR (D):
    def MIRROR0 (pol):
        return  PLASM_STRUCT([PLASM_S(D)(-1)(pol),pol])
    return MIRROR0


# ===================================================
# POLYMARKER
# ===================================================

def POLYMARKER (type,MARKERSIZE=0.1):
	A,B=(MARKERSIZE,-MARKERSIZE)
	marker0=Plasm.mkpol(2,[A,0, 0,A, B,0, 0,B],[[0, 1], [1, 2], [2, 3], [3, 0]])
	marker1=Plasm.mkpol(2,[A, A, B, A, B, B, A, B], [[0, 2], [1, 3]])
	marker2=Plasm.mkpol(2,[A, A, B, A, B, B, A, B], [[0, 1], [1, 2], [2, 3], [3, 0]])
	marker3=PLASM_STRUCT([marker0,marker1])
	marker4=PLASM_STRUCT([marker0,marker2])
	marker5=PLASM_STRUCT([marker1,marker2])
	marker=[marker0, marker1, marker2, marker3, marker4,marker5][type % 6]
	def POLYMARKER_POINTS(points):
		dim=len(points[0])
		axis=range(1,dim+1)
		return Plasm.Struct([PLASM_T(axis)(point)(marker) for point in points])
	return POLYMARKER_POINTS


# ===================================================
# CHOOSE (binomial factors)
# ===================================================

def CHOOSE (args):
    N , K = args
    return FACT(N)/float(FACT(K)*FACT(N-K))

if self_test:
	assert CHOOSE([7,3])==35

# ===================================================
# TRACE
# ===================================================

def TRACE(MATRIX):
	acc=0
	dim=len(MATRIX)
	for i in range(dim):acc+=MATRIX[i][i]
	return acc

if self_test:
	assert TRACE([[5,0],[0,10]])==15

# ===================================================
# PASCALTRIANGLE
# ===================================================

def PASCALTRIANGLE (N):
	if (N==0): return [[1]]
	if (N==1): return [[1],[1,1]]
	prev=PASCALTRIANGLE(N-1)
	last_row=prev[-1]
	cur=[1]+[last_row[i-1]+last_row[i]  for i in range(1,len(last_row))] + [1]
	return prev+[cur]

if self_test:
	assert PASCALTRIANGLE(4)==[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]


# =====================================================
# see http://it.wikipedia.org/wiki/Curva_di_B%C3%A9zier
# =====================================================
def PLASM_BEZIER(U):
        raise NameError('Bezier curves are available starting with Basic Plan.')
	def PLASM_BEZIER0 (controldata_fn):
		N=len(controldata_fn)-1

		def map_fn(point):
			t=U(point)
			controldata=[fun(point) if callable(fun) else fun for fun in controldata_fn]
			ret=[0.0 for i in range(len(controldata[0]))]		
			for I in range(N+1):
				weight=CHOOSE([N,I])*math.pow(1-t,N-I)*math.pow(t,I)
				for K in range(len(ret)):  ret[K]+=weight*(controldata[I][K])
			return ret
		return map_fn
	return PLASM_BEZIER0

if self_test:
	VIEW(PLASM_MAP(PLASM_BEZIER(S1)([[-0,0],[1,0],[1,1],[2,1],[3,1]]))(PLASM_INTERVALS(1)(32)))
	C0 = PLASM_BEZIER(S1)([[0,0,0],[10,0,0]])
	C1 = PLASM_BEZIER(S1)([[0,2,0],[8,3,0],[9,2,0]])
	C2 = PLASM_BEZIER(S1)([[0,4,1],[7,5,-1],[8,5,1],[12,4,0]])
	C3 = PLASM_BEZIER(S1)([[0,6,0],[9,6,3],[10,6,-1]])

	plasm_config.push(1e-4)
	out = PLASM_MAP(PLASM_BEZIER(S2)([C0,C1,C2,C3]))(  Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))  )
	plasm_config.pop()
	VIEW(out)


def PLASM_BEZIERCURVE (controlpoints):
    return PLASM_BEZIER(S1)(controlpoints)

# NEW DEFINITIONS:
def BEZIER_1(*args):
    return PLASM_BEZIER(S1)(list(args))

#BE_1 = BEZIER_1

def BEZIER_2(*args):
    return PLASM_BEZIER(S2)(list(args))

#BE_2 = BEZIER_2

def BEZIER_3(*args):
    return PLASM_BEZIER(S3)(list(args))

#BE_3 = BEZIER_3


# ======================================================
# coons patch
# ======================================================

def PLASM_COONSPATCH (args):
        raise NameError('Coons patch is available starting with Basic Plan.')
	su0_fn , su1_fn , s0v_fn , s1v_fn = args

	def map_fn(point):
		u,v=point

		su0=su0_fn(point) if callable(su0_fn) else su0_fn
		su1=su1_fn(point) if callable(su1_fn) else su1_fn
		s0v=s0v_fn(point) if callable(s0v_fn) else s0v_fn
		s1v=s1v_fn(point) if callable(s1v_fn) else s1v_fn

		ret=[0.0 for i in range(len(su0))]	
		for K in range(len(ret)):
			ret[K]= (1-u)*s0v[K]+u*s1v[K]+(1-v)*su0[K]+v*su1[K]+(1-u)*(1-v)*s0v[K]+(1-u)*v*s0v[K]+u*(1-v)*s1v[K]+u*v*s1v[K] 
		return ret
	return map_fn


if self_test:
	Su0=PLASM_BEZIER(S1)([[0,0,0],[10,0,0]])
	Su1=PLASM_BEZIER(S1)([[0,10,0],[2.5,10,3],[5,10,-3],[7.5,10,3],[10,10,0]])
	Sv0=PLASM_BEZIER(S2)([[0,0,0],[0,0,3],[0,10,3],[0,10,0]])
	Sv1=PLASM_BEZIER(S2)([[10,0,0],[10,5,3],[10,10,0]])
	plasm_config.push(1e-4)
	out=PLASM_MAP(PLASM_COONSPATCH([Su0,Su1,Sv0,Sv1]))(Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10)))
	plasm_config.pop()
	VIEW(out)

# NEW DEFINITION:
def COONSPATCH(a, b, c, d):
    return PLASM_COONSPATCH([a, b, c, d])

# ======================================================
# RULED SURFACE
# ======================================================

def PLASM_RULEDSURFACE (args):
        raise NameError('Ruled surface is available starting with Basic Plan.')
	alpha_fn , beta_fn = args

	def map_fn(point):
		u,v=point
		alpha,beta=alpha_fn(point),beta_fn(point)
		ret=[0.0 for i in range(len(alpha))]	
		for K in range(len(ret)): ret[K]=alpha[K]+v*beta[K]
		return ret
	return map_fn


if self_test:
	alpha= lambda point: [point[0],point[0],       0 ]
	beta = lambda point: [      -1,      +1,point[0] ]
	domain= PLASM_TRANSLATE([1, 2, 3])([-1, -1, 0])(Plasm.power(PLASM_INTERVALS(2)(10),PLASM_INTERVALS(2)(10)))
	plasm_config.push(1e-4)
	VIEW(PLASM_MAP(PLASM_RULEDSURFACE([alpha,beta]))(domain))
	plasm_config.pop()

# NEW DEFINITION
def RULED_SURFACE(a, b):
    raise NameError('Ruled surface is available starting with Basic Plan.')
    return PLASM_RULEDSURFACE([a, b])
#RUSURFACE = RULED_SURFACE
    
# ======================================================
# PROFILE SURFACE
# ======================================================

def PROFILEPRODSURFACE (args):
        raise NameError('Profile product surface is available starting with Basic Plan.')
	profile_fn,section_fn = args

	def map_fun(point):
		u,v=point
		profile,section=profile_fn(point),section_fn(point)
		ret=[profile[0]*section[0],profile[0]*section[1],profile[2]]
		return ret
	return map_fun

if self_test:
	alpha=PLASM_BEZIER(S1)([[0.1,0,0],[2,0,0],[0,0,4],[1,0,5]])
	beta =PLASM_BEZIER(S2)([[0,0,0],[3,-0.5,0],[3,3.5,0],[0,3,0]])
	plasm_config.push(1e-4)
	domain=Plasm.power(PLASM_INTERVALS(1)(20),PLASM_INTERVALS(1)(20))
	out=Plasm.Struct([PLASM_MAP(alpha)(domain),PLASM_MAP(beta )(domain),PLASM_MAP(PROFILEPRODSURFACE([alpha,beta]))(domain)])
	plasm_config.pop()
	VIEW(out)

# NEW DEFINITION
def PROFILE_PROD_SURFACE(a, b):
    return PROFILEPRODSURFACE([a, b])
#PPSURFACE = PROFILE_PROD_SURFACE

    
# ======================================================
# ROTATIONALSURFACE
# ======================================================

def ROTATIONALSURFACE (args):
        raise NameError('Rotational surface is available starting with Basic Plan.')
	profile = args

	def map_fn(point):
		u,v=point
		f,h,g= profile(point)
		ret=[f*math.cos(v),f*math.sin(v),g]
		return ret
	return map_fn

if self_test:
	profile=PLASM_BEZIER(S1)([[0,0,0],[2,0,1],[3,0,4]]) # defined in xz!
	plasm_config.push(1e-4)
	domain=Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(2*PI)(30)) # the first interval should be in 0,1 for bezier
	out=PLASM_MAP(ROTATIONALSURFACE(profile))(domain)
	plasm_config.pop()
	VIEW(out)

# NEW COMMAND:
def ROTATIONAL_SURFACE(args):
    return ROTATIONALSURFACE(args)
#ROSURFACE = ROTATIONAL_SURFACE
#ROS = ROTATIONAL_SURFACE

    
# ======================================================
# CYLINDRICALSURFACE
# ======================================================

def CYLINDRICALSURFACE (args):
        raise NameError('Cylindrical surface is available starting with Basic Plan.')
	alpha_fun   = args[0]
	beta_fun    = CONS(AA(K)(args[1]))
	return PLASM_RULEDSURFACE([alpha_fun,beta_fun])

if self_test:
	alpha=PLASM_BEZIER(S1)([[1,1,0],[-1,1,0],[1,-1,0],[-1,-1,0]])
	Udomain=PLASM_INTERVALS(1)(20)
	Vdomain=PLASM_INTERVALS(1)(6)
	domain=Plasm.power(Udomain,Vdomain)
	fn=CYLINDRICALSURFACE([alpha,[0,0,1]])
	VIEW(PLASM_MAP(fn)(domain))

# NEW COMMAND:
def CYLINDRICAL_SURFACE(a, b):
    return CYLINDRICALSURFACE([a, b])
#CYSURFACE = CYLINDRICAL_SURFACE


# ======================================================
# CONICALSURFACE
# ======================================================

   
def CONICALSURFACE (args):
        raise NameError('Conical surface is available starting with Basic Plan.')
	apex=args[0]
	alpha_fn   = lambda point: apex
	beta_fn    = lambda point: [ args[1](point)[i]-apex[i] for i in range(len(apex))]
	return PLASM_RULEDSURFACE([alpha_fn, beta_fn])


if self_test:
	domain=Plasm.power(PLASM_INTERVALS(1)(20),PLASM_INTERVALS(1)(6))
	beta=PLASM_BEZIER(S1)([ [1,1,0],[-1,1,0],[1,-1,0],[-1,-1,0] ])
	out=PLASM_MAP(CONICALSURFACE([[0,0,1],beta]))(domain)
	VIEW(out)

# NEW COMMAND:
def CONICAL_SURFACE(a, b):
    return CONICALSURFACE([a, b])
#COSURFACE = CONICAL_SURFACE


# ======================================================
# CUBICHERMITE
# ======================================================

def PLASM_CUBICHERMITE (U):
        raise NameError('Cubic Hermite splines are available starting with Basic Plan.')
	def PLASM_CUBICHERMITE0 (args):
		p1_fn , p2_fn , s1_fn , s2_fn = args
		def map_fn(point):
			u=U(point);u2=u*u;u3=u2*u
			p1,p2,s1,s2=[f(point) if callable(f) else f for f in [p1_fn , p2_fn , s1_fn , s2_fn]]
			ret=[0.0 for i in range(len(p1))]		
			for i in range(len(ret)):				
				ret[i]+=(2*u3-3*u2+1)*p1[i] + (-2*u3+3*u2)*p2[i]+(u3-2*u2+u)*s1[i]+(u3-u2)*s2[i]
			return ret
		return map_fn
	return PLASM_CUBICHERMITE0

if self_test:

	domain=PLASM_INTERVALS(1)(20)
	out=Plasm.Struct([
		PLASM_MAP(PLASM_CUBICHERMITE(S1)([[1,0],[1,1],[ -1, 1],[ 1,0]]))(domain),
		PLASM_MAP(PLASM_CUBICHERMITE(S1)([[1,0],[1,1],[ -2, 2],[ 2,0]]))(domain),
		PLASM_MAP(PLASM_CUBICHERMITE(S1)([[1,0],[1,1],[ -4, 4],[ 4,0]]))(domain),
		PLASM_MAP(PLASM_CUBICHERMITE(S1)([[1,0],[1,1],[-10,10],[10,0]]))(domain)
	])
	VIEW(out)

	c1=PLASM_CUBICHERMITE(S1)([[1  ,0,0],[0  ,1,0],[0,3,0],[-3,0,0]])
	c2=PLASM_CUBICHERMITE(S1)([[0.5,0,0],[0,0.5,0],[0,1,0],[-1,0,0]])
	sur3=PLASM_CUBICHERMITE(S2)([c1,c2,[1,1,1],[-1,-1,-1]])
	plasm_config.push(1e-4)
	domain=Plasm.power(PLASM_INTERVALS(1)(14),PLASM_INTERVALS(1)(14))
	out=PLASM_MAP(sur3)(domain)
	plasm_config.pop()
	VIEW(out)

# NEW DEFINITION
def CUBIC_HERMITE_1(*args):
    return PLASM_CUBICHERMITE(S1)(list(args))

#CH_1 = CUBIC_HERMITE_1

def CUBIC_HERMITE_2(*args):
    return PLASM_CUBICHERMITE(S2)(list(args))

#CH_2 = CUBIC_HERMITE_2

def CUBIC_HERMITE_3(*args):
    return PLASM_CUBICHERMITE(S3)(list(args))

#CH_3 = CUBIC_HERMITE_3

def PLASM_HERMITE(args):
    P1 , P2 , T1 , T2 = args
    return PLASM_CUBICHERMITE(S1)([P1, P2, T1, T2])




# ======================================================
# EXTRUDE
# ======================================================

def Q(H):
	return Plasm.mkpol(1,[0,H],[[0,1]])

def PLASM_EXTRUDE (args):
        raise NameError('Extrusion is available starting with Basic Plan.')
	__N, Pol, H = args
	return Plasm.power(Pol,Q(H))

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
def EXTRUDE(*args):
    return PLASM_EXTRUDE(list(args))

def MULTEXTRUDE (P):
	def MULTEXTRUDE0 (H):
		return Plasm.power(P,Q(H))
	return MULTEXTRUDE0


# ======================================================
# PROJECT
# ======================================================

def PROJECT (M):
	def PROJECT0 (POL):
		vertices,cells,pols=UKPOL(POL)
		vertices=[vert[0:-M] for vert in vertices]
		return MKPOL([vertices,cells,pols])
	return PROJECT0



# ======================================================
# SPLITCELLS
# ======================================================

def SPLITCELLS (scene):
	vertices,cells,pols= UKPOL(scene)
	ret=[]
	for c in cells: ret+=[MKPOL([vertices,[c],[[1]]])]
	return ret


def EXTRACT_WIRES (scene):
    return SPLITCELLS(SKEL_1(scene))

# no notion of pols for xge mkpol!
#SPLITPOLS=SPLITCELLS

# ===================================================
# PERMUTATIONS
# ===================================================

def PERMUTATIONS (SEQ):
	if len(SEQ)<=1: return [SEQ]
	ret=[]
	for i in range(len(SEQ)):
		element =SEQ[i]
		rest    =PERMUTATIONS(SEQ[0:i] + SEQ[i+1:])
		for r in rest: ret+=[[element] + r]
	return ret
	
if self_test:
	assert len(PERMUTATIONS([1,2,3]))==6


# ===================================================
# PERMUTAHEDRON
# ===================================================

def PERMUTAHEDRON (d):
	vertices = PERMUTATIONS(range(1,d+2))
	center = MEANPOINT(vertices)
	cells=[range(1,len(vertices)+1)]
	object=MKPOL([vertices,cells,[[1]]])
	object=Plasm.translate(object,Vecf([0] + center)*-1)
	for i in range(1,d+1): object=PLASM_R([i,d+1])(PI/4)(object)
	object=PROJECT(1)(object)
	return object


if self_test:
	VIEW(Plasm.Struct([PERMUTAHEDRON(2),SKEL_1(PERMUTAHEDRON(2))]))
	VIEW(Plasm.Struct([PERMUTAHEDRON(3),SKEL_1(PERMUTAHEDRON(3))]))



# ===================================================
# STAR
# ===================================================

def STAR (N):
    raise NameError('Command STAR is available starting with Basic Plan.')
    def CIRCLEPOINTS (STARTANGLE):
        def CIRCLEPOINTS1 (R):
            def CIRCLEPOINTS0 (N):
                return AA((COMP([CONS([RAISE(PROD)([K(R),COS]), RAISE(PROD)([K(R),SIN])]), (RAISE(SUM)([ID,K(STARTANGLE)]))])))(((COMP([COMP([AA(RAISE(PROD)), TRANS]), CONS([K((FROMTO([1,N]))), DIESIS(N)])]))((2*PI/N))))
            return CIRCLEPOINTS0
        return CIRCLEPOINTS1
    return  (COMP([COMP([TRIANGLEFAN, CAT]), TRANS]))([CIRCLEPOINTS(0)(1)(N), CIRCLEPOINTS((PI/N))(2.5)(N)])



# ===================================================
# SCHLEGEL
# ===================================================

def SCHLEGEL2D(D):
	def map_fn(point):
		return [D*point[0]/point[2],D*point[1]/point[2]]
	return PLASM_MAP(map_fn)

def SCHLEGEL3D (D):
	def map_fn(point):
		return [D*point[0]/point[3],D*point[1]/point[3],D*point[2]/point[3]]
	return PLASM_MAP(map_fn)


if self_test:
	VIEW(SCHLEGEL3D(0.2)(SKEL_1(PLASM_T([1,2,3,4])([-1.0/3.0,-1.0/3.0,-1,+1])(SIMPLEX(4)))))
	VIEW(SCHLEGEL3D(0.2)(SKEL_1(PLASM_T([1,2,3,4])([-1,-1,-1,1])(CUBOID([2,2,2,2])))))
	VIEW(SCHLEGEL3D(0.2)(SKEL_1(PLASM_T([1,2,3,4])([-1.0/3.0,-1.0/3.0,-1,+1])(Plasm.power(SIMPLEX(2),SIMPLEX(2))))))

# ===================================================
# FINITECONE
# ===================================================

def FINITECONE (pol):
	point=[0 for i in range(RN(pol))]
	return PLASM_JOIN([pol,MK(point)])


# ===================================================
# PRISM
# ===================================================

def PLASM_PRISM (HEIGHT):
    raise NameError('Command PLASM_PRISM is available starting with Basic Plan.')
    def PLASM_PRISM0 (BASIS):
        return Plasm.power(BASIS,QUOTE([HEIGHT]))
    return PLASM_PRISM0

# NEW DEFINITION
def PRISM(basis, h):
    raise NameError('Command PRISM is available starting with Basic Plan.')
    return PLASM_PRISM(h)(basis)

# ===================================================
# CROSSPOLYTOPE
# ===================================================

def CROSSPOLYTOPE (D):
	points=[]
	for i in range(D):
		point_pos=[0 for x in range(D)];point_pos[i]=+1
		point_neg=[0 for x in range(D)];point_neg[i]=-1
		points+=[point_pos,point_neg]

	cells=[range(1,D*2+1)]
	pols=[[1]]
	return MKPOL([points,cells,pols])

#OCTAHEDRON = CROSSPOLYTOPE(2)



# ===================================================
# MATHOM
# ===================================================

def MATHOM (M):
	return [[1] + [0 for i in range(len(M))]] + map(lambda l: [0]+l, M)

if self_test:
	assert MATHOM([[1,2],[3,4]])==[[1,0,0],[0,1,2],[0,3,4]]



# ===================================================
# ROTN
# ===================================================

def ROTN (args):
	alpha, N = args
	N=UNITVECT(N)
	QX = UNITVECT((VECTPROD([[0, 0, 1],N])))

	QZ = UNITVECT(N)
	QY = VECTPROD([QZ,QX])
	Q  = MATHOM([QX, QY, QZ])

	ISUP = COMP([AND, CONS([COMP([C(EQ)(0), S1]), COMP([C(EQ)(0), S2]), COMP([COMP([NOT, C(EQ)(0)]), S3])])])

	if N[0]==0 and N[1]==0:
		return PLASM_R([1, 2])(alpha)
	else:
		return COMP([MAT(TRANS(Q)),PLASM_R([1, 2])(alpha),MAT(Q)])


# ===================================================
# MKVECTOR
# ===================================================

#MKVERSORK = PLASM_TOP([PLASM_CYLINDER([1.0/100.0, 7.0/8.0])(6),PLASM_CONE([1.0/16.0,1.0/8])(8)])

def MKVECTOR (P1):
    def MKVECTOR0 (P2):
        TR = PLASM_T([1, 2, 3])(P1)
        U = VECTDIFF([P2,P1])
        ALPHA = ACOS((INNERPROD([[0, 0, 1],UNITVECT(U)])))
        B = VECTNORM(U)
        SC = PLASM_S([1, 2, 3])([B, B, B])
        N = VECTPROD([[0, 0, 1],U])
        ROT = ROTN([ALPHA, N])
        return (COMP([COMP([TR, ROT]), SC]))(MKVERSORK)
    return MKVECTOR0


# ===================================================
# Matrix stuff
# ===================================================

SCALARMATPROD = COMP([COMP([(COMP([AA, AA]))(RAISE(PROD)), AA(DISTL)]), DISTL])

MATDOTPROD = COMP([INNERPROD, AA(CAT)])

def ORTHO (matrix):
	return SCALARMATPROD([0.5,SUM([matrix,TRANS(matrix)])])

def SKEW (matrix):
    return SCALARMATPROD([0.5, PLASM_DIFF([matrix,TRANS(matrix)])])


if self_test:
	temp=[[1,2],[3,4]]
	assert SCALARMATPROD([10.0,temp])==[[10,20],[30,40]]
	assert MATDOTPROD([temp,[[1,0],[0,1]]])==5
	assert ORTHO([[1,0],[0,1]])==[[1,0],[0,1]]
	assert SKEW ([[1,0],[0,1]])==[[0,0],[0,0]]



# ======================================================
# CUBICUBSPLINE
# ======================================================

def CUBICUBSPLINE (domain):
	
	def CUBICUBSPLINE0(args):
		q1_fn, q2_fn , q3_fn , q4_fn = args


		def map_fn(point):
			u=S1(point)
			u2=u*u
			u3=u2*u
			q1,q2,q3,q4=[f(point) if callable(f) else f for f in [q1_fn,q2_fn,q3_fn,q4_fn]]
			ret=[0 for x in range(len(q1))]
			for i in range(len(ret)):
				ret[i]=(1.0/6.0)*  ( (-u3+3*u2-3*u+1)*q1[i] + (3*u3-6*u2+4)*q2[i]  + (-3*u3+3*u2+3*u+1)*q3[i] + (u3)*q4[i]  )
			return ret
		return PLASM_MAP(map_fn)(domain)
	return CUBICUBSPLINE0



# ===========================================
# CUBICCARDINAL
# ===========================================

def CUBICCARDINAL (domain,h=1):
	def CUBICCARDINAL0(args):
		q1_fn , q2_fn , q3_fn , q4_fn = args
		def map_fn(point):
			u=S1(point)
			u2=u*u
			u3=u2*u
			q1,q2,q3,q4=[f(point) if callable(f) else f for f in [q1_fn,q2_fn,q3_fn,q4_fn]]
			
			ret=[0.0 for i in range(len(q1))]	
			for i in range(len(ret)):
				ret[i]=(-h*u3+2*h*u2-h*u)*q1[i] +((2-h)*u3+(h-3)*u2+1)*q2[i] + ((h-2)*u3+(3-2*h)*u2+h*u)*q3[i] + (h*u3-h*u2)*q4[i]

			return ret
		return PLASM_MAP(map_fn)(domain)
	return CUBICCARDINAL0


# ======================================================
# SPLINE
# ======================================================

def SPLINE (curve):
	def SPLINE0(points):
		ret=[]
		for i in range(len(points)-4+1):
			P=points[i:i+4]
			ret+=[curve(P)]
		return Plasm.Struct(ret)
	return SPLINE0



if self_test:
	domain=PLASM_INTERVALS(1)(20)
	points = [[-3,6],[-4,2],[-3,-1],[-1,1],[1.5,1.5],[3,4],[5,5],[7,2],[6,-2],[2,-3]]
	VIEW(SPLINE(CUBICCARDINAL(domain))(points))
	VIEW(SPLINE(CUBICUBSPLINE(domain))(points))

# ======================================================
# CUBICUBSPLINE
# ======================================================

def JOINTS (curve):
	knotzero = MK([0])
	def JOINTS0(points):
		points,cells,pols=UKPOL(SPLINE(curve(knotzero)))
		return POLYMARKER(2)(points)



# ======================================================
# BERNSTEINBASIS
# ======================================================

def BERNSTEINBASIS (U):
	def BERNSTEIN0 (N):
		def BERNSTEIN1 (I):

			def map_fn(point):

				t=U(point)
				ret=CHOOSE([N,I])*math.pow(1-t,N-I)*math.pow(t,I)
				return ret
			return map_fn
		return [BERNSTEIN1(I) for I in range(0,N+1)]
	return BERNSTEIN0


# ======================================================
# TENSORPRODSURFACE
# ======================================================

def TENSORPRODSURFACE (args):
	ubasis , vbasis = args
	def TENSORPRODSURFACE0 (controlpoints_fn):

		def map_fn(point):

			# resolve basis
			u,v=point
			U=[f([u]) for f in ubasis]
			V=[f([v]) for f in vbasis]
			
			controlpoints=[f(point) if callable(f) else f for f in controlpoints_fn]

			# each returned vector will be this side (the tensor product is SOLID)
			target_dim=len(controlpoints[0][0])

			ret=[0 for x in range(target_dim)]
			for i in range(len(ubasis)):
				for j in range(len(vbasis)):
					for M in range(len(ret)):
						for M in range(target_dim): 
							ret[M]+= U[i]*V[j] * controlpoints[i][j][M]

			return ret
		return map_fn
	return TENSORPRODSURFACE0

# ======================================================
# BILINEARSURFACE
# ======================================================

def BILINEARSURFACE(controlpoints):
        raise NameError('Command BILINEARSURFACE is available starting with Basic Plan.')
	return TENSORPRODSURFACE([BERNSTEINBASIS(S1)(1),BERNSTEINBASIS(S1)(1)])(controlpoints)

if self_test:
	controlpoints=[[[0,0,0],[2,-4,2]],[[0,3,1],[4,0,0]]]
	domain=Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))
	mapping=BILINEARSURFACE(controlpoints)
	VIEW(PLASM_MAP(mapping)(domain))

# ======================================================
# BIQUADRATICSURFACE
# ======================================================

def BIQUADRATICSURFACE (controlpoints):
	def u0(point):u=S1(point);return 2*u*u-u
	def u1(point):u=S1(point);return 4*u-4*u*u
	def u2(point):u=S1(point);return 2*u*u-3*u+1
	basis = [u0, u1, u2]
	return TENSORPRODSURFACE([basis, basis])(controlpoints)

if self_test:
	controlpoints=[[[0,0,0],[2,0,1],[3,1,1]],[[1,3,-1],[3,2,0],[4,2,0]],[[0,9,0],[2,5,1],[3,3,2]]]
	domain=Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))
	mapping=BIQUADRATICSURFACE(controlpoints)
	plasm_config.push(1e-4)
	VIEW(PLASM_MAP(mapping)(domain))
	plasm_config.pop()


# ======================================================
# HERMITESURFACE
# ======================================================

def PLASM_HERMITESURFACE(controlpoints):
        raise NameError('Hermite surface is available starting with Basic Plan.')
	def H0(point):u=S1(point);u2=u*u;u3=u2*u;return u3-u2
	def H1(point):u=S1(point);u2=u*u;u3=u2*u;return u3-2*u2+u
	def H2(point):u=S1(point);u2=u*u;u3=u2*u;return 3*u2-2*u3
	def H3(point):u=S1(point);u2=u*u;u3=u2*u;return 2*u3-3*u2+1
	basis=[H3, H2, H1, H0]
	return  TENSORPRODSURFACE([basis, basis])(controlpoints)

if self_test:
	controlpoints=[[[0,0,0 ],[2,0,1],[3,1,1],[4,1,1]],[[1,3,-1],[3,2,0],[4,2,0],[4,2,0]],[[0,4,0 ],[2,4,1],[3,3,2],[5,3,2]],[[0,6,0 ],[2,5,1],[3,4,1],[4,4,0]]]
	domain=Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))
	mapping=PLASM_HERMITESURFACE(controlpoints)
	plasm_config.push(1e-4)
	VIEW(PLASM_MAP(mapping)(domain))
	plasm_config.pop()

# ======================================================
# PLASM_BEZIERSURFACE
# ======================================================

def PLASM_BEZIERSURFACE (controlpoints):
    raise NameError('Bezier surface is available starting with Basic Plan.')
    M = len(controlpoints   )-1
    N = len(controlpoints[0])-1
    return TENSORPRODSURFACE([BERNSTEINBASIS(S1)(M), BERNSTEINBASIS(S1)(N)])(controlpoints)

if self_test:
	controlpoints=[
		[[ 0,0,0],[0 ,3  ,4],[0,6,3],[0,10,0]],
		[[ 3,0,2],[2 ,2.5,5],[3,6,5],[4,8,2]],
		[[ 6,0,2],[8 ,3 , 5],[7,6,4.5],[6,10,2.5]],
		[[10,0,0],[11,3  ,4],[11,6,3],[10,9,0]]]
	domain=Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))
	mapping=PLASM_BEZIERSURFACE(controlpoints)
	plasm_config.push(1e-4)
	VIEW(PLASM_MAP(mapping)(domain))
	plasm_config.pop()

# ======================================================
# generic tensor product
# ======================================================

def TENSORPRODSOLID (args):
	# todo other cases (>3 dimension!)
	ubasis,vbasis,wbasis = args
	def TENSORPRODSOLID0 (controlpoints_fn):

		def map_fn(point):

			# resolve basis
			u,v,w=point
			U=[f([u]) for f in ubasis]
			V=[f([v]) for f in vbasis]
			W=[f([w]) for f in wbasis]

			# if are functions call them
			controlpoints=[f(point) if callable(f) else f for f in controlpoints_fn]

			# each returned vector will be this side (the tensor product is SOLID)
			target_dim=len(controlpoints[0][0][0])

			# return vector
			ret=[0 for x in range(target_dim)]
			for i in range(len(ubasis)):
				for j in range(len(vbasis)):
					for k in range(len(wbasis)):
						for M in range(target_dim): 
							ret[M]+= U[i]*V[j]*W[k] * controlpoints[M][i][j][k]
			return ret

		return map_fn
	return TENSORPRODSOLID0

# ======================================================
# PLASM_BEZIERMANIFOLD
# ======================================================

def PLASM_BEZIERMANIFOLD (degrees):
	basis=[BERNSTEINBASIS(S1)(d) for d in degrees]
	return TENSORPRODSOLID(basis)

if self_test:
	grid1D = PLASM_INTERVALS(1)(5)
	domain3D = Plasm.power(Plasm.power(grid1D,grid1D),grid1D)
	degrees = [2,2,2]
	Xtensor =  [[[0,1,2],[-1,0,1],[0,1,2]],[[0,1,2],[-1,0,1],[0,1,2]],[[0,1,2],[-1,0,1],[0,1,2]]]
	Ytensor =  [[[0,0,0.8],[1,1,1],[2,3,2]],[[0,0,0.8],[1,1,1],[2,3,2]],[[0,0,0.8],[1,1,1],[2,3,2]]]
	Ztensor =  [[[0,0,0],[0,0,0],[0,0,0]],[[1,1,1],[1,1,1],[1,1,1]],[[2,2,1],[2,2,1],[2,2,1]]] 
	mapping = PLASM_BEZIERMANIFOLD(degrees)([Xtensor,Ytensor,Ztensor])
	out=PLASM_MAP(mapping)(domain3D)
	VIEW(out)

# ===================================================
# LOCATE
# ===================================================

def LOCATE (args):
	pol, a, distances = args
	ret=[]
	for d in distances:
		ret+=[PLASM_T(a)(d),pol]
	return PLASM_STRUCT(ret)


# ===================================================
# SUBSEQ
# ===================================================

def SUBSEQ (I_J):
	def SUBSEQ0 (SEQ):
		return SEQ[I_J[0]-1:I_J[1]]
	return SUBSEQ0



# ===================================================
# NORTH,SOUTH,WEST,EAST
# ===================================================

NORTH    = CONS([CONS([MAX(1), MAX(2)]), CONS([MIN(1), MIN(2)])])
SOUTH    = CONS([CONS([MIN(1), MIN(2)]), CONS([MAX(1), MIN(2)])])
WEST     = CONS([CONS([MIN(1), MAX(2)]), CONS([MIN(1), MIN(2)])])
EAST     = CONS([CONS([MAX(1), MIN(2)]), CONS([MAX(1), MAX(2)])])

MXMY = COMP([PLASM_STRUCT, CONS([COMP([COMP([PLASM_T([1, 2]), AA(RAISE( PLASM_DIFF))]), MID([1, 2])]), ID])])
MXBY = COMP([PLASM_STRUCT, CONS([COMP([COMP([PLASM_T([1, 2]), AA(RAISE( PLASM_DIFF))]), CONS([MID(1), MIN(2)])]), ID])])
MXTY = COMP([PLASM_STRUCT, CONS([COMP([COMP([PLASM_T([1, 2]), AA(RAISE( PLASM_DIFF))]), CONS([MID(1), MAX(2)])]), ID])])
LXMY = COMP([PLASM_STRUCT, CONS([COMP([COMP([PLASM_T([1, 2]), AA(RAISE( PLASM_DIFF))]), CONS([MIN(1), MID(2)])]), ID])])
RXMY = COMP([PLASM_STRUCT, CONS([COMP([COMP([PLASM_T([1, 2]), AA(RAISE( PLASM_DIFF))]), CONS([MAX(1), MID(2)])]), ID])])


# ===================================================
# RIF
# ===================================================

def RIF (size):
	thin = 0.01*size
	x=COLOR(RED)(CUBOID([size, thin, thin]))
	y=COLOR(GREEN)(CUBOID([thin, size, thin]))
	z=COLOR(BLUE)(CUBOID([thin, thin, size]))
	return Plasm.Struct([x,y,z])




# ===================================================
# FRACTALSIMPLEX
# ===================================================

def FRACTALSIMPLEX (D):
    def FRACTALSIMPLEX0 (N):

		mkpols = COMP([COMP([COMP([COMP([PLASM_STRUCT, AA(MKPOL)]), AA(AL)]), DISTR]), CONS([ID, K([[FROMTO([1,D+1])], [[1]]])])])

		def COMPONENT (args):
			i, seq = args
			firstseq =   seq[0:i-1]
			pivot    = seq[i-1]
			lastseq = seq[i:len(seq)]
			firstpart = AA(MEANPOINT)(DISTR([firstseq, pivot]))
			lastpart  = AA(MEANPOINT)(DISTR([lastseq , pivot]))
			return CAT([firstpart, [pivot], lastpart])

		expand = COMP([COMP([AA(COMPONENT), DISTR]), CONS([COMP([INTSTO, LEN]), ID])])
		splitting = (COMP([COMP, DIESIS(N)]))((COMP([CAT, AA(expand)])))
	
		return (COMP([COMP([COMP([COMP([mkpols, splitting]), CONS([S1])])])]))(UKPOL(SIMPLEX(D)))

    return FRACTALSIMPLEX0


# ===================================================
# VECT2MAT
# ===================================================

def VECT2MAT(v):
	n=len(v)
	return [[0 if r!=c else v[r] for c in range(n)] for r in range(n)]
	

# ===================================================
# VECT2DTOANGLE
# ===================================================

def VECT2DTOANGLE(v):
	v=UNITVECT(v)
	return math.acos(v[0])*(1 if v[1]>=0 else -1)


# ===================================================
# CART
# ===================================================

def CART(l):
    CART2 = COMP([COMP([CAT, AA(DISTL)]), DISTR])
    F1 = AA((AA(CONS([ID]))))
    return TREE(COMP([AA(CAT), CART2]))(F1(l))


def POWERSET(l):
	return COMP([COMP([AA(CAT), CART]), AA((CONS([CONS([ID]), K([])])))])(l)


if self_test:
	assert len(CART([[1, 2, 3], ['a', 'b'],[10,11]]))==12
	assert len(POWERSET([ 1, 2, 3]) )==8



# ===================================================
# ARC
# ===================================================

def ARC(args):
	degrees , cents = args
	return PI*(degrees+cents)/(100.0*180.0)


# ===================================================
# PYRAMID
# ===================================================


def PYRAMID (H):
	def PYRAMID0(pol):
		barycenter=MEANPOINT(UKPOL(pol)[0])
		return PLASM_JOIN([MK(barycenter+[H]),pol])
	return PYRAMID0


# ===================================================
# MESH
# ===================================================

def MESH (seq):
	return INSL(RAISE(PROD))([QUOTE(i) for i in seq])



# ===================================================
# NU_GRID
# ===================================================


def NU_GRID (data):
	polylines=[POLYLINE(i) for i in data]
	return INSL(RAISE(PROD))(polylines)



# ===================================================
# CURVE2PLASM_MAPVECT
# ===================================================

def CURVE2PLASM_MAPVECT (CURVE):
	D = len((CURVE([0])))
	return [ COMP([SEL(i),CURVE]) for i in FROMTO([1,D]) ]

if self_test:
	temp=CURVE2PLASM_MAPVECT(lambda t: [t[0]+1,t[0]+2])
	assert temp[0]([10])==11
	assert temp[1]([10])==12


# ===================================================
# SEGMENT
# ===================================================

def SEGMENT (sx):
	def SEGMENT0 (args):
		N=len(args[0])
		A,B=args
		P0=A
		P1=[A[i]+(B[i]-A[i])*sx for i in range(N)]

		print P0,P1
		return POLYLINE([P0,P1])
	return SEGMENT0

# ===================================================
# SOLIDIFY
# ===================================================

def SOLIDIFY(pol):
	
	box=Plasm.limits(pol)
	min=box.p1[1]
	max=box.p2[1]
	siz=max-min
	far_point=max+siz*100

	def InftyProject(pol):
		verts,cells,pols=UKPOL(pol)
		verts=[[far_point] + v[1:] for v in verts]
		return MKPOL([verts,cells,pols])

	def IsFull(pol):
		return DIM(pol)==RN(pol)

	ret=SPLITCELLS(pol)
	ret=[PLASM_JOIN([pol,InftyProject(pol)]) for pol in ret]
	return PLASM_XOR(FILTER(IsFull)(ret))

if self_test:

	VIEW(SOLIDIFY(PLASM_STRUCT(AA(POLYLINE)([
		[[0,0],[4,2],[2.5,3],[4,5],[2,5],[0,3],[-3,3],[0,0]],
		[[0,3],[0,1],[2,2],[2,4],[0,3]],
		[[2,2],[1,3],[1,2],[2,2]]]))))

# ===================================================
# EXTRUSION
# ===================================================

def EXTRUSION (angle):
	def EXTRUSION1 (height):
		def EXTRUSION0 (pol):
			dim = DIM(pol)
			cells=SPLITCELLS( SKELETON(dim)(pol) )
			slice=[EMBED(1)(c) for c in cells]
			tensor=COMP([PLASM_T(dim+1)(1.0/height),PLASM_R([dim-1,dim])(angle/height)])
			layer=Plasm.Struct([PLASM_JOIN([p,tensor(p)]) for p in slice])
			return (COMP([COMP([PLASM_STRUCT, CAT]), DIESIS(height)]))([layer, tensor])
		return EXTRUSION0
	return EXTRUSION1

# ===================================================
# EX
# ===================================================

def EX (args):
	x1 ,x2 = args
	def EX0 (pol):
		dim = DIM(pol)
		return PLASM_T(dim+1)(x1)(PLASM_S(dim+1)(x2-x1)(EXTRUSION(0.0)(1.0)(pol)))
	return EX0

# ===================================================
# LEX
# ===================================================

def LEX (args):
	x1 , x2 = args
	def LEX0 (pol):
		def SHEARTENSOR (A):
			def SHEARTENSOR0 (POL):
				dim = DIM(POL)
				newrow = K((AR([CAT([[0, 1],DIESIS((dim-2))(0)]),A])))
				update = (COMP([CONS, CAT]))([[S1, newrow],AA(SEL)((FROMTO([3,dim+1])))])
				matrix=  update(IDNT(dim+1))              
				return (MAT(matrix))(POL)
			return SHEARTENSOR0

		ret=EXTRUSION(0)(1)(pol)
		ret=SHEARTENSOR(x2-x1)(ret)
		ret=S(DIM(pol)+1)(x2-x1)(ret)
		ret=PLASM_T(DIM(pol)+1)(x1)(ret)
		return ret
	return LEX0

# ===================================================
# SEX 
# ===================================================

def SEX (args):
	x1 , x2 = args
	def SEX1 (height):
		def SEX0 (pol):
			dim = DIM(pol)
			ret=EXTRUSION(x2-x1)(height)(pol)
			ret=PLASM_S(dim+1)(x2-x1)(ret)
			ret=PLASM_R([dim,dim-1])(x1)(ret)
			return ret
		return SEX0
	return SEX1

if self_test:

	mypol1 = PLASM_T([1, 2, 3])([-5,-5,0])(CUBOID([10,10]))
	mypol2 = PLASM_S(0.9,0.9,0)(mypol1)
	mypol3 =  PLASM_DIFF([mypol1,mypol2]);

	VIEW(PLASM_STRUCT([
		  EX([0,10])(mypol3), PLASM_T(1)(12) ,
		  LEX([0,10])(mypol3), PLASM_T(1)(25) ,
		   PLASM_S(3)(3)(SEX([0,PI])(16)(mypol3))
		]))

# ===================================================
# POLAR 
# ===================================================

def POLAR(pol,precision=1e-6):
	faces,cells,pols=UKPOLF(pol)
	for i in range(len(faces)):
		mod=-1*faces[i][0]
		if math.fabs(mod)<precision:mod=1
		faces[i]=[value/mod for value in faces[i][1:]]
	return MKPOL([faces,cells,pols]) 
	
if self_test:
	VIEW(POLAR(CUBOID([1,1,1])))

# ===================================================
# SWEEP 
# ===================================================

def SWEEP (v):
    def SWEEP0 (pol):

		ret=Plasm.power(pol,QUOTE([1]))

		# shear operation
		mat=IDNT(len(v)+2)
		for i in range(len(v)):
			mat[i+1][len(v)+1]=v[i]
		ret=MAT(mat)(ret)

		return PROJECT(1)(ret)

    return SWEEP0

# ===================================================
# MINKOWSKI
# ===================================================

def MINKOWSKI (vects):
	def MINKOWSKI0 (pol):
		ret=pol
		for i in range(len(vects)-1,-1,-1):
			ret=SWEEP(vects[i])(ret)
		return ret
	return MINKOWSKI0

if self_test:
	p = MKPOL([[[0,0]],[[1]],[[1]]])
	B = MINKOWSKI([  [-1.0/2.0,-1*math.sqrt(3.0/2.0)] , [-1.0/2.0,math.sqrt(3.0/2.0)] , [1,0] ])(p)
	vertices = [[0,0],[1,0],[1,0.5],[0.5,0.5],[0.5,1],[0,1]]
	pol1D = MKPOL([vertices,[[1,2],[2,3],[3,4],[4,5],[5,6],[6,1]],[[1],[2],[3],[4],[5],[6]]])
	pol2D = MKPOL( [vertices,[[1,2,3,4],[4,5,6,1]],[[1,2]]])
	Min0 = PLASM_STRUCT([PLASM_T([1,2])(v)(PLASM_S([1,2])([0.1,0.1])(B)) for v in vertices ])
	Min1 = MINKOWSKI ([[0.1*-1.0/2.0,0.1*-1*math.sqrt(3.0/2.0)],[0.1*-1.0/2.0,0.1*math.sqrt(3.0/2.0)],[0.1*1,0.1*0]])(pol1D)
	Min2 = MINKOWSKI ([[0.1*-1.0/2.0,0.1*-1*math.sqrt(3.0/2.0)],[0.1*-1.0/2.0,0.1*math.sqrt(3.0/2.0)],[0.1*1,0.1*0]])(pol2D)
	A=Plasm.power(Min2,Q(0.05))
	B=Plasm.power(Min0,Q(0.70))
	C=Plasm.power(Min1,Q(0.05))
	VIEW(PLASM_TOP([PLASM_TOP([A,B]),C]) )

# ===================================================
# OFFSET 
# ===================================================

def OFFSET (v):
	def OFFSET0 (pol):

		ret=pol
		for i in range(len(v)):

			# shear vector
			shear=[0 if j!=i else v[i] for j in range(len(v))] + [0 for j in range(i)]

			# shear operation
			mat=IDNT(len(shear)+2)
			for i in range(len(shear)):
				mat[i+1][len(shear)+1]=shear[i]
			
			# apply shearing
			ret=MAT(mat)((Plasm.power(ret,QUOTE([1]))))

		return PROJECT(len(v))(ret)
	return OFFSET0

if self_test:
	verts = [[0,0,0],[3,0,0],[3,2,0],[0,2,0],[0,0,1.5],[3,0,1.5],[3,2,1.5],[0,2,1.5],[0,1,2.2],[3,1,2.2]]
	cells = [[1,2],[2,3],[3,4],[4,1],[5,6],[6,7],[7,8],[8,5],[1,5],[2,6],[3,7],[4,8],[5,9],[8,9],[6,10],[7,10], [9,10]]
	pols = [[1]]
	House = MKPOL([verts,cells,pols])
	out=Plasm.Struct([ OFFSET([0.1,0.2,0.1])(House), PLASM_T(1)(1.2*SIZE(1)(House))(House)])
	VIEW(out)


# //////////////////////////////////////////////////////////////////
# THINSOLID
# //////////////////////////////////////////////////////////////////
def THINSOLID (surface,delta=1e-4):

	def map_fn(point):

		u,v,w=point
		# calculate normal as cross product of its gradient
		P0=surface([u,v])
		PX=surface([u+delta,v])
		PY=surface([u,v+delta])
		GX=[PX[i]-P0[i] for i in range(3)]
		GY=[PY[i]-P0[i] for i in range(3)]
		normal=UNITVECT(VECTPROD([GX,GY]))
		ret=[P0[i]+w*normal[i] for i in range(3)]

		return ret

	return map_fn

if self_test:
	Su0 = COMP([PLASM_BEZIERCURVE([[0,0,0],[10,0,0]]),CONS([S1])])
	Su1 = COMP([PLASM_BEZIERCURVE([[0,10,0],[2.5,10,3],[5,10,-3],[7.5,10,3],[10,10,0]]),CONS([S1]) ])
	S0v = COMP([PLASM_BEZIERCURVE([[0,0,0],[0,0,3],[0,10,3],[0,10,0]]) , CONS([S2]) ]) 
	S1v = COMP([PLASM_BEZIERCURVE([[10,0,0],[10,5,3],[10,10,0]]) ,CONS([S2])   ])
	surface=PLASM_COONSPATCH([Su0,Su1,S0v,S1v])
	VIEW(PLASM_MAP(  surface ) (Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))))
	solidMapping = THINSOLID(surface)
	Domain3D = Plasm.power(Plasm.power(PLASM_INTERVALS(1)(5),PLASM_INTERVALS(1)(5)),PLASM_INTERVALS(0.5)(5))
	VIEW(PLASM_MAP(solidMapping)(Domain3D))

	
# //////////////////////////////////////////////////////////////////
# PLANE
# //////////////////////////////////////////////////////////////////

def PLANE (args):

	p0 , p1 , p2 = args
	v1 = VECTDIFF([p1,p0])
	v2 = VECTDIFF([p2,p0])

	side1 = VECTNORM(v1)
	side2 = VECTNORM(v2)

	normal=UNITVECT(VECTPROD([v1,v2]))
	axis=VECTPROD([[0, 0, 1],normal])
	angle = math.acos((INNERPROD([[0, 0, 1],normal])))

	geometry=PLASM_T([1,2,3])(p0)(ROTN([angle, axis])(PLASM_T([1,2])([-1*side1,-1*side2]) (CUBOID([2*side1, 2*side2]))))
	return  [normal, p0, geometry]


# //////////////////////////////////////////////////////////////////
# RATIONAL PLASM_BEZIER
# //////////////////////////////////////////////////////////////////

def RATIONALPLASM_BEZIER (controlpoints_fn):
	degree = len(controlpoints_fn)-1
	basis=BERNSTEINBASIS(S1)(degree)

	def map_fn(point):

		# if control points are functions
		controlpoints=[f(point) if callable(f) else f for f in controlpoints_fn]

		target_dim=len(controlpoints[0])

		ret=[0 for i in range(target_dim)]
		for i in range(len(basis)):
			coeff=basis[i](point)
			for M in range(target_dim):
				ret[M]+=coeff * controlpoints[i][M] 

		# rationalize (== divide for the last value)
		last=ret[-1]
		if last!=0: ret=[value/last for value in ret]
		ret=ret[:-1]

		return  ret

	return map_fn



# //////////////////////////////////////////////////////////////////
# ELLIPSE
# //////////////////////////////////////////////////////////////////


def ELLIPSE (args):
    raise NameError('Command ELLIPSE is available starting with Basic Plan.')
    A , B = args
    def ELLIPSE0 (N):
        C = 0.5*math.sqrt(2)
        mapping = RATIONALPLASM_BEZIER([[A, 0, 1], [A*C, B*C, C], [0, B, 1]])
        quarter = PLASM_MAP(mapping)((PLASM_INTERVALS(1.0)(N)))
        half = PLASM_STRUCT([quarter, PLASM_S(2)(-1)(quarter)])
        return PLASM_STRUCT([half, PLASM_S(1)(-1)(half)])
    return ELLIPSE0


if self_test:
	VIEW(ELLIPSE([1,2])(8))




# //////////////////////////////////////////////////////////////////
# NORM2 (==normal of a curve)
# //////////////////////////////////////////////////////////////////

def CURVE_NORMAL(curve):

	def map_fn(point):
		xu,yu=curve(point)
		
		mod2=xu*xu+yu*yu
		den=math.sqrt(mod2) if mod2>0 else 0

		return [-yu/den,xu/den]

	return map_fn

# //////////////////////////////////////////////////////////////////
# DERPLASM_BEZIER
# //////////////////////////////////////////////////////////////////

def DERPLASM_BEZIER (controlpoints_fn):
	degree = len(controlpoints_fn)-1

	# derivative of bernstein
	def DERBERNSTEIN (N):
		def DERBERNSTEIN0 (I):
			def map_fn(point):
				t=S1(point)
				return CHOOSE([N,I]) * math.pow(t,I-1) * math.pow(1-t,N-I-1) * (I-N*t)
			return  map_fn
		return DERBERNSTEIN0


	basis=[DERBERNSTEIN(degree)(i) for i in range(degree+1)]

	def map_fn(point):

		# if control points are functions
		controlpoints=[f(point) if callable(f) else f for f in controlpoints_fn]

		target_dim=len(controlpoints[0])

		ret=[0 for i in range(target_dim)]
		for i in range(len(basis)):
			coeff=basis[i](point)
			for M in range(target_dim):
				ret[M]+=coeff * controlpoints[i][M] 

		return ret

	return map_fn


# //////////////////////////////////////////////////////////////////
# PLASM_BEZIERSTRIPE
# //////////////////////////////////////////////////////////////////

def PLASM_BEZIERSTRIPE (args):
	controlpoints, width, n = args

	bezier  = PLASM_BEZIERCURVE(controlpoints)
	normal  = CURVE_NORMAL(DERPLASM_BEZIER(controlpoints))


	def map_fn(point):

		u,v=point
		bx,by=bezier (point)
		nx,ny=normal (point)
		ret=[bx+v*nx,by+v*ny]

		return ret

	domain=PLASM_S(2)(width)(PLASM_T(1)(0.00001)(Plasm.power(PLASM_INTERVALS(1)(n),PLASM_INTERVALS(1)(1))))
	return PLASM_MAP(map_fn)(domain)

if self_test:
	vertices=[[0,0],[1.5,0],[-1,2],[2,2],[2,0]]
	VIEW(Plasm.Struct([ POLYLINE(vertices) , Plasm.power(PLASM_BEZIERSTRIPE([vertices,0.25,22]),QUOTE([0.9]))  ]))





# ===================================================
# BSPLINE see http://www.idav.ucdavis.edu/education/CAGDNotes/B-Spline-Curve-Definition.pdf
# ===================================================


def BSPLINE (degree):
	def BSPLINE0 (knots):
		def BSPLINE1 (points_fn):

			n=len(points_fn)-1
			m=len(knots)-1
			k=degree+1
			T=knots
			tmin,tmax=T[k-1],T[n+1]

			# see http://www.na.iac.cnr.it/~bdv/cagd/spline/B-spline/bspline-curve.html
			if len(knots)!=(n+k+1):
				raise Exception("Invalid point/knots/degree for bspline!")

			# de boord coefficients
			def N(i,k,t):

				# Ni1(t)
				if k==1: 
					if (t>=T[i] and t<T[i+1]) or (t==tmax and t>=T[i] and t<=T[i+1]): # i use strict inclusion for the max value
						return 1
					else:
						return 0

				# Nik(t)
				ret=0

				num1,div1= t-T[i], T[i+k-1]-T[i]  
				if div1!=0: ret+=(num1/div1) * N(i,k-1,t)

				num2,div2=T[i+k]-t, T[i+k]-T[i+1]
				if div2!=0:  ret+=(num2/div2) * N(i+1,k-1,t)

				return ret

			# map function
			def map_fn(point):
				t=point[0]

				# if control points are functions
				points=[f(point) if callable(f) else f for f in points_fn]

				target_dim=len(points[0])
				ret=[0 for i in range(target_dim)];
				for i in range(n+1):
					coeff=N(i,k,t) 
					for M in range(target_dim):
						ret[M]+=points[i][M]*coeff
				return ret

			return map_fn

		return BSPLINE1
	return BSPLINE0



# ===================================================
# NUBSPLINE
# ===================================================

def NUBSPLINE(degree,totpoints=80):
	def NUBSPLINE1(knots):
		def NUBSPLINE2(points):
			m=len(knots)
			tmin=min(knots)
			tmax=max(knots)
			tsiz=tmax-tmin
			v=[tsiz/float(totpoints-1) for i in range(totpoints-1)]
			assert len(v)+1==totpoints
			v=[-tmin] + v
			domain=QUOTE(v)
			return PLASM_MAP(BSPLINE(degree)(knots)(points))(domain)
		return NUBSPLINE2
	return NUBSPLINE1

# ===================================================
# DISPLAYNUBSPLINE
# ===================================================

def DISPLAYNUBSPLINE (args,marker_size=0.1):
	degree, knots, points = args

	spline_view_knots=POLYMARKER(2,marker_size)(UKPOL(NUBSPLINE(degree,len(knots))(knots)(points))[0])

	return  PLASM_STRUCT([
		NUBSPLINE(degree)(knots)(points) if degree>0 else POLYMARKER(3,marker_size)(points)
		,spline_view_knots
		,POLYLINE(points)
		,POLYMARKER(1,marker_size)(points)
	])


if self_test:
	ControlPoints=[[0,0],[-1,2],[1,4],[2,3],[1,1],[1,2],[2.5,1], [2.5,3], [4,4],[5,0]]
	VIEW(DISPLAYNUBSPLINE([3,[0,0,0,0, 1,2,3,4,5, 6    ,7,7,7,7], ControlPoints]))


# =================================================
# RATIONALBSPLINE
# =================================================    


def RATIONALBSPLINE (degree):
	def RATIONALBSPLINE0 (knots):
		def RATIONALBSPLINE1 (points):

			bspline=BSPLINE(degree)(knots)(points)

			def map_fn(point):			

				ret=bspline(point)

				# rationalize (== divide for the last value)
				last=ret[-1]
				if last!=0: ret=[value/last for value in ret]
				ret=ret[:-1]
				return ret

			return map_fn

		return RATIONALBSPLINE1
	return RATIONALBSPLINE0


# =================================================
# NURBSPLINE
# =================================================

def NURBSPLINE(degree,totpoints=80):
	def NURBSPLINE1(knots):
		def NURBSPLINE2(points):
			m=len(knots)
			tmin=min(knots)
			tmax=max(knots)
			tsiz=tmax-tmin
			v=[tsiz/float(totpoints-1) for i in range(totpoints-1)]
			assert len(v)+1==totpoints
			v=[-tmin] + v
			domain=QUOTE(v)
			return PLASM_MAP(RATIONALBSPLINE(degree)(knots)(points))(domain)
		return NURBSPLINE2
	return NURBSPLINE1


# ===================================================
# DISPLAYNURBSPLINE
# ===================================================


def DISPLAYNURBSPLINE (args,marker_size=0.1):
	degree, knots, points = args

	spline_view_knots=POLYMARKER(2,marker_size)(UKPOL(NURBSPLINE(degree,len(knots))(knots)(points))[0])

	return  PLASM_STRUCT([
		NURBSPLINE(degree)(knots)(points) if degree>0 else POLYMARKER(3,marker_size)(points)
		,spline_view_knots
		,POLYLINE(points)
		,POLYMARKER(1,marker_size)(points)
	])


if self_test:
	knots = [0,0,0,1,1,2,2,3,3,4,4,4]
	_p=math.sqrt(2)/2.0
	controlpoints = [[-1,0,1], [-_p,_p,_p], [0,1,1], [_p,_p,_p],[1,0,1], [_p,-_p,_p], [0,-1,1], [-_p,-_p,_p], [-1,0,1]]
	VIEW(DISPLAYNURBSPLINE([2, knots, controlpoints]))



#===================================================================================
# Colors (wants a list [R,G,B] or [R,G,B,A]
# Example COLOR([1,0,0])(pol)
#===================================================================================

def COLOR(C):

	def formatColor(C):
		assert isinstance(C,Color4f) 
		return "%s %s %s %s" % (C.r,C.g,C.b,C.a)

	# convert list to Color
	if isinstance(C,list) and len(C) in (3,4):
		C=Color4f(C[0],C[1],C[2],C[3] if len(C)>=4 else 1.0)

	if not isinstance(C,Color4f):
		raise Exception("cannot transform " + repr(C) + " to Color4f")

	def COLOR0(pol):
		return Plasm.addProperty(pol, "RGBcolor", formatColor(C))

	return COLOR0

GRAY    = Color4f([0.5, 0.5, 0.5, 1.0])
GREEN   = Color4f([0.0, 1.0, 0.0, 1.0])
BLACK   = Color4f([0.0, 0.0, 0.0, 1.0])
BLUE    = Color4f([0.0, 0.0, 1.0, 1.0])
BROWN   = Color4f([0.5, 0.5, 0.5, 1.0])
CYAN    = Color4f([0.0, 1.0, 1.0, 1.0])
MAGENTA = Color4f([1.0, 0.0, 1.0, 1.0])
ORANGE  = Color4f([1.0, 0.5, 1.0, 1.0])
PURPLE  = Color4f([0.5, 0.0, 0.5, 1.0])
WHITE   = Color4f([1.0, 1.0, 1.0, 1.0])
RED     = Color4f([1.0, 0.0, 0.0, 1.0])
YELLOW  = Color4f([1.0, 1.0, 0.0, 1.0])



if self_test: 
   (Plasm.getProperty(COLOR(RED)(Plasm.cube(3)),"RGBcolor")==("%s %s %s %s" % (1.0,0.0,0.0,1.0)))


#===================================================================================
# Materials (want a list of 17 elements(ambientRGBA, diffuseRGBA specularRGBA emissionRGBA shininess)
# Example MATERIAL([1,0,0,1,  0,1,0,1,  0,0,1,0, 0,0,0,1, 100])(pol)
#===================================================================================

def MATERIAL(M):

	def MATERIAL0(pol):

		svalue="%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" % (M[ 0],M[ 1],M[ 2],M[ 3],M[ 4],M[ 5],M[ 6],M[ 7],M[ 8],M[ 9],M[10],M[11],M[12],M[13],M[14],M[15],M[16])
		return Plasm.addProperty(pol, "VRMLmaterial", svalue) 

	# convert list to Material
	if isinstance(M,list) and (len(M)==3 or len(M)==4):
		r,g,b=M[0:3]
		a=M[3] if len(M)==4 else 1.0
		ambient =[r*0.4,g*0.4,b*0.4,alpha]
		diffuse =[r*0.6,g*0.6,b*0.6,alpha]
		specular=[0    ,0    ,0    ,alpha]
		emission=[0    ,0    ,0    ,alpha]
		shininess
		M=ambient + diffuse + specular + emission + [shininess]

	#convert the list to a XGE material
	if not (isinstance(M,list) and len(M)==17):
		raise Exception("cannot transform " + repr(M) + " in a material (which is a list of 17 floats, ambient,diffuse,specular,emission,shininess)")

	return MATERIAL0

if self_test:
   (Plasm.getProperty(MATERIAL([1,0,0,1,  0,1,0,1,  0,0,0,1,  0,0,0,1,  100])(Plasm.cube(3)),"VRMLmaterial")==[1,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,100])



#===================================================================================
# Textures (wants a list [url:string,repeatS:bool,repeatT:bool,cx::float,cy::float,rot::float,sx::float,sy::float,tx::float,ty::float]
# Example TEXTURE('filename.png')(pol)
#===================================================================================

def TEXTURE(params):

	def TEXTURE0(params,pol):

		# is simply an URL
		if isinstance(params,str):
			url=params
			params=[]
		# is a list with a configuration
		else:
			assert isinstance(params,list) and len(params)>=1
			url=params[0]
			if not isinstance(url,str): 
				raise Exception("Texture error " + repr(url) + " is not a path")
			params=params[1:]

		# complete with default parameters
		params+=[True,True, 0.0,0.0,  0.0,   1.0,1.0,    0.0,0.0   ][len(params):]

		# unpack
		repeatS, repeatT, cx, cy, rot, sx, sy, tx, ty=params

		spacedim = Plasm.getSpaceDim(pol)
		
		if not (spacedim in (2,3)):
			# raise Exception("Texture cannot be applyed only to 2 or 3 dim pols")
			return Plasm.copy(pol)

		box = Plasm.limits(pol)
		ref0,ref1=[box.maxsizeidx(),box.minsizeidx()]

		if (spacedim==3):
			ref1=1 if (ref0!=1 and ref1!=1) else (2 if (ref0!=2 and ref1!=2) else 3)
			
		assert ref0!=ref1
		
		# empty box
		if (box.size()[ref0]==0 or box.size()[ref1]==0):
			return Plasm.copy(pol)
		
		# translate vector
		vt=Vecf(0.0, \
			-box.p1[1] if box.dim()>=1 else 0.0, \
			-box.p1[2] if box.dim()>=2 else 0.0, \
			-box.p1[3] if box.dim()>=3 else 0.0)
		
		# scale vector
		vs=Vecf(0.0, \
			1.0/(box.size()[1]) if box.dim()>=1 and box.size()[1] else 1.0, \
			1.0/(box.size()[2]) if box.dim()>=2 and box.size()[2] else 1.0, \
			1.0/(box.size()[3]) if box.dim()>=3 and box.size()[3] else 1.0)
		
		# permutation
		refm=1 if (ref0!=1 and ref1!=1) else (2 if (ref0!=2 and ref1!=2) else 3)
		assert ref0!=ref1 and ref1!=refm and ref0!=refm
		perm=[0,0,0,0]
		perm[ref0]=1
		perm[ref1]=2
		perm[refm]=3 


		project_uv=Matf.translateV (Vecf(0.0,+cx,+cy,0)) \
				* Matf.scaleV (Vecf(0.0,sx,sy,1)) \
				* Matf.rotateV(3,1,2,-rot) \
				* Matf.translateV (Vecf(0.0,-cx,-cy,0)) \
				* Matf.translateV (Vecf(0.0,tx,ty,0))  \
				* Matf(3).swapCols(perm) \
				* Matf.scaleV     (vs) \
				* Matf.translateV (vt)


		return Plasm.Skin(pol,url,project_uv)

	return lambda pol: TEXTURE0(params,pol)

if self_test:
	VIEW(TEXTURE(":images/gioconda.png")(CUBOID([1,1])))



# //////////////////////////////////////////////////////////////
def BOUNDARY(hpc,dim):

	"""
		Find all boundary faces of dimension <cell_dim> inside an hpc,
		Extract only faces from FULL hpc, skipping "embedded" hpc 
	"""

	# here i will store the return value, ie all the boundary cells
	vertex_db=[]
	faces_db =[]

	def getCells(g,dim):
		""" local utility: get all cells of a certain dimension inside an hasse diagram """
		ret=[]
		it=g.each(dim)
		while not it.end():
			ret.append(it.getNode())
			it.goForward()
		return ret

	def getVerticesId(g,cell):

		""" local utility: return all vertices id of a generic cell inside an hasse diagram """

		# special navigator to find cells inside an hasse diagram
		nav=GraphNavigator()

		# extract all vertices if from this face
		nv=g.findCells(0, cell,nav)
	
		return [nav.getCell(0,I) for I in range(nv)]


	# flat the hpc to two levels
	temp=Plasm.shrink(hpc,False)

	for node in temp.childs:

		# this is the hasse diagram
		g=node.g

		# no geometry in the node, useless hpc node
		if g is None: continue

		# check if the hpc is  "full", and not "embedded"
		if node.spacedim!=node.pointdim or node.pointdim!=g.getPointDim(): 
			continue

		# this hpc is in different dimension
		if (dim+1)!=node.pointdim: 
			continue

		# this is the transformation matrix inside the child hpc
		T=node.vmat

		# iterate in all <dim>-cells
		for face in getCells(g,dim):

			# it's an internal face
			if g.getNUp(face)==2: continue 

			new_face=[]

			# this is the new boundary face	
			for Id in getVerticesId(g,face):

				# get the geometry as a Vecf and transform using T
				vertex =T * g.getVecf(Id)

				# convert the Vecf to a python list	(removing the homo components)		
				vertex=[vertex[i]/vertex[0] for i in range(1,dim+2)]

				if not vertex in vertex_db:
					vertex_db.append(vertex)

				new_face.append(vertex_db.index(vertex))

			# consider it as the unordered list of vertex indices, I sort it
			faces_db.append(sorted(new_face))
				
	return [vertex_db,faces_db]
	
	


print "...fenvs.py imported in",(time.clock() - start),"seconds"


