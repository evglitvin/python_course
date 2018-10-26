class Enum(object):
    __values__ = None

    @classmethod
    def to_string(cls, key):
        try:
            return "{}.{}".format(cls.__name__, cls.__values__[key])
        except TypeError:
            try:
                n_dict = {item[1]: item[0] for item in cls.__dict__.iteritems()}
                cls.__values__ = n_dict
                return "{}.{}".format(cls.__name__, cls.__values__[key])
            except KeyError:
                return "UNKNOWN"
        except KeyError:
            return "UNKNOWN"