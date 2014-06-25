# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from datetime import date,datetime

class wiz_list_attestation(osv.osv_memory):
    _name="nf_fundraising.wiz.listattestation"
    _description="Lister les attestations à remercier"
    _columns = {
                'name':fields.char("Nom"),
                'gift_ids':fields.many2many("nf_fundraising.gift","nf_fundraising_attestation_wiz_gift","gift_id","wiz_id","Dons choisis",domain=[('attestation_id','=',False),('state','=','valid')]),
                }
    def _prefill(self,cr,uid,context={}):
        return self.pool.get('nf_fundraising.gift').search(cr,uid,[('attestation_id','=',False),('state','=','valid')])
        
#         gift_ids = gift_obj.search(cr,uid,[("attestation_id","=",False),('state','=','valid')])
#             
#         self.write(cr,uid,ids,{
#                      'gift_ids':[(6,0,gift_ids)],
#                      }, context=context)
        
    
    _defaults = {
                 'gift_ids': _prefill,
                 }
    
    
        
    def action_validate(self,cr,uid,ids,context={}):
        #link related gifts
        gift_obj=self.pool.get("nf_fundraising.gift")
        attestation_obj=self.pool.get("nf_fundraising.attestation")
        attestation_id=context['active_id']
        this = self.browse(cr, uid, ids, context=context)[0]
        for gift in this.gift_ids:
            if gift.attestation_id:
                 raise osv.except_osv(_('Erreur!'), _('Vous essayez d\'attester un don qui l\'est déjà. (id : %s)') % gift.id)
            gift.write({'attestation_id':attestation_id})
        attestation_obj.write(cr,uid,[attestation_id],{'state':'listed'})
        return { 'type': 'ir.actions.client', 'tag': 'reload' }
        
wiz_list_attestation()