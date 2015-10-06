# vim: set ft=python ts=4 sw=4 sts=4 et :
# -*- coding: utf-8 -*-
#! /usr/bin/env python

__author__ = 'Jason Mehring'

'''
Bind salt modules within formula directories to salt cache directory.

Allow breakpoint to be properly set in debuggers.

mount --bind /srv/formulas/base/topd-formula/_modules/topd.py /var/cache/salt/minion/extmods/modules/topd.py
mount --bind /srv/formulas/base/topd-formula/_utils/pathutils.py /var/cache/salt/minion/extmods/utils/pathutils.py
mount --bind /srv/formulas/base/topd-formula/_utils/toputils.py /var/cache/salt/minion/extmods/utils/toputils.py
mount --bind /srv/formulas/base/topd-formula/_utils/pathinfo.py /var/cache/salt/minion/extmods/utils/pathinfo.py
mount --bind /srv/formulas/base/topd-formula/_utils/fileinfo.py /var/cache/salt/minion/extmods/utils/fileinfo.py
mount --bind /srv/formulas/base/topd-formula/_utils/matcher.py /var/cache/salt/minion/extmods/utils/matcher.py
mount --bind /srv/formulas/base/topd-formula/_utils/adapt.py /var/cache/salt/minion/extmods/utils/adapt.py
mount --bind /srv/formulas/dev/development-tools/_modules/bind.py /var/cache/salt/minion/extmods/modules/bind.py

umount /var/cache/salt/minion/extmods/modules/topd.py
umount /var/cache/salt/minion/extmods/utils/pathutils.py
umount /var/cache/salt/minion/extmods/utils/toputils.py
umount /var/cache/salt/minion/extmods/utils/fileinfo.py
umount /var/cache/salt/minion/extmods/utils/pathinfo.py
umount /var/cache/salt/minion/extmods/utils/matcher.py
umount /var/cache/salt/minion/extmods/modules/bind.py
umount /var/cache/salt/minion/extmods/utils/adapt.py
'''

# Import python libs
import fnmatch
import logging
import os
import shutil
import subprocess

# Import salt libs
import salt.fileclient
import salt.fileserver
import salt.utils

from salt.exceptions import SaltRenderError

# Import custom libs

# XXX: temp location
#    Access other function this way...
#    mod = sys.modules[name]
#    if not hasattr(mod, '__utils__'):
#        setattr(mod, '__utils__', salt.loader.utils(mod.__opts__))

# Set up logging
log = logging.getLogger(__name__)

try:
    __context__['salt.loaded.ext.module.bind'] = True
except NameError:
    __context__ = {}

# Define the module's virtual name
__virtualname__ = 'bind'


def __virtual__():
    '''
    Only load on POSIX-like systems
    '''
    # XXX: Should only be set if mounting is anabled
    # Disable clening up of modules, since they are bound
    __opts__['clean_dynamic_modules'] = False

    # Disable on Windows, a specific file module exists:
    if salt.utils.is_windows():
        return False
    return True


#XXX: TEMP: From topd
##def get_opts(opts=None):
##    if not opts:
##        opts = __opts__
##    return opts

#XXX: TEMP: From topd
##def get_fileclient(opts=None):
##    if 'fileclient' in __context__:
##        return __context__['fileclient']
##
##    opts = get_opts(opts)
##    fileclient = salt.fileclient.get_file_client(opts, is_pillar(opts))
##    __context__['fileclient'] = fileclient
##    return fileclient


def coerce_to_list(value):
    '''Converts value to a list.
    '''
    if not value:
        value = []
    elif isinstance(value, str):
        value = [value,]
    elif isinstance(value, tuple):
        value = list(value)
    return value


def XXXparse_files(paths, saltenv):
    '''
    Convert paths into salt relative paths and add '_' prefix to module
    directories.
    '''
    modules = [
        'beacons',
        'modules',
        'states',
        'grains',
        'renderers',
        'returners',
        'outputters',
        'utils',
    ]
    paths = coerce_to_list(paths)
    for index, path in enumerate(paths):
        if path in modules:
            paths[index] = u'_' + path

