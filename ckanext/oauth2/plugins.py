# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from ckan import plugins
from ckan.plugins import toolkit


log = logging.getLogger(__name__)


def _no_permissions(context, msg):
    user = context['user']
    return {'success': False, 'msg': msg.format(user=user)}


# @toolkit.auth_sysadmins_check
# def user_create(context, data_dict):
#     msg = toolkit._('Users cannot be created.')
#     return _no_permissions(context, msg)


# @toolkit.auth_sysadmins_check
# def user_update(context, data_dict):
#     msg = toolkit._('Users cannot be edited.')
#     return _no_permissions(context, msg)


@toolkit.auth_sysadmins_check
def user_reset(context, data_dict):
    msg = toolkit._('Users cannot reset passwords.')
    return _no_permissions(context, msg)


@toolkit.auth_sysadmins_check
def request_reset(context, data_dict):
    msg = toolkit._('Users cannot reset passwords.')
    return _no_permissions(context, msg)


class OAuth2Plugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IAuthenticator, inherit=True)
    plugins.implements(plugins.IAuthFunctions, inherit=True)
    plugins.implements(plugins.IConfigurable)

    def configure(self, config):
        '''Store the OAuth 2 client configuration'''
        log.debug('configure')
        self.logout_url = config['ckan.oauth2.logout_url']
        self.logout_next_name = config['ckan.oauth2.logout_next_name']

    def identify(self):
        log.debug('identify')

    def login(self):
        log.debug('login')
        if not toolkit.c.user:
            # A 401 HTTP Status will cause the login to be triggered
            return toolkit.abort(401, toolkit._('Login required!'))
        redirect_to = toolkit.request.params.get('came_from', '/')
        toolkit.redirect_to(bytes(redirect_to))

    def logout(self):
        log.debug('logout')
        # environ = toolkit.request.environ
        # repoze_userid = environ["repoze.who.identity"]['repoze.who.userid']
        # for plugin in environ['repoze.who.plugins']:
        #     if hasattr(plugin, 'forget'):
        #         plugin.forget(environ, repoze_userid)
        # return toolkit.redirect_to(bytes(self.logout_url), locale='default')

    def get_auth_functions(self):
        # we need to prevent some actions being authorized.
        return {
            # 'user_create': user_create,
            # 'user_update': user_update,
            'user_reset': user_reset,
            'request_reset': request_reset,
        }




