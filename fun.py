#!/usr/local/bin/python

import math
import random

class Complex:
    def __init__(self, a, b=0, roundOff=False):
        self.real = a
        self.imag = b
      
    def round(self):
        # floats get strange, so compute with as much precision as you
        # can (math.sqrt(2) and others) then call round() at very end to
        # see if the result os squared roots gets you back home
        return Complex(round(self.real,4), round(self.imag,4))

    def sqrt(self):
        if not self.imag:
            return Complex(math.sqrt(self.real))
            
        # from http://math.stackexchange.com/questions/44406/how-do-i-get-the-square-root-of-a-complex-number
        # there are two square roots per given complex number
        # TODO: possibly randomize between the two possible
        # TODO: check that parameter is ok for this formula?
        av = self.absValue()
        r = Complex(av)
        sqrtR = Complex(math.sqrt(av))
        numerator = sqrtR * (self + r)
        denominator = Complex((self + r).absValue())
        return numerator/denominator

    @staticmethod
    def random():
        # 0 <= r,i <= 1 so you can multiply to scale up
        r = random.getrandbits(64)/(2.0**64)
        i = random.getrandbits(64)/(2.0**64)
        return Complex(r, i)

    def absValue(self):
        # note: you do NOT square the i
        return math.sqrt(self.real**2 + self.imag**2)

    def modulus(self):
        return self.absValue()

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        # re-arranged FOIL
        r = self.real * other.real + -1*(self.imag * other.imag)
        i = self.real * other.imag + self.imag * other.real
        return Complex(r,i)

    def __div__(self, other):
        divisor = (other.conj() * other.conj()).real
        temp = self * other.conj()
        temp.real /= divisor
        temp.imag /= divisor
        return temp

    def __eq__(self, other):
        tmpA = self.round()
        tmpB = other.round()
        return tmpA.real == tmpB.real and tmpA.imag == tmpB.imag

    def conj(self):
        return Complex(self.real, -1*self.imag)

    def __str__(self):
        if self.imag:
            if self.imag > 0:
                return "%f+%fi" % (self.real, self.imag)
            else:
                return "%f%fi" % (self.real, self.imag)
        else:
            return str(self.real)

# polarization is represented as a 2-dim vector space over the complex numbers
class Polarization:
    def __init__(self,a=0,b=0):
        # TODO: verify that incoming params are orthogonal
        # TODO: verify that incoming params make magnitude 1
        self.a = a;
        self.b = b;

    # dot product returns a scalar, since we're a 2-dim vector space over the
    # complex numbers, our scalars are complex numbers
    def dotProd(self, other):
        return self.a*other.a + self.b*other.b

    def toComplexRepresentation(self):
        return self.b / self.a

    def fromComplexRepresentation(self, alpha):
        self.a = self.b = 1/sqrt(1+alpha.magnitude()**2)

    def magnitude(self):
        # remember the scalar of this vector space is a complex
        return (self.a*self.a + self.b*self.b).sqrt()

    def __eq__(self, other)
        # two representations are equal if they're multiples modulus 1
        # kinda

    @staticmethod
    def random():
        a = Complex.random()
        b = (Complex(1)-a*a).sqrt()
        return Polarization(a, b)

    @staticmethod
    def hadamard():
        st = math.sqrt(2)
        a = Complex(st, st)
        b = Complex(-st, st)
        return Polarization(a, b)

    def __str__(self):
        return "(%s)|0>+(%s)|1>" % (self.a, self.b)

# test that (2+3i)*(4+5i)==-7+22i
# test that (2+3i)*conj(2+3i)==13
# test that (4+2i)/(3-i) = 1+i
