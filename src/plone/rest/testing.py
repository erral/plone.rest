# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.testing import z2

from zope.configuration import xmlconfig


class PloneRestLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.rest
        xmlconfig.file(
            'configure.zcml',
            plone.rest,
            context=configurationContext
        )
        xmlconfig.file(
            'testing.zcml',
            plone.rest,
            context=configurationContext
        )


PLONE_REST_FIXTURE = PloneRestLayer()
PLONE_REST_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_REST_FIXTURE,),
    name="PloneRestLayer:Integration"
)
PLONE_REST_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_REST_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PloneRestLayer:Functional"
)
