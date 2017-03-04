# -*- coding: utf-8 -*-
import pkg_resources
import os

from sphinxcontrib.httpexample.directives import HTTPExample

CSS_FILE = 'sphinxcontrib-httpexample.css'
JS_FILE = 'sphinxcontrib-httpexample.js'


def copy_assets(app, exception):
    if app.builder.name != 'html' or exception:
        return
    filename = os.path.join(app.builder.outdir, '_static', CSS_FILE)
    with open(filename, 'w') as fp:
        fp.write("""\
.http-example.container .code-block-caption {
  display: inline-block;
  cursor: pointer;
  padding: 0.5em 1em;
}
.http-example.container .code-block-caption.selected {
  font-weight: bold;
  background-color: #fff;
  border: 1px solid #e1e4e5;
  border-bottom: 1px solid white;
}
.http-example.container div[class^='highlight'] {
  margin-top: -1px;
}
.http-example.container .code-block-caption .headerlink {
  display: none;
}
.http-example.container .container + .container pre {
  white-space: normal;
}
""")
    filename = os.path.join(app.builder.outdir, '_static', JS_FILE)
    with open(filename, 'w') as fp:
        fp.write("""\
(function() {
var jQuery = window.jQuery || function() {};

jQuery(function($) {
  $('.http-example.container').each(function() {
    var $container = $(this),
        $blocks = $(this).children(),
        $captions = $(this).find('.code-block-caption');
    $captions.each(function() {
      var $block = $(this).parent();
      $(this).on('click', function() {
        $captions.removeClass('selected');
        $(this).addClass('selected');
        $blocks.hide();
        $block.show();
      });
      $container.append($(this));
    });
    $container.append($blocks);
    $captions.first().click();
  });
});

})();
""")


def setup(app):
    app.connect('build-finished', copy_assets)
    app.add_directive_to_domain('http', 'example', HTTPExample)
    app.add_javascript(JS_FILE)
    app.add_stylesheet(CSS_FILE)
    dist = pkg_resources.get_distribution('sphinxcontrib-httpexample')
    return {'version': dist.version}
