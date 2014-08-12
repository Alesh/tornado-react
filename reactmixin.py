import json
import uuid
import execjs
import os.path
import logging
import tornado.web

class ReactMixin(object):
    """ Mixin for tornado.web.Application class allow using React.js features. """
    _components = dict()
    _requires = ['react']
    _PRE_RENDERING = True

    def __init__(self):
        if not isinstance(self, tornado.web.Application):
            raise TypeError("This mixin must be used with class of 'tornado.web.Application'.")
        if 'static_path' not in self.settings:
            raise AttributeError("Please define 'static_path' in application settings.")
        self.ui_modules['JSX'] = JSXModule
        self._bundle_file = os.path.join(self.settings['static_path'], self.settings.get('bundle_file', 'bundle.js'))
        with open(self._bundle_file) as file:
            script = file.read()
        with open(os.path.join(os.path.dirname(__file__), 'render.js')) as file:
            self._ctx = execjs.compile(script+file.read());
        self._make_bundle()

    @classmethod
    def _register(cls, filename, name):
        if name in cls._components:
            if cls._components[name]!=filename:
                logging.warning("Component '%s' already has registred for '%s',"
                    " but will be overwrited for '%s'.", name, cls._components[name], filename)
        cls._components[name] = filename

    def _make_bundle(self):
        with open(os.path.join(os.path.dirname(__file__), 'build.js')) as file:
            build_script = file.read()
        file_list = list(self._components.items())
        debug = self.settings.get('debug', False)
        ctx = execjs.compile(build_script)
        try:
            ctx.call('make_bundle', self._bundle_file, self._requires, file_list, debug)
        except execjs.RuntimeError as exc:
            raise RuntimeError('execjs.RuntimeError: {0}'.format(exc.args[0].decode('utf8')))
        logging.info("Rebuilded: '{0}'.".format(self._bundle_file)) 


class JSXModule(tornado.web.UIModule):
    """ Tornado UI module for placing JSX component on page template. """

    def render(self, component, tag="div", id=None, cssClass=None, **props):
        """ Renders JSX components in initial state. """
        rendered_code = ""
        element_id = id or uuid.uuid1()
        props = self._conv_props(props);
        css_class = component.replace('.', '-') + (' '+cssClass if cssClass is not None else '')
        if self.handler.application._PRE_RENDERING:
            try:
                rendered_code = self.handler.application._ctx.call('render_jsx', component, props)
            except execjs.RuntimeError as exc:
                raise RuntimeError('execjs.RuntimeError: {0}'.format(exc.args[0].decode('utf8')))
        startup_code = ('<script>'
                        'require("react").renderComponent(require("{0}")({1}), document.getElementById("{2}"));'
                        '</script>').format(component, props, element_id)
        return '<{3} id="{0}" class="{1}">{2}</{3}>'.format(element_id, css_class, rendered_code, tag) + startup_code
    
    def _conv_props(self, props):
        return json.dumps(props)


def component(filename, name=None):
    """ Defines JSX component and prepares it to using."""
    if os.path.exists(filename):
        ReactMixin._register(os.path.abspath(filename), 
            name or os.path.splitext(os.path.basename(filename))[0])
