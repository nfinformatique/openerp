# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from datetime import date,datetime


class gift(osv.osv):
    _name = 'nf_fundraising.gift'
    
    def unlink(self,cr,uid,ids,context={}):
        for thegift in self.browse(cr,uid,ids):
            if thegift.state!='draft':
                raise osv.except_osv('Erreur!', u"Impossible d'effacer un don qui n'est pas brouillon ! (don du %s)"%thegift.date)
            if thegift.move_id :
                print type(thegift.move_id)
                raise osv.except_osv('Erreur!', u"Impossible d'effacer un don lié à un mouvement comptable ! (don du %s)"%thegift.date)
            for attr in thegift.attribution_ids:
                attr.unlink()
        return super(gift,self).unlink(cr,uid,ids,context)
                
    
    def validate(self,cr,uid,ids,context={}):
        move_obj=self.pool.get("account.move")
        period_obj=self.pool.get("account.period")
        move_line_obj=self.pool.get("account.move.line")
        attr_obj=self.pool.get("nf_fundraising.attribution")
        for gift in self.browse(cr,uid,ids):
            if gift.amount<=0.0:
                raise osv.except_osv('Erreur!', u"Le don est égal ou inférieur à zéro !")
            
            #check if sum of attributions equals amount
            sum=0.0
            
            for gift_attribution in gift.attribution_ids:
                if gift_attribution.amount==0.0:
                    attr_obj.unlink(cr,uid,gift_attribution.id,context=context)
                else:
                    sum+=gift_attribution.amount
                
                
            if sum!=gift.amount:
                raise osv.except_osv('Erreur!', u"Le total des attributions ne correspond pas au total du don !")

            period_id=period_obj.find(cr,uid,gift.date)[0]
            period=period_obj.browse(cr,uid,period_id)
            if period.state!="draft":
                raise osv.except_osv('Erreur!', u"La période comptable concernée est fermée !")
                

            #Create move
            #MOVE: journal_id, period_id, date, to_check, line_id
            #MOVE (opt) : ref, 
            move_vals={
                       'journal_id':gift.journal_id.id,
                       'period_id':period.id,
                       'date':gift.date,
                       'to_check': True,
                       'line_id':[],
                       'ref':"Don #%s"%gift.id,
                       'partner_id':gift.partner_id.id,
                       }
            move_id = move_obj.create(cr,uid,move_vals)
            
            #CREATE LINE FOR BANK ACCOUNT
            line_vals={
                       'date':gift.date,
                       'period_id':period.id,
                       'move_id':move_id,
                       'account_id':gift.journal_id.default_debit_account_id.id,
                       'debit':gift.amount,
                       'attribution_id':False,
                       'name':"Don #%s"%gift.id,
                       'journal_id':gift.journal_id.id,
                       'partner_id':gift.partner_id.id,
                       }
            move_line_obj.create(cr,uid,line_vals)
            #CREATE LINES FOR GIFT ACCOUNTS 
            for gift_attribution in gift.attribution_ids:
                line_vals={
                           'date':gift.date,
                           'period_id':period.id,
                           'move_id':move_id,
                           'account_id':gift_attribution.attribution_id.account_id.id,
                           'credit':gift_attribution.amount,
                           'attribution_id':gift_attribution.attribution_id.id,
                           'name':"Don #%s"%gift.id,
#                           'journal_id':gift_attribution.attribution_id.journal_id.id,
                           'journal_id':gift.journal_id.id,
                           'partner_id':gift.partner_id.id,
                        
                           }
                move_line_obj.create(cr,uid,line_vals)
                
            move_obj.post(cr,uid,[move_id],context=context)
            
            self.write(cr,uid,[gift.id],{'state':'valid','move_id':move_id})
            
        
        
    def set_draft(self,cr,uid,ids,context={}):
        move_obj=self.pool.get("account.move")
        for gift in self.browse(cr,uid,ids):
            if gift.move_id:
                move_obj.button_cancel(cr,uid,[gift.move_id.id])
                gift.write({'move_id':False})
                move_obj.unlink(cr,uid,[gift.move_id.id])
            
            self.write(cr,uid,[gift.id],{'state':'draft'})
        
        
    def onchange_sol(self,cr,uid,ids,sol_id,attr_ids,amount=0.0):
        #don't change attributions if existing
        res={}
        res['value']={}
        if not sol_id is None and not sol_id is False:
            sol_obj=self.pool.get("nf_fundraising.solicitation")
            sol=sol_obj.browse(cr,uid,sol_id)
            if len(attr_ids)==0 or (len(attr_ids)==1 and attr_ids[0][0]==5):
                attrs_ids=[]
                for attr in sol.attribution_ids:
                    attr_amount = round(amount/float(len(sol.attribution_ids)),2)
                    new_attr={'attribution_id':attr.id,'amount':attr_amount}
                    attrs_ids.append(new_attr)
                res['value'].update({'attribution_ids':attrs_ids})
