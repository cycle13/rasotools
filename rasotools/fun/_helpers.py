# -*- coding: utf-8 -*-

__all__ = ['find_files', 'now', 'message', 'dict2str', 'print_fixed', 'check_kw', 'update_kw', 'suche123', 'dict_add',
           'dict_in_dict']


def now():
    """ Datetime string

    Returns:
        str : datetime now
    """
    import datetime
    return datetime.datetime.now().isoformat()


def find_files(directory, pattern, recursive=True):
    """ find files

    Args:
        directory (str): directory path
        pattern (str):  regex string: '*.nc'
        recursive (bool): recursive search?

    Returns:
        list: of files
    """
    import os
    import fnmatch
    matches = []
    if recursive:
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename))
    else:
        matches.extend(fnmatch.filter([os.path.join(directory, ifile) for ifile in os.listdir(directory)], pattern))
    return matches


def message(*args, mname=None, verbose=0, level=0, logfile=None, **kwargs):
    if logfile is not None:
        # with open(kwargs['filename'], 'a' if not kwargs.get('force', False) else 'w') as f:
        with open(logfile, 'a') as f:
            f.write(_print_string(*args, **kwargs) + "\n")

    elif verbose > level:
        text = _print_string(*args, **kwargs)
        if mname is not None:
            text = "[%s] " % mname + text

        print(text)
    else:
        pass


def _print_string(*args, adddate=False, **kwargs):
    if adddate:
        return "[" + now() + "] " + " ".join([str(i) for i in args])
    else:
        return " ".join([str(i) for i in args])


def dict2str(tmp, sep=', '):
    return sep.join("{!s}={!r}".format(k, v) for (k, v) in tmp.items())


def print_fixed(liste, sep, width, offset=0):
    offset = " " * offset
    out = offset + liste[0]
    n = len(out)
    for i in liste[1:]:
        if (n + len(i) + 1) > width:
            out += sep + "\n" + offset + i
            n = len(offset + i)
        else:
            out += sep + " " + i
            n += len(i) + 2

    return out


def check_kw(name, value=None, **kwargs):
    if value is None:
        return name in kwargs.keys()
    return kwargs.get(name, None) == value


def update_kw(name, value, **kwargs):
    kwargs.update({name: value})
    return kwargs


def suche123(eins, zwei, drei, test=None):
    if eins is not test:
        return eins
    elif zwei is not test:
        return zwei
    else:
        return drei


def dict_add(d1, d2):
    d2 = d2.copy()
    for i, j in d1.items():
        if i in d2.keys():
            if ',' in j:
                j = j.split(',')
            else:
                j = [j]

            if ',' in d2[i]:
                k = d2[i].split(',')
            else:
                k = [d2[i]]

            for l in k:
                if l not in j:
                    j.append(l)

            d1[i] = ",".join(j)
            d2.pop(i)
    d1.update(d2)
    return d1


def list_in_list(jlist, ilist):
    """ compare lists and use wildcards

    Args:
        jlist (list): list of search patterns
        ilist (list): list of available choices

    Returns:
        list : common elements
    """
    out = []
    for ivar in jlist:
        if '*' in ivar:
            new = [jvar for jvar in ilist if ivar.replace('*', '') in jvar]
            out.extend(new)
        elif ivar in ilist:
            out.append(ivar)
        else:
            pass
    return out


def dict_in_dict(a, b, method='difference'):
    if method == 'difference':
        return {k: v for k, v in set(a.items()) - set(b.items())}
    elif method == 'union':
        return {k: v for k, v in set(a.items()).union(set(b.items()))}
    elif method == 'intersection':
        return {k: v for k, v in set(a.items()).intersection(set(b.items()))}
    else:
        return {}
