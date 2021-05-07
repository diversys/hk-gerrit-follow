import os
import os.path
import subprocess
import tempfile

import paths
import subprocess_wrapper


__all__ = ('jam',)


def jam(wd, target, options=None, quick=False, jam_cmd=None, output=None):
    if jam_cmd is None:
        jam_cmd = paths.jam()
        if jam_cmd is None:
            jam_cmd = 'jam'
    args = [jam_cmd]

    if quick:
        args.append('-q')
    else:
        try:
            i = min(int(len(os.sched_getaffinity(0))/2), 4)
            if i > 1:
                args.append('-j' + str(i))
        except:
            pass

    if options:
        args.extend(options)

    if isinstance(target, str):
        args.append(target)
        basefile = target
    else:
        args.extend(target)
        basefile = target[0]

    if not output:
        output = ''.join([c for c in basefile if c.isalnum()])
        if output:
            output = os.path.join(wd, output)
    if output:
        out = open(output + '.out', mode='wb')
        err = open(output + '.err', mode='wb')
    else:
        out, _ = tempfile.mkstemp(suffix='.out', prefix='jam', dir=wd)
        err, _ = tempfile.mkstemp(suffix='.err', prefix='jam', dir=wd)

    return subprocess.run(args, stdout=out, stderr=err, cwd=wd)

