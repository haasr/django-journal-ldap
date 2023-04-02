import ldap
import re

from django_auth_ldap.backend import LDAPBackend, _LDAPUser
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType

class GroupLDAPBackend(LDAPBackend):
  default_settings = {
    # All those settings are overwriting base class values
    "SERVER_URI": "ldap://ldappi.local",
    "CACHE_TIMEOUT": 240,

    "GROUP_REGEX": re.compile(r"\^*django$"),
    "GROUP_SEARCH": LDAPSearch(
        "OU=groups, DC=toothyboi, DC=com",
        ldap.SCOPE_SUBTREE,
        "(cn=*django)",
    ),
    "GROUP_TYPE": PosixGroupType,

    # Those settings should probably be overwritten by the settings.py
    "BIND_DN": "",
    "BIND_PASSWORD": "",
    "USER_SEARCH": LDAPSearch(
      "OU=people, DC=toothyboi, DC=com",
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

    ldap_groups = ldap_user.group_names
    ldap_groups = {x for x in ldap_groups if self.settings.GROUP_REGEX.match(x)}

    if len(ldap_groups) == 0:
      return None
    return user


  def create_groups_and_assign_user_to_it(self, user, ldap_groups):
    for group_name in ldap_groups:
      django_group, was_created = Group.objects.get_or_create(name=group_name)
      django_group.user_set.add(user)

