# coding=utf8
import os
import re
from pyutil.program.exception import ConfException


class ConfLoader(object):
    def __init__(self, filename):
        self.filename = filename

    def parse(self, ):
        kv = dict()
        if not os.path.exists(self.filename):
            return kv
        with open(self.filename, 'r', encoding='UTF-8') as f:
            base_dir = os.path.dirname(os.path.abspath(self.filename))
            for lineno, l in enumerate(f):
                if re.match('^\s*#', l):
                    continue

                elements = l.strip().split()
                if not elements:
                    continue
                if len(elements) < 2:
                    errmsg = 'format incorrect: lineno:%s %s' % (lineno, l)
                    raise ConfException(errmsg)
                key, value = self.clean_elem(elements)
                if key == 'include':
                    conf_loader = ConfLoader(
                        os.path.join(base_dir, value)
                        )
                    kv.update(conf_loader.parse())
                else:
                    kv[key] = value
        return kv

    def clean_elem(self, elements):
        key = elements[0]
        value = ' '.join(elements[1:])
        return key.strip(), value.strip()

