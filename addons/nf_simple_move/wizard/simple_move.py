# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from datetime import date,datetime
import openerp.addons.decimal_precision as dp

class simple_move(osv.osv_memory):
    _name="nf_simple_move.wiz.simple_move"
    _description="simple Move"
    _columns = {
                'name': fields.char('Name', size=64, required=True),
                'journal_id': fields.many2one("account.journal","Journal",required=True),#,domain=[('journal_type','=','general')]),
                'period_id': fields.many2one("account.period","Period",required=True),
                'date': fields.date("Date",required=True),
                'move_id': fields.many2one("account.move","Move"),
                'debit_tax_id':fields.many2one('account.tax', 'Tax Credit'),
                'credit_tax_id':fields.many2one('account.tax', 'Tax Debit'),
                'amount': fields.float('Amount', digits_compute=dp.get_precision('Account')),
                'currency_id': fields.many2one('res.currency', 'Currency', help="The optional other currency if it is a multi-currency entry."),
                'credit_account_id': fields.many2one('account.account', 'Credit Account', required=True, ondelete="cascade", domain=[('type','<>','view'), ('type', '<>', 'closed')], select=2),
                'debit_account_id': fields.many2one('account.account', 'Debit Account', required=True, ondelete="cascade", domain=[('type','<>','view'), ('type', '<>', 'closed')], select=2),
                'company_id': fields.related('journal_id', 'company_id', type='many2one', relation='res.company', string='Company', store=False, readonly=True),
                }
    
    def _get_default_date(self,cr,uid,context={}):
        date=None
        
        if 'move_line_record_id' in context:
            move_line_obj=self.pool.get("account.move.line")
            move_line = move_line_obj.browse(cr,uid,context['move_line_record_id'])
            return move_line.move_id.date 
            #get date from move
        else:
            period_obj=self.pool.get("account.period")
            if 'journal_id' in context and 'period_id' in context:
                cr.execute('''SELECT move_id, date FROM account_move_line
                            WHERE journal_id = %s AND period_id = %s
                             ORDER BY date DESC limit 1''', (context['journal_id'], context['period_id']))
                res = cr.fetchone()
                date = res and res[1] or period_obj.browse(cr, uid, context['period_id'], context=context).date_start
            
        return date
    
    def _get_default_journal(self,cr,uid,context={}):
        if 'move_line_record_id' in context:
            move_line_obj=self.pool.get("account.move.line")
            move_line = move_line_obj.browse(cr,uid,context['move_line_record_id'])
            return move_line.move_id.journal_id.id 
            #get date from move
        
        if 'journal_id' in context:
            return context['journal_id']
        return False
    
    def _get_default_company(self,cr,uid,context={}):
        if 'move_line_record_id' in context:
            move_line_obj=self.pool.get("account.move.line")
            move_line = move_line_obj.browse(cr,uid,context['move_line_record_id'])
            return move_line.move_id.journal_id.company_id.id 
            #get date from move
        
        if 'journal_id' in context:
            return  self.pool.get("account.journal").browse(cr,uid,context['journal_id'],context=context).company_id.id
        return False
    
    def _get_default_period(self,cr,uid,context={}):
        if 'move_line_record_id' in context:
            move_line_obj=self.pool.get("account.move.line")
            move_line = move_line_obj.browse(cr,uid,context['move_line_record_id'])
            return move_line.move_id.period_id.id
            #get date from move
        
        if 'period_id' in context:
            return context['period_id']
        return False
    
    def _get_default_credit_account(self,cr,uid,context={}):
        return False
    def _get_default_debit_account(self,cr,uid,context={}):
        return False
    def _get_default_amount(self,cr,uid,context={}):
        if 'move_line_record_id' in context:
            move_line_obj=self.pool.get("account.move.line")
            move_line = move_line_obj.browse(cr,uid,context['move_line_record_id'])
            return 0.0