##    # real path to salt path...
##    # take real path
##    # IE: u'/srv/formulas/base/qubes-base/_modules/module_utils.py'
##
##    # file_roots -- (USE a RE search here; combine file roots ?? -- cant; its reversed??)
##    # IE: ['/srv/formulas/base/qubes_base']
##    # add a '/'
##    # IE: ['/srv/formulas/base/qubes_base']
##    path = u'/srv/formulas/base/qubes-base/_modules/module_utils.py'
##    file_roots = []
##    striped_path = None
##    for env in saltenv:
##        if env in __opts__['file_roots']:
##            file_roots.extend(__opts__['file_roots'][env])
##    # add a '/'
##
##    import itertools
##    from itertools import chain, imap
##    from itertools import ifilter
##
##    # Combine all file_roots; then
##    # Reverse to to be able to find longest match first
##    file_roots = sorted(
##        chain.from_iterable(__opts__['file_roots'].values()),
##        reverse=True
##    )
##
##    # XXX: Add another match so we can find longest match
##    file_roots.insert(0, '/srv/formulas/base')
##    file_roots = sorted(file_roots, reverse=True)
##
##    # Compile file_roots pattern
##    #matcher = re.compile(wildcard_to_regex([root+'/*' for root in file_roots]))
##    matcher = re.compile(
##        # This will return a group list and needs to be processed further
##        #'|'.join(['({0}/*)'.format(re.escape(root)) for root in file_roots])
##
##        # This will return the root
##        '|'.join(['(?:{0}/*)'.format(re.escape(root)) for root in file_roots])
##    )
##
##    try:
##        root = matcher.match(path).group()
##    except AttributeError:
##        #XXX: Raise a salt error
##        pass
##
##    paths = __utils__['topd.paths'](__opts__)
##    result = paths.find(path)
##
##    # XXX: If no match... will bomb cause of []... can use ''join, but want to raise an error anyway
##    #      so just capture error and raise
##    # Find the file_root that path belongs to
##    # Raise an error if no match exists
##    #root = [file_roots[i] for i, y in enumerate(matcher.findall(path).groups()) if y][0]
##    matched = matcher.findall(path)
##    try:
##        root = [file_roots[index] for index, root in enumerate(matched) if root][0]
##    except IndexError:
##        #XXX: Raise a salt error
##        pass
##
##    root = ''.join(itertools.compress(file_roots, matcher.match(path).groups()))
##
##    # Retuns tuple
##    list(itertools.izip(matcher.match(path).groups(), file_roots))
##
##    # XXX: TODO: Maybe have a map of sorts to allow reverse lookup
##    # Determine saltenv that path belongs to
##
##    # Does not return any results
##    #"".join([_ for _,_ in itertools.takewhile(lambda cr: cr[0]==cr[1], itertools.izip(s1,s2))])
##
##    # Only sends s1[0], so only get first result
##    s1 = file_roots
##    s2 = path
##    list(itertools.dropwhile(lambda cr: not os.path.commonprefix(cr), itertools.izip(s1, s2)))
##
##    root1 = wildcard_to_regex(file_roots)
##    root2 = wildcard_to_regex([root+'/*' for root in file_roots])
##    match = re.match(root2, path)
##    root3 = [root+'/*' for root in file_roots]
##    map(lambda f1, f2: os.path.commonprefix([f1, f2]), file_roots, path)
##    print

    # Based on fileclient.list_states
    for root in file_roots:
        if path.startswith(root + os.sep):
            #found = path.split(root + os.sep)[1]
            stripped_root = os.path.relpath(path, root).replace('/', '.')
            if salt.utils.is_windows():
                stripped_path = stripped_path.replace('\\', '/')
            break

    return paths

