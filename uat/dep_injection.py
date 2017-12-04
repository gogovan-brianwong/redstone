# -*- coding=utf-8 -*-


class Mapper(object):
    # 在字典里定义依赖注入关系
    __mapper_relation = {}

    # 类直接调用注册关系
    @staticmethod
    def register(cls, value):
        Mapper.__mapper_relation[cls] = value

    @staticmethod
    def exist(cls):
        if cls in Mapper.__mapper_relation:
            return True
        return False

    @staticmethod
    def get_value(cls):
        return Mapper.__mapper_relation[cls]


class MyType(type):
    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        arg_list = list(args)
        if Mapper.exist(cls):
            value = Mapper.get_value(cls)
            arg_list.append(value)
        obj.__init__(*arg_list, **kwargs)
        return obj


class Head(object):
    def __init__(self):
        self.name = 'brian'


class Foo(metaclass=MyType):

    def __init__(self, h):
        self.h = h

    def f1(self):
        print(self.h)


class Bar(metaclass=MyType):

    def __init__(self, f):
        self.f = f

    def f2(self):
        print(self.f)


if __name__ == '__main__':

    Mapper.register(Foo, Head())
    Mapper.register(Bar, Foo())

    b1 = Bar()
    print(b1.f.h.name)
    # head = Mapper.get_value(Foo)
    # print('1111111')
    # print (head)
    # print (head.name)
    # print ('2222222')
    # foo = Mapper.get_value(Bar)
    # print (foo)
    # print (foo.h.name)
    # print ('3333333')
    # b = Bar()
    # print(b.f)
    # print (b.f.h.name)




########################333

# class MyType(type):
#     def __call__(cls, *args, **kwargs):
#         obj = cls.__new__(cls, *args, **kwargs)
#         print(u'在这里面..')
#         obj.__init__(*args, **kwargs)
#         return obj
#
#
# class Foo(metaclass=MyType):
#
#
#     def __init__(self):
#         self.name = 'alex'
#
# if __name__ == '__main__':
#     f = Foo()
#     print(f.name)

###############################