#            return move_line.move_id.date 
            #get date from move
            
    def _get_default_move(self,cr,uid,context={}):
        if 'move_line_record_id' in context:
            move_line_obj=self.pool.get("account.move.line")
            move_line = move_line_obj.browse(cr,uid,context['move_line_record_id'])
            return move_line.move_id.id 
            #get date from move
        
    def _get_default_debit_tax(self,cr,uid,context={}):
        return False
    def _get_default_credit_tax(self,cr,uid,context={}):
        return False
    def _get_default_name(self,cr,uid,context={}):
        return False
    def _get_default_alert(self,cr,uid,context={}):
        osv.except_osv(_('Do not use default fct') ,"Bad guy !")
        return False
    
    _defaults = {
        'name': _get_default_alert,
        'date': _get_default_alert,
        'journal_id': _get_default_alert,
        'period_id': _get_default_alert,
        'credit_account_id' : _get_default_alert,
        'debit_account_id' : _get_default_alert,
        'company_id': _get_default_alert,
        'move_id': _get_default_alert,
        'debit_tax_id':_get_default_alert,
        'credit_tax_id':_get_default_alert,
        'amount': _get_default_alert,
        'currency_id': _get_default_alert,
    }

    def default_get(self,cr,uid,fields,context={}):
        res={}
        
        #Opening existing entry
        if 'move_line_record_id' in context and context['move_line_record_id']:
            move_line_obj=self.pool.get("account.move.line")
            move_line = move_line_obj.browse(cr,uid,context['move_line_record_id'])
            move=move_line.move_id
            #get first untaxed line
            untaxed_line=False
            taxed_line=False
            if len(move.line_id)>3:
                osv.except_osv(_('This entry is not simple enough for me') ,"This entry is not simple enough for me!")
            for line in move.line_id:
                if not line.account_tax_id and not line.tax_code_id:
                    untaxed_line=line
                if line.account_tax_id and line.tax_code_id:
                    taxed_line=line
                    
            first_line=untaxed_line   
            second_line=taxed_line
            if not second_line:
                for line in move.line_id:
                    if not line.account_tax_id and not line.tax_code_id and not line == untaxed_line:
                        second_line=line
                        
                
            res['name']=first_line.name
            res['date']=move.date
            res['journal_id']=move.journal_id.id
            res['period_id']=move.period_id.id
            res['credit_account_id']=second_line.account_id.id if second_line.credit>0.0 else first_line.account_id.id  
            res['debit_account_id']=second_line.account_id.id if second_line.debit>0.0 else first_line.account_id.id
            res['company_id']=move.company_id.id
            res['move_id']=move.id
            res['debit_tax_id']=taxed_line.account_tax_id.id if taxed_line and taxed_line.debit>0.0 else False
            res['credit_tax_id']=taxed_line.account_tax_id.id if taxed_line and taxed_line.credit>0.0 else False
            res['amount']=first_line.credit if first_line.credit>0.0 else first_line.debit 
            res['currency_id']=first_line.currency_id.id
            
        #Creating new entry
        else:
            res['name']=""
            period_obj=self.pool.get("account.period")
            if 'journal_id' in context and 'period_id' in context:
                cr.execute('''SELECT move_id, date FROM account_move_line
                            WHERE journal_id = %s AND period_id = %s
                             ORDER BY date DESC limit 1''', (context['journal_id'], context['period_id']))
                crres = cr.fetchone()
                res['date'] = crres[1] if crres else period_obj.browse(cr, uid, context['period_id'], context=context).date_start
            else:
                res['date']=False
                                
            if 'journal_id' in context:
                res['journal_id']=context['journal_id']
            else:
                res['journal_id']=False
            if 'period_id' in context:
                res['period_id']= context['period_id']
            else:
                res['period_id']=False
            res['credit_account_id']=False
            res['debit_account_id']=False
            if 'journal_id' in context:
                res['company_id']=self.pool.get("account.journal").browse(cr,uid,context['journal_id'],context=context).company_id.id
            else:
                res['company_id']=False
            
            res['move_id']=False
            res['debit_tax_id']=False
            res['credit_tax_id']=False
            res['amount']=0.0
            res['currency_id']=False
            
            
        return res
        

    def get_period_from_date(self,cr,uid,ids,date,period_id,context={}):
        period_obj=self.pool.get("account.period")
        return period_obj.find(cr,uid,date,context)
        
    def basic_check(self,cr,uid,ids):
        return True
        
    def create_entries(self,cr,uid,ids,context={}):
        move_line_obj=self.pool.get("account.move.line")
        modified_ids=[]
        for wiz in self.browse(cr,uid,ids,context=context):
            #create entry with debit
            move=wiz.move_id or False
            if move:
                for line in move.line_id:
                    modified_ids.append(line.id)
                    line.unlink(context=context)
            vals={
                  'name': wiz.name,
                  'debit':wiz.amount,
                  'credit':0.0,
                  'account_id':wiz.debit_account_id.id,
                  'move_id':move and move.id or False,
                  'journal_id':wiz.journal_id.id,
                  'period_id':wiz.period_id.id,
                  'date':wiz.date,
                  'account_tax_id':wiz.debit_tax_id.id,
                  }
            id=move_line_obj.create(cr,uid,vals,context=context)
            if not move:
                move_line = move_line_obj.browse(cr,uid,id)
                move=move_line.move_id
            #create entry with credit
            vals={
                  'name': wiz.name,
                  'debit':0.0,
                  'credit':wiz.amount,
                  'account_id':wiz.credit_account_id.id,
                  'move_id':move.id,
                  'journal_id':wiz.journal_id.id,
                  'period_id':wiz.period_id.id,
                  'date':wiz.date,
                  'account_tax_id':wiz.credit_tax_id.id,
                  }
            id=move_line_obj.create(cr,uid,vals,context=context)
            modified_ids.append(map(lambda x:x.id,move.line_id))
            
            wiz.unlink()
        return modified_ids
        
    def action_validate_close(self,cr,uid,ids,context={}):
        modified_ids=self.create_entries(cr,uid,ids,context=context)
        return { 'type': 'ir.actions.client', 'tag': 'simple_move.reload', 'params':{'modified_ids':modified_ids,'close':True} }
    
    def action_validate_new(self,cr,uid,ids,context={}):
        modified_ids=self.create_entries(cr,uid,ids,context=context)
        return { 'type': 'ir.actions.client', 'tag': 'simple_move.reload', 'params':{'modified_ids':modified_ids,'close':False} }
