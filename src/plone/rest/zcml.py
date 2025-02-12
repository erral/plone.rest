# -*- coding: utf-8 -*-
from zope.configuration.exceptions import ConfigurationError
from zope.configuration.fields import GlobalObject, GlobalInterface
from zope.interface import Interface
from zope.schema import TextLine, Bool
from zope.publisher.interfaces.browser import IBrowserPublisher
from plone.rest import interfaces
from plone.rest.cors import get_cors_preflight_view

from zope.component.zcml import adapter
from zope.security.zcml import Permission
from zope.security.checker import CheckerPublic


class IService(Interface):
    """
    """

    method = TextLine(
        title=u"The name of the view that should be the default. " +
              u"[get|post|put|delete]",
        description=u"""
        This name refers to view that should be the view used by
        default (if no view name is supplied explicitly).""",
        )

    for_ = GlobalObject(
        title=u"The interface this view is the default for.",
        description=u"""Specifies the interface for which the view is
        registered. All objects implementing this interface can make use of
        this view. If this attribute is not specified, the view is available
        for all objects.""",
        )

    factory = GlobalObject(
        title=u"The factory for this behavior",
        description=u"If this is not given, the behavior is assumed to " +
                    u"provide a marker interface")

    layer = GlobalInterface(
        title=u"A marker interface to be applied by the behavior",
        description=u"If provides is given and factory is not given, then "
                    u"this is optional",
        required=False)

    cors_enabled = Bool(
        title=u"The name of the view that should be the default."
              u"[get|post|put|delete]",
        description=u"""
        This name refers to view that should be the view used by
        default (if no view name is supplied explicitly).""",
        required=False
        )

    cors_origin = TextLine(
        title=u"The name of the view that should be the default." +
              u"[get|post|put|delete]",
        description=u"""
        This name refers to view that should be the view used by
        default (if no view name is supplied explicitly).""",
        required=False
        )

    permission = Permission(
        title=u"Permission",
        description=u"The permission needed to use the view.",
        required=False
        )


def serviceDirective(
        _context,
        method,
        factory,
        for_,
        layer=None,
        cors_enabled=False,
        cors_origin=None,
        permission=CheckerPublic
        ):

    if method.upper() == 'GET':
        marker = interfaces.IGET
    elif method.upper() == 'POST':
        marker = interfaces.IPOST
    elif method.upper() == 'OPTIONS':
        marker = interfaces.IOPTIONS
    elif method.upper() == 'PUT':
        marker = interfaces.IPUT
    elif method.upper() == 'DELETE':
        marker = interfaces.IDELETE
    elif method.upper() == 'PATCH':
        marker = interfaces.IPATCH
    else:
        raise ConfigurationError(
            u"No implementation for %s method" % method
        )

    required = {}

    if permission == 'zope.Public':
        permission = CheckerPublic

    for n in ('browserDefault', '__call__', 'publishTraverse'):
        required[n] = permission

    # defineChecker(factory, Checker(required))

    if cors_enabled:
        # Check if there is already an adapter for options

        # Register
        adapter(
            _context,
            factory=(get_cors_preflight_view),
            provides=IBrowserPublisher,
            for_=(for_, interfaces.IOPTIONS)
        )

    adapter(
        _context,
        factory=(factory,),
        provides=IBrowserPublisher,
        for_=(for_, marker)
    )
