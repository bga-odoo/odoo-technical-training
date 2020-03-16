from odoo import models, fields

class Teams(models.Model):
    _name ='foot.team'
    _descritpion = "Teams"

    name = fields.Char(string="Name" required="1")
    