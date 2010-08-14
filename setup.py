from setuptools import setup, find_packages
import os

version = '0.5dev'

setup(name='dexterity.draftspreviewbehavior',
      version=version,
      description="Preview behavior to show modified content before saving in default view",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone draft dexterity content',
      author='Jason Mehring',
      author_email='jason@canadapop.com',
      url='http://plone.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['dexterity'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'rwproperty',
          'ZODB3',
          'zope.interface',
          'zope.component',
          'zope.schema',
          'zope.annotation',
          'plone.app.intid',
          'Zope2',
          'plone.dexterity',
          'plone.app.drafts'
      ],
      #extras_require={
      #  'tests': ['collective.testcaselayer', 'Products.PloneTestCase'],
      #},
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
