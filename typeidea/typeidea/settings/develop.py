from .base import *   # NOQA

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
    # 'pympler',
    # 'silk',

]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'silk.middleware.SilkyMiddleware',
]


INTERNAL_IPS = ['127.0.0.1']


#
# DEBUG_TOOLBAR_PANELS = [
#     'djdt_flamegraph.FlamegraphPanel',
# ]


# DEBUG_TOOLBAR_PANELS = [
#     # 'djdt_flamegraph.FlamegraphPanel', # 火焰图没效果
#
#     # 'pympler.panels.MemoryPanel',
# ]



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}





