#            res['value'].update({'journal_id':sol.journal_id.id})
        return res
    
    def onchange_partner(self,cr,uid,ids,partner_id,solicitation_id,attribution_ids):
        #GET PARTNER OPENED SOLICITATIONS AND AUTO ADD IF #1
        return {}
        #don't change attributions if existing
        res={}
        res['value']={}
        if not sol_id is None:
            sol_obj=self.pool.get("nf_fundraising.solicitation")
            sol=sol_obj.browse(cr,uid,sol_id)
            if len(attr_ids)==0 or (len(attr_ids)==1 and attr_ids[0][0]==5):
                attrs_ids=[]
                for attr in sol.attribution_ids:
                    new_attr={'attribution_id':attr.id,'amount':0.0}
                    attrs_ids.append(new_attr)
                res['value'].update({'attribution_ids':attrs_ids})
            res['value'].update({'journal_id':sol.journal_id.id})
        return res
        
    
    def _get_store_ids(self,cr,uid,ids,context={}):
        gift_obj = self.pool.get("nf_fundraising.gift")
        if self._name=="account.move":
            return gift_obj.search(cr,uid,[('move_id','in',ids)])
        
    _columns = {
                'state': fields.selection((("draft",u"Brouillon"),("valid",u"Validé")),u"État",readonly=True),
                'move_id': fields.many2one("account.move",u'Mouvement',ondelete="restrict"),
                'period_id':  fields.related('move_id','period_id', type='many2one', string=u"Période",relation="account.period", readonly=True,store={
                                                                                                                   'account.move': (_get_store_ids,['period_id'],10)
                                                                                                                   }),
                'amount':fields.float(u"Montant total",required=True),
                'date': fields.date(u"Date",required=True),
                'journal_id': fields.many2one("account.journal",u"Journal",ondelete="restrict",select=True, required=True),
                
                #'period_id': fields.many2one("account.period",u"Période",ondelete="restrict",select=True, required=True),
                'partner_id':fields.many2one("res.partner",u"Partenaire",ondelete="restrict",select=True, required=True),
                'attribution_ids': fields.one2many("nf_fundraising.gift.attribution","gift_id",u"Attributions",required=True),
                'solicitation_id': fields.many2one("nf_fundraising.solicitation",u"Solicitation",required=True,ondelete="restrict"),
                'thanks_id':fields.many2one("nf_fundraising.thanks",u"Remerciement lié",ondelete="restrict"),
                'attestation_id':fields.many2one("nf_fundraising.attestation",u"Attestation liée",ondelete="restrict"),
#                 'thanked': fields.boolean("Remercié"),
#                 'attested': fields.boolean("Attesté"),
#                'credit_account_id': fields.many2one('account.account','Compte de crédit',ondelete="restrict",select=True, required=True),
                }
    _defaults ={
                'state':'draft',
                "date": lambda *a: date.today().strftime('%Y-%m-%d'),
                }
gift()   
    