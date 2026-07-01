# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from importlib.metadata import entry_points

from blockdiag.utils.logging import warning,info,error

drawers = {}

def init_imagedrawers(debug=False):
    for drawer in entry_points().select(group = 'blockdiag_imagedrawers'):
        if debug:
            info(f"initialize drawer {drawer}")
        try:
            drawer_module = drawer.load()
            if hasattr(drawer_module, 'setup'):
                drawer_module.setup(drawer_module)
            if debug:
                info(f"initialized drawer {drawer}" )
        except Exception as exc:
            print(exc)
            if debug:
                warning(f'Failed to load {drawer.module!s} {exc}')

def install_imagedrawer(ext, drawer):
    drawers[ ext ] = drawer
    # info(f"installing drawer {drawer!r}  for {ext} ")

def create(_format, filename, **kwargs):
    
    if len(drawers) == 0:
        init_imagedrawers(debug=kwargs.get('debug'))

    _format = _format.lower()
    
    if _format in drawers:
        drawer = drawers[_format](filename, **kwargs)
        # info(f"loaded drawer {drawer!r} for format {_format}")
    else:
        msg = 'failed to load %s image driver' % _format
        raise RuntimeError(msg)

    if 'linejump' in kwargs.get('filters', []):
        from blockdiag.imagedraw.filters.linejump import LineJumpDrawFilter
        jumpsize = kwargs.get('jumpsize', 0)
        drawer = LineJumpDrawFilter(drawer, jumpsize)

    return drawer
