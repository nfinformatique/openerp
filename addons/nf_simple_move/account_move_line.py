from openerp.osv import osv, fields

class account_move_line(osv.osv):
    _inherit= "account.move.line"
    _order = "date desc, move_id desc, account_id asc"
account_move_line()