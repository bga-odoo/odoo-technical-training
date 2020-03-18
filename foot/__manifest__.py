# -*- coding: utf-8 -*-
{
    'name' : "Football_training",

    'summary' : """To manage my technical training""",

    'description' : """Description of my training""",

    'author' : "BGA",

    'website' : "https://www.odoo.com",

    'depends' : [
        
        'base',
        'sale',
    ],

    'data' : [

        'security/ir.model.access.csv',
        'views/team.xml',
        'views/game.xml',
        'views/partner.xml',
        'views/appearance.xml',
        'data/menus.xml',
        'data/product.xml',
    ],

    'demo' : [
        
    ],


}