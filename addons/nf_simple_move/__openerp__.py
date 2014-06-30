# -*- coding: utf-8 -*-
{
        "name" : "nf_simple_move",
        "version" : "0.0.1",
        "author" : "NF informatique Sàrl",
        "website" : "http://www.nfinformatique.ch",
        "category" : "Custom",
        "description": """  Simple move form.""",
        "license":"AGPL-3",
        "depends" : ['base', 'account','web'],
        "data" : [
                  "simple_move_view.xml",
                  "wizard/simple_move.xml",
                  ],
        "demo" : [ ],
        'css': [
                "static/css/style.css",
                ],
        'js': [
#               "static/js/account_move_line_quickadd.extend.js",
               "static/js/account_move_line_quickadd.extend.b.js",
               ],
        'qweb' : [
            "static/xml/account_move_line_quickadd.extend.xml",
        ],
        "installable": True
}
