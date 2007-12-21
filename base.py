CO_VARARGS = 4
CO_VARKEYWORDS = 8

class Element(object): 
  def __init__(self, __name__, __doc__=''):
    """
    """
    if not __doc__ and __name__.find(' ') >= 0:
        __doc__ = __name__
        __name__ = None

    self.__name__=__name__
    self.__doc__=__doc__

  def getName(self):
    """ Returns the name of the object. """
    return self.__name__

  def getDoc(self):
    """ Returns the documentation for the object. """
    return self.__doc__

class Attribute(Element):
    """Attribute descriptions
    """

    # We can't say this yet because we don't have enough
    # infrastructure in place.
    #
    # implements(IAttribute)

    interface = None


class Method(Attribute):
    """Method interfaces

    The idea here is that you have objects that describe methods.
    This provides an opportunity for rich meta-data.
    """

    # We can't say this yet because we don't have enough
    # infrastructure in place.
    #
    # implements(IMethod)

    def __call__(self, *args, **kw):
        raise BrokenImplementation(self.interface, self.__name__)

    def getSignatureInfo(self):
        return {'positional': self.positional,
                'required': self.required,
                'optional': self.optional,
                'varargs': self.varargs,
                'kwargs': self.kwargs,
                }

    def getSignatureString(self):
        sig = []
        for v in self.positional:
            sig.append(v)
            if v in self.optional.keys():
                sig[-1] += "=" + `self.optional[v]`
        if self.varargs:
            sig.append("*" + self.varargs)
        if self.kwargs:
            sig.append("**" + self.kwargs)

        return "(%s)" % ", ".join(sig)

def fromFunction(func, interface=None, imlevel=0, name=None):
    name = name or func.__name__
    method = Method(name, func.__doc__)
    defaults = func.func_defaults or ()
    code = func.func_code
    # Number of positional arguments
    na = code.co_argcount-imlevel
    names = code.co_varnames[imlevel:]
    opt = {}
    # Number of required arguments
    nr = na-len(defaults)
    if nr < 0:
        defaults=defaults[-nr:]
        nr = 0

    # Determine the optional arguments.
    opt.update(dict(zip(names[nr:], defaults)))

    method.positional = names[:na]
    method.required = names[:nr]
    method.optional = opt

    argno = na

    # Determine the function's variable argument's name (i.e. *args)
    if code.co_flags & CO_VARARGS:
        method.varargs = names[argno]
        argno = argno + 1
    else:
        method.varargs = None

    # Determine the function's keyword argument's name (i.e. **kw)
    if code.co_flags & CO_VARKEYWORDS:
        method.kwargs = names[argno]
    else:
        method.kwargs = None

    method.interface = interface

    for key, value in func.__dict__.items():
        method.setTaggedValue(key, value)

    return method


def fromMethod(meth, interface=None, name=None):
    func = meth.im_func
    return fromFunction(func, interface, imlevel=1, name=name)
