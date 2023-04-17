import ldap
import re
import os

from django_auth_ldap.backend import LDAPBackend, _LDAPUser
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect

'''
from ldap3 import Server, Connection, ALL
from dotenv import load_dotenv

load_dotenv()

server = Server("ldap://ldappi.local", get_info=ALL)
conn = Connection(server, "cn=admin,dc=tak,dc=etsu,dc=edu", os.getenv('LDAP_BIND_PASS'))

conn.search('cn=washingtoncounty')
'''

domain_logins = {
  "domain-washingtoncounty": "http://ldapsubdir0.local:8000/blogApp/user_login/"
}

class GroupLDAPBackend(LDAPBackend):
  default_settings = {
    # All those settings are overwriting base class values
    "SERVER_URI": "ldap://ldappi.local",
    "CACHE_TIMEOUT": 240,

    "GROUP_REGEX": re.compile(r"\^*django.*"),
    "GROUP_SEARCH": LDAPSearch(
        "OU=groups, DC=tak, DC=etsu, DC=edu",
        ldap.SCOPE_SUBTREE,
        "(cn=*django)",
    ),
    "GROUP_TYPE": PosixGroupType,

    # Those settings should probably be overwritten by the settings.py
    "BIND_DN": "",
    "BIND_PASSWORD": "",
    "USER_SEARCH": LDAPSearch(
      "OU=people, DC=tak, DC=etsu, DC=edu",
      # If you know, that all your users logging in are on that
      # exact ou depth specified above, you can get better performance
      # by using ldap.SCOPE_BASE or for that depth and its direct
      # children ldap.SCOPE_ONELEVEL, see python-ldap documentation for
      # more.
      ldap.SCOPE_SUBTREE,
      "(uid=%(user)s)"
    ),
  }


  def authenticate_ldap_user(self, ldap_user: _LDAPUser, password: str):
    # This is the default implemented authentication
    user = ldap_user.authenticate(password)

    # If the authentication was denied, we have to return None
    if not user:
      return None

    user.set_password(password) # Keep local password synced with LDAP's password
    user.save()

    ldap_groups = list(ldap_user.group_names)
    ldap_groups = [x for x in ldap_groups if not self.settings.GROUP_REGEX.match(x)]
    domain_groups = [x for x in ldap_groups if x.startswith("domain-")]

    if len(ldap_groups) == 0:
      return None

    self.create_groups_and_assign_user(user, ldap_groups)
    
    if len(domain_groups) == 0:
      return user
    else: # If user member of a local domain, redirect to it
      return HttpResponseRedirect(domain_logins[domain_groups[0]]) # Obviously using the first index of several wouldn't be good but for now, just use first one


  def create_groups_and_assign_user(self, user, ldap_groups):
    for group_name in ldap_groups:
      django_group, was_created = Group.objects.get_or_create(name=group_name)
      django_group.user_set.add(user)



