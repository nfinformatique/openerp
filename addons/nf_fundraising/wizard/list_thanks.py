# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from datetime import date,datetime

class wiz_list_thanks(osv.osv_memory):
    _name="nf_fundraising.wiz.listthanks"
    _description="Lister les dons à remercier"
    _columns = {
                'name':fields.char("Nom"),
                'attribution_ids':fields.many2many("nf_fundraising.attribution","nf_fundraising_thank_wiz_attribution_rel","attribution_id","thank_id","Filtrer par attributions"),
                'gift_ids':fields.many2many("nf_fundraising.gift","nf_fundraising_thank_wiz_gift","gift_id","wiz_id","Dons choisis",domain=[('thanks_id','=',False),('state','=','valid')]),
                }
    
    def action_list(self,cr,uid,ids,context={}):
        #TESTER QUE LES REMERCIEMENT SOIENT OUVERTS
        #TESTER QUE LES DONS SOIENT BIEN NON REMERCIÉS
        gift_obj=self.pool.get("nf_fundraising.gift")
    
    
        thanks_id=context['active_id']
        this = self.browse(cr, uid, ids, context=context)[0]
        
        if len(this.attribution_ids)>0:
            gift_attr_obj=self.pool.get("nf_fundraising.gift.attribution")
            attr_ids = gift_attr_obj.search(cr,uid,[('state','=','valid'),("attribution_id",'in',[x.id for x in this.attribution_ids])])
            gift_ids=[]
            for attr in gift_attr_obj.browse(cr,uid,attr_ids):
                if attr.gift_id.thanks_id :
                    continue
                gift_ids.append(attr.gift_id.id)
        else:
            gift_ids = gift_obj.search(cr,uid,[("thanks_id","=",False),('state','=','valid')])
            
        self.write(cr,uid,ids,{
                     'gift_ids':[(6,0,gift_ids)],
                     }, context=context)
        

        try:
            dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'nf_fundraising', 'wiz_thanks_review')
        except ValueError, e:
            view_id = False

        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Dons à remercier',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'nf_fundraising.wiz.listthanks',
#            'nodestroy': 'true',
            'target': 'new',
            'context':context,
#            'domain':{'moniteur_id':[('id','not in',excluded_partners)]},
#            'res_id': this.student.id, # assuming the many2one is (mis)named 'student'
            'res_id':ids[0],
            'views': [(view_id, 'form')],
        }
        
    def action_validate(self,cr,uid,ids,context={}):
        #link related gifts
        gift_obj=self.pool.get("nf_fundraising.gift")
        thanks_obj=self.pool.get("nf_fundraising.thanks")
        thanks_id=context['active_id']
        this = self.browse(cr, uid, ids, context=context)[0]
        for gift in this.gift_ids:
            if gift.thanks_id:
                 raise osv.except_osv(_('Erreur!'), _('Vous essayez de remercier un don qui l\'est déjà. (id : %s)') % gift.id)
            gift.write({'thanks_id':thanks_id})
        thanks_obj.write(cr,uid,[thanks_id],{'state':'listed'})
        return { 'type': 'ir.actions.client', 'tag': 'reload' }
        
wiz_list_thanks()