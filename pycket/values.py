from rpython.tool.pairtype import extendabletype

class W_Object:
    __metaclass__ = extendabletype
    def call(self, args, env, frame):
        raise Exception ("not callable")

class W_Cons(W_Object):
    def __init__(self, a, d):
        self.car = a
        self.cdr = d

class W_Number(W_Object):
    pass


class W_Fixnum(W_Number):
    def __init__(self, val):
        self.value = val

class W_Flonum(W_Number):
    def __init__(self, val):
        self.value = val

class W_Bignum(W_Number):
    def __init__(self, val):
        self.value = val

class W_Void (W_Object):
    def __init__(self): pass

class W_Null (W_Object):
    def __init__(self): pass

w_void = W_Void()
w_null = W_Null()

class W_Bool(W_Object):
    @staticmethod
    def make(b):
        if b: return w_true
        else: return w_false
    def __init__(self, val):
        self.value = val

w_false = W_Bool(False)
w_true = W_Bool(True)

class W_String(W_Object):
    def __init__(self, val):
        self.value = val

class W_Symbol(W_Object):
    all_symbols = {}
    @staticmethod
    def make(string):
        assert isinstance(string, str)
        if string in W_Symbol.all_symbols:
            return W_Symbol.all_symbols[string]
        else:
            W_Symbol.all_symbols[string] = w_result = W_Symbol(string)
            return w_result
    def __repr__(self):
        return self.value
    def __init__(self, val):
        self.value = val

class W_SimplePrim (W_Object):
    def __init__ (self, name, code):
        self.name = name
        self.code = code

    def call(self, args, env, frame):
        from pycket.interpreter import Value
        return Value(self.code(args)), env, frame

class W_Prim (W_Object):
    def __init__ (self, name, code):
        self.name = name
        self.code = code

    def call(self, args, env, frame):
        return self.code(args, env, frame)

def to_list(l):
    if not l:
        return w_null
    else:
        return W_Cons(l[0], to_list(l[1:]))

class W_Continuation (W_Object):
    def __init__ (self, frame):
        self.frame = frame
    def call(self, args, env, frame):
        from pycket.interpreter import Value
        a, = args # FIXME: multiple values
        return Value(a), env, self.frame

class W_Closure (W_Object):
    def __init__ (self, lam, env):
        self.lam = lam
        self.env = env
    def call(self, args, env, frame):
        from pycket.interpreter import make_begin, ConsEnv
        fmls_len = len(self.lam.formals)
        args_len = len(args)
        if fmls_len != args_len and not self.lam.rest:
            raise Exception("wrong number of arguments, expected %s but got %s"%fmls_len,args_len)
        if fmls_len > args_len:
            raise Exception("wrong number of arguments, expected at least %s but got %s"%fmls_len,args_len)
        if self.lam.rest:
            return make_begin(self.lam.body, ConsEnv ([self.lam.rest] + self.lam.formals,
                                                      [to_list(args[fmls_len:])] + args[0:fmls_len],
                                                      self.env),
                              frame)
        else:
            return make_begin(self.lam.body, ConsEnv(self.lam.formals, args, self.env), frame)