#        return { 'type': 'ir.actions.client', 'tag': 'reload' }
    
#     def action_cancel(self,cr,uid,ids,context={}):
#         return { 'type': 'ir.actions.client', 'tag': 'simple_move.reload', 'params':{'modified_ids':[],'close':True} }
    
    def on_change_date(self,cr,uid,ids,date,context={}):
        period_obj=self.pool.get("account.period")

        return {}
    def on_change_credit_account(self,cr,uid,ids,credit_account_id,debit_tax_id,credit_tax_id,context={}):
        move_line_obj=self.pool.get("account.move.line")
        res=move_line_obj.onchange_account_id(cr,uid,ids,credit_account_id,context=context)
        if 'value' in res and 'account_tax_id' in res['value'] and res['value']['account_tax_id']:
            return {'value':{'credit_tax_id':res['value']['account_tax_id'],'debit_tax_id':False}} 
        return {}
    
    def on_change_debit_account(self,cr,uid,ids,debit_account_id,debit_tax_id,credit_tax_id,context={}):
        move_line_obj=self.pool.get("account.move.line")
        res=move_line_obj.onchange_account_id(cr,uid,ids,debit_account_id,context=context)
        if 'value' in res and 'account_tax_id' in res['value'] and res['value']['account_tax_id']:
            return {'value':{'debit_tax_id':res['value']['account_tax_id'],'credit_tax_id':False}} 
        return {}
        
simple_move()