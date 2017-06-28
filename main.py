class PropAdder(object):
    def __get__(self, instance, owner):
        self.instance = instance
        self.owner = owner
        return self


class HelperPropAdder(object):
    def __init__(self, name):
        self.template = '%s'
        self.name = name

    def __getattr__(self, value):
        setattr(self.instance, self.name, value)


class BoolPropAdder(PropAdder):
    TEMPLATE_CHOICE = {
        str(True): 'is_a_%s',
        str(False): 'is_a_%s',
    }

    def __init__(self, mutator_value):
        self.mutator_value = mutator_value

    def __get__(self, instance, owner):
        self.instance = instance
        self.owner = owner
        return self

    def __getattr__(self, name):
        for template in self.TEMPLATE_CHOICE.values():
            if hasattr(self.instance, template % name):
                delattr(self.instance, template % name)
        setattr(self.instance, self.template % name, self.mutator_value)

    @property
    def template(self):
        return self.TEMPLATE_CHOICE[str(self.mutator_value)]


class ValuePropAdder(PropAdder):
    HELPER_PROP_NAME = '___helper___'
    helper_prop_adder = HelperPropAdder(name=HELPER_PROP_NAME)

    def __getattr__(self, name):
        self.helper_prop_adder.name = name
        self.helper_prop_adder.instance = self.instance
        return self.helper_prop_adder


class ThingMeta(type):
    def __init__(self, name, bases, attrs):
        self.is_a = BoolPropAdder(mutator_value=True)
        self.is_not_a = BoolPropAdder(mutator_value=False)
        self.is_the = ValuePropAdder()
        self.__init__ = self.__override_init__
        super(ThingMeta, self).__init__(name, bases, attrs)

    def __override_init__(self, name, is_child=False, *args, **kwargs):
        self.name = name
        self.__is_child__ = is_child


class Thing(object):
    __metaclass__ = ThingMeta






