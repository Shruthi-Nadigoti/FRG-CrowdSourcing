from flask import current_app as app

from flask.ext.plugins import Plugin

#from flask.ext.plugins import PluginManager
__plugin__ = "HelloWorld"

#plugin_manager = PluginManager()
#plugin_manager.init_app(app)

class HelloWorld(Plugin):
    def setup(self):
    	#self.load_config()
         print "x"
         self.setup_blueprint()
        #connect_event('before-data-rendered', do_before_data_rendered)
    def setup_blueprint(self):
        """Setup blueprint."""
        from .views import blueprint
        app.register_blueprint(blueprint, url_prefix="/testhello")
