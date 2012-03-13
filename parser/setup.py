from distutils.core import setup, Extension

module1 = Extension("parser",sources = ['parsermodule.c','parser.c'])

setup (name = 'parser',
		version = '1.0',
		description = 'C parser',
		ext_modules = [module1])