##import re
##def fnmatch_encode(text):
##    # replace the left square bracket with [[]
##    text = re.sub(r'\[', '[[]', text)
##
##    # replace the right square bracket with []] but be careful not to replace
##    # the right square brackets in the left square bracket's 'escape' sequence.
##    return re.sub(r'(?<!\[)\]', '[]]', text)
##
##def fnmatch_translate(text):
##    return  r'{0}'.format(fnmatch.translate(fnmatch_encode(text)))
##    #return  r'{0}'.format(re.escape(text))
##
##def wildcard_to_regex(wildcards):
##    data = []
##    for wildcard in wildcards:
##        #data.append(fnmatch_translate(wildcard))
##        data.append( '(' + fnmatch_translate(wildcard) + ')')
##    if data:
##        data = r'|'.join(data)
##    return data


def module_dirs(paths, saltenv):
    '''
    Convert paths into salt relative paths and add '_' prefix to module
    directories.
    '''
    modules = [
        'beacons',
        'modules',
        'states',
        'grains',
        'renderers',
        'returners',
        'outputters',
        'utils',
    ]
    paths = coerce_to_list(paths)
    for index, path in enumerate(paths):
        if path in modules:
            paths[index] = u'_' + path
    return paths


def find_files(paths, saltenv=None):
    saltenvs = coerce_to_list(saltenv) if saltenv else client.envs()
    paths = module_dirs(paths, saltenvs)

    opts = __opts__
    client = salt.fileclient.get_file_client(opts)
    fileserver = salt.fileserver.Fileserver(opts)

##    # Salt client.file_list() loops though all the file roots, then
##    # applies a relpath to return files
##    root = '/srv/salt/test'
##    fname = 'test-top.top'
##    path = '/srv/salt'
##    # IE: rel_fn = 'test/test-top.top'
##    rel_fn = os.path.relpath(
##                os.path.join(root, fname),
##                path
##            )

    # TODO: Implement source

    # Locate all '.py' module files
    modules = []
    #for env in saltenv:
    #    matches = fnmatch.filter(client.list_env(saltenv=env), '*.py')
    #    matches = [match for match in matches if match.split('/')[0] in paths]
    #    for relpath in matches:
    #        path_local = fileserver.find_file(relpath, env)['path']
    #        path_cached = client._extrn_path(relpath, env)
    #        if path_local and path_cached:
    #            modules.append((path_local, path_cached))
    #return modules
    pathutils = __utils__['pathutils.pathutils'](__opts__)

    for saltenv in saltenvs:
        #files = fnmatch.filter(client.list_env(saltenv=saltenv), '*.py')
        files = pathutils.files(saltenv, '*.py')
        files = [match for match in files if match.split('/')[0] in paths]
        for relpath in files:
            local_path = pathutils.loacl_path(relpath, saltenv)
            cached_path = pathutils.cache_path(relpath, saltenv)
            if os.path.exists(local_path) and os.path.exists(cached_path):
                modules.append((local_path, cached_path))
            else:
                raise SaltRenderError('Can not determine paths for {0} and {1}'.format(local_path,cached_path))
    return modules


def _bind(paths, saltenv=None):
    paths = find_files(paths, saltenv)


# Allow ether prefix or paths
# Maybe prefix or file can be; just check
def mount(*paths, **kwargs):
    '''
    Bind mount local salt path(s) or contents of module directories to
    cached salt file location.

    [FILE...]
        Source paths of files to bind; and/or
        Module directories to bind:
            beacons
            modules
            states
            grains
            renderers
            returners
            outputters
            utils
        (Default: all files within all module directories)

    saltenv
        Salt environments to choose. (Default: all)

    CLI Example:

    .. code-block:: bash

        qubesctl bind.mount
        qubesctl bind.mount /srv/salt/dir/file
        qubesctl bind.mount modules utils saltenv=base
        qubesctl bind.mount modules utils saltenv=['base, user']
        qubesctl bind.mount saltenv=['base, user']
    '''
    saltenv = kwargs.get('saltenv', None)
    #return _bind(paths, saltenv=saltenv)
    #return _test_paths(paths, saltenv=saltenv)

    #return __salt__['topd.report']()
    #return __salt__['topd.enabled']()
    return __salt__['topd.status']()
    #return __salt__['topd.is_enabled']('topd.base|salt.directories',
    #                                   'topd.dev|bind')

