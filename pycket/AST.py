
class AST(object):
    _attrs_ = ["should_enter", "mvars", "surrounding_lambda", "source_index"]
    _immutable_fields_ = ["should_enter?", "surrounding_lambda", "source_index?"]
    _settled_ = True

    should_enter = False # default value
    mvars = None
    surrounding_lambda = None

    simple = False
    #source_index = 1000000000

    def defined_vars(self): return {}

    def interpret(self, env, cont):
        from pycket.interpreter import return_value
        # default implementation for simple AST forms
        assert self.simple
        return return_value(self.interpret_simple(env), env, cont)

    def interpret_simple(self, env):
        raise NotImplementedError("abstract base class")

    def set_surrounding_lambda(self, lam):
        from pycket.interpreter import Lambda
        assert isinstance(lam, Lambda)
        self.surrounding_lambda = lam
        for child in self.direct_children():
            child.set_surrounding_lambda(lam)

    def traceworthy(self):
        for c in self.direct_children():
            if c.traceworthy():
                return True
        return False

    def direct_children(self):
        return []

    def free_vars(self):
        free_vars = {}
        for child in self.direct_children():
            free_vars.update(child.free_vars())
        return free_vars

    def assign_convert(self, vars, env_structure):
        """ make a copy of the AST that converts all writable variables into
        using cells. In addition, compute the state of the environment for
        every AST node that needs to know.

        The vars argument contains the variables that need to use cells.
        The env_structure is an instance of SymList (or None) describing the
        environment at that AST node.
        """
        raise NotImplementedError("abstract base class")

    def mutated_vars(self):
        if self.mvars is not None:
            return self.mvars
        self.mvars = self._mutated_vars()
        return self.mvars

    def _mutated_vars(self):
        raise NotImplementedError("abstract base class")

    def tostring(self):
        return "UNKNOWN AST: "

    def __str__(self):
        return self.tostring()

