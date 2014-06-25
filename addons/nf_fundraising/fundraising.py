# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from datetime import date,datetime

class account_move_line_attr(osv.osv):
    _name = "account.move.line"
    _inherit = "account.move.line"
    _columns = {
                'attribution_id': fields.many2one("nf_fundraising.attribution","Attribution",ondelete="restrict",select=True),
                }

account_move_line_attr    


    