#def all(saltenv=None):
#    return _bind(MODULES, saltenv=saltenv)

#def file(source, saltenv=None):
#    return _bind(source, saltenv=saltenv)

#def beacons(saltenv=None):
#    return _bind('_beacons', saltenv=saltenv)

#def modules(saltenv=None):
#    return _bind('_modules', saltenv=saltenv)

#def states(saltenv=None):
#    return _bind('_states', saltenv=saltenv)

#def grains(saltenv=None):
#    return _bind('_grains', saltenv=saltenv)

#def renderers(saltenv=None):
#    return _bind('_renderers', saltenv=saltenv)

#def returners(saltenv=None):
#    return _bind('_returners', saltenv=saltenv)

#def outputters(saltenv=None):
#    return _bind('_outputters', saltenv=saltenv)

#def utils(saltenv=None):
#    return _bind('_utils', saltenv=saltenv)

def XXXall():
    #ret = []
    cache = []

    for env in saltenv:
        log.info('Syncing {0} for environment {1!r}'.format(form, env))
        log.info('Loading cache from {0}, for {1})'.format(source, env))

        # Grab only the desired files (.py, .pyx, .so)
        cache.extend(
            __salt__['cp.cache_dir'](
                source, env, include_pat=r'E@\.(pyx?|so)$'
            )
        )
        local_cache_base_dir = os.path.join(
                __opts__['cachedir'],
                'files',
                env
                )
        log.debug('Local cache base dir: {0!r}'.format(local_cache_base_dir))

        local_cache_dir = os.path.join(local_cache_base_dir, '_{0}'.format(form))
        log.debug('Local cache dir: {0!r}'.format(local_cache_dir))

        client = salt.fileclient.get_file_client(__opts__)
        fileserver = salt.fileserver.Fileserver(__opts__)

        for fn_ in cache:
            relpath = os.path.relpath(fn_, local_cache_dir)
            relname = os.path.splitext(relpath)[0].replace(os.sep, '.')

            saltpath = os.path.relpath(fn_, local_cache_base_dir)
            filenamed = fileserver.find_file(saltpath, env)

            remote.add(relpath)
            dest = os.path.join(mod_dir, relpath)

            #if not os.path.isfile(dest):
            #    dest_dir = os.path.dirname(dest)
            #    if not os.path.isdir(dest_dir):
            #        os.makedirs(dest_dir)
            #    shutil.copyfile(fn_, dest)
            #    ret.append('{0}.{1}'.format(form, relname))

            #
            # XXX: Use salt's mount module
            #

            # Test to see if already mounted (bound)
            #cmd = ['findmnt', dest]
            #proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=subprocess.STDOUT)
            #proc.wait()

            #if proc.returncode:
            #    cmd = ['mount', '--bind', filenamed['path'], dest]
            #    proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=subprocess.STDOUT)
            #    proc.wait()
            #elif umount:
            #    cmd = ['umount', dest]
            #    proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=subprocess.STDOUT)
            #    proc.wait()


##BIND = None
##
##import os
##import sys
##import shutil
##import subprocess
##import logging
##
##if BIND is not None:
##    import salt.config
##    import salt.fileclient
##    import salt.fileserver
##    import salt.loader
##    import salt.modules.saltutil
##    import salt.pillar
##
##    try:
##        from subprocess import DEVNULL # py3k
##    except ImportError:
##        import os
##        DEVNULL = open(os.devnull, 'wb')
##
##    from salt.modules.saltutil import (
##        _get_top_file_envs, _listdir_recursively, _list_emptydirs
##    )
##    from salt.ext.six import string_types
##
##    # Enable logging
##    log = logging.getLogger(__name__)
##
##    BASE_DIR = os.getcwd()
##
##    # Set salt pillar, grains and opts settings so they can be applied to modules
##    __opts__ = salt.config.minion_config('/etc/salt/minion')
##    __opts__['grains'] = salt.loader.grains(__opts__)
##    pillar = salt.pillar.get_pillar(
##        __opts__,
##        __opts__['grains'],
##        __opts__['id'],
##        __opts__['environment'],
##    )
##    __opts__['pillar'] = pillar.compile_pillar()
##    __salt__ = salt.loader.minion_mods(__opts__)
##    __grains__ = __opts__['grains']
##    __pillar__ = __opts__['pillar']
##    __context__ = {}
##
##    salt.modules.saltutil.__opts__ =  __opts__
##    salt.modules.saltutil.__grains__ =  __grains__
##    salt.modules.saltutil.__pillar__ =  __pillar__
##    salt.modules.saltutil.__salt__ =  __salt__
##    salt.modules.saltutil.__context__ =  __context__
##
##from salt.scripts import salt_call
##
##def _bind(module_name, saltenv=None, umount=False):
##    '''
##    Bind the files in salt extmods directory within the given environment
##    '''
##    if saltenv is None:
##        saltenv = _get_top_file_envs()
##    if isinstance(saltenv, string_types):
##        saltenv = saltenv.split(',')
##    ret = []
##    remote = set()
##
##    # IE: 'salt://_modules'
##    source = os.path.join('salt://_{0}'.format(module_name))
##
##    # IE: '/var/cache/salt/minion/extmods/modules'
##    mod_dir = os.path.join(__opts__['extension_modules'], '{0}'.format(module_name))
##
##    #if not os.path.isdir(mod_dir):
##    #    log.info('Creating module dir {0!r}'.format(mod_dir))
##    #    try:
##    #        os.makedirs(mod_dir)
##    #    except (IOError, OSError):
##    #        msg = 'Cannot create cache module directory {0}. Check permissions.'
##    #        log.error(msg.format(mod_dir))
##
##    for sub_env in saltenv:
##        log.info('Syncing {0} for environment {1!r}'.format(module_name, sub_env))
##        cache = []
##        log.info('Loading cache from {0}, for {1})'.format(source, sub_env))
##
##        # IE: [u'/var/cache/salt/minion/files/base/_modules/qubes.py',]
##        # Grab only the desired files (.py, .pyx, .so)
##        cache.extend(
##            __salt__['cp.cache_dir'](
##                source, sub_env, include_pat=r'E@\.(pyx?|so)$'
##            )
##        )
##
##        # IE: ['/var/cache/salt/minion', 'files', 'base']
##        #      '/var/cache/salt/minion/files/base'
##        local_cache_base_dir = os.path.join(
##                __opts__['cachedir'],
##                'files',
##                sub_env
##                )
##        log.debug('Local cache base dir: {0!r}'.format(local_cache_base_dir))
##
##        # IE: '/var/cache/salt/minion/files/base/_modules'
##        local_cache_dir = os.path.join(local_cache_base_dir, '_{0}'.format(module_name))
##        log.debug('Local cache dir: {0!r}'.format(local_cache_dir))
##
##        client = salt.fileclient.get_file_client(__opts__)
##        fileserver = salt.fileserver.Fileserver(__opts__)
##
##        for fn_ in cache:
##            # IE: 'qubes.py'
##            relpath = os.path.relpath(fn_, local_cache_dir)
##
##            # IE: 'qubes'
##            relname = os.path.splitext(relpath)[0].replace(os.sep, '.')
##
##            # IE: '_modules/qubes.py'
##            saltpath = os.path.relpath(fn_, local_cache_base_dir)
##
##            # IE: {'back': 'roots',
##            #      'path': '/srv/formulas/base/qubes-base/_modules/qubes.py',
##            #      'rel': '_modules/qubes.py'}
##            filenamed = fileserver.find_file(saltpath, sub_env)
##
##            # 'qubes.py'
##            remote.add(relpath)
##
##            # IE: '/var/cache/salt/minion/extmods/modules/qubes.py'
##            dest = os.path.join(mod_dir, relpath)
##
##            if not os.path.isfile(dest):
##                dest_dir = os.path.dirname(dest)
##                if not os.path.isdir(dest_dir):
##                    os.makedirs(dest_dir)
##                shutil.copyfile(fn_, dest)
##                ret.append('{0}.{1}'.format(module_name, relname))
##
##            # Test to see if already mounted (bound)
##            cmd = ['findmnt', dest]
##            proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=subprocess.STDOUT)
##            proc.wait()
##
##            if proc.returncode:
##                cmd = ['mount', '--bind', filenamed['path'], dest]
##                proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=subprocess.STDOUT)
##                proc.wait()
##            elif umount:
##                cmd = ['umount', dest]
##                proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=subprocess.STDOUT)
##                proc.wait()
##
##    touched = bool(ret)
##    if __opts__.get('clean_dynamic_modules', True):
##        current = set(_listdir_recursively(mod_dir))
##        for fn_ in current - remote:
##            full = os.path.join(mod_dir, fn_)
##
##            if os.path.ismount(full):
##                proc = subprocess.Popen(['umount', full])
##                proc.wait()
##
##            if os.path.isfile(full):
##                touched = True
##                try:
##                    os.remove(full)
##                except OSError: pass
##
##        # Cleanup empty dirs
##        while True:
##            emptydirs = _list_emptydirs(mod_dir)
##            if not emptydirs:
##                break
##            for emptydir in emptydirs:
##                touched = True
##                shutil.rmtree(emptydir, ignore_errors=True)
##
##    # Dest mod_dir is touched? trigger reload if requested
##    if touched:
##        mod_file = os.path.join(__opts__['cachedir'], 'module_refresh')
##        with salt.utils.fopen(mod_file, 'a+') as ofile:
##            ofile.write('')
##    return ret

##def bind_dirs(umount):
##    _bind('beacons', umount=umount)
##    _bind('modules', umount=umount)
##    _bind('states', umount=umount)
##    _bind('grains', umount=umount)
##    _bind('renderers', umount=umount)
##    _bind('returners', umount=umount)
##    _bind('outputters', umount=umount)
##    _bind('utils', umount=umount)

##if __name__ == '__main__':
##    argv = sys.argv
##
##    def join_path(basepath, paths):
##        return [os.path.join(basepath, path) for path in paths]
##
##    if BIND or BIND is False:
##        umount = not BIND
##        path = BASE_DIR.split(os.sep)
##        srv_dir = '/srv'
##        if srv_dir.lstrip(os.sep) in path:
##            index = BASE_DIR.index(srv_dir)
##            basepath = os.sep.join(path[:6+1])
##            cur_dirs = join_path(basepath, os.listdir(basepath))
##            srv_dirs = join_path(srv_dir, os.listdir(srv_dir))
##
##            for path in cur_dirs:
##                if path not in srv_dirs:
##                    basename = os.path.basename(path)
##                    if basename in os.listdir(srv_dir):
##                        dest = os.path.join(srv_dir, basename)
##
##                        # Test to see if already mounted (bound)
##                        cmd = ['findmnt', dest]
##                        proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=subprocess.STDOUT)
##                        proc.wait()
##
##                        if proc.returncode:
##                            print 'mounting:', path, dest
##                            cmd = ['mount', '--bind', path, dest]
##                            proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=subprocess.STDOUT)
##                            proc.wait()
##                        elif umount:
##                            cmd = ['umount', dest]
##                            proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=subprocess.STDOUT)
##                            proc.wait()

##        # Bind custom modules
##        bind_dirs(umount)
##
##        if not BIND:
##            sys.exit()
##
##    salt_call()
