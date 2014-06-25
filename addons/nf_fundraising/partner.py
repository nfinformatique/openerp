# -*- coding: utf-8 -*-

from dbfpy import dbf


from openerp.osv import osv, fields
from datetime import date,datetime
import types
import difflib

    


class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner' 

    
    def get_all_gifts(self,cr,uid,ids,field_names,arg,context):
        ret={}
        for partner in self.browse(cr,uid,ids):
            last_date=False
            total=0.0
            for gift in partner.gift_ids:
                if gift.state=="valid":
                    total+=gift.amount
                    if not last_date or last_date < gift.date:
                        last_date=gift.date
            ret[partner.id]={'total_dons':total,'dernier_don':last_date}
        return ret
    
    
    def is_gift_partner(self,cr,uid,ids,context={}):
        #get all partners
        gift_obj=self.pool.get("nf_fundraising.gift")
        partner_ids=[]
        for gift in gift_obj.browse(cr,uid,ids):
            if gift.partner_id.id not in partner_ids:
                partner_ids.append(gift.partner_id.id) 
        return partner_ids
    
    store_gifts = {
                   'nf_fundraising.gift':(
                                  is_gift_partner,
                                  ['state','amount','date','partner_id'],
                                  5
                                  )
                   }
    _columns = {
#        'external_id': fields.char(u'Identifiant extérieur',size=128,readonly=True ),
        'code_dp': fields.char(u'Code Donner Perfect',size=128,select=True),
        'donor': fields.boolean(u'Donateur'),
        
        #FIELDS FROM DP:
        'anonymous': fields.boolean(u'Anonyme'),#ANONYME
        'dp_pas_lettre': fields.boolean(u'Pas de lettre'),#PAS_LETTRE
        'nomail': fields.boolean(u'Pas de Courrier'),#NOMAIL
        'noemail': fields.boolean(u'Pas de Courriel'),#NOEMAIL
        
        'nothanks': fields.boolean(u'Pas de remerciements'),
        'noattestation': fields.boolean(u'Pas d\'attestation'),
        
        'dp_text': fields.text(u'Champ de texte Donor Perfect'),
        'attribution_ids': fields.many2many("nf_fundraising.attribution","nf_fundraising_attribution_partner_rel","partner_id","attribution_id",u'Attributions à solliciter',ondelete="restrict",select=True),
        'solicitation_ids': fields.many2many('nf_fundraising.solicitation','nf_fundraising_solicitation_partner_rel','partner_id','solicitation_id','Solicitations',domain="[]",readonly=True),
        'gift_ids': fields.one2many("nf_fundraising.gift","partner_id","Dons"),
        'total_dons': fields.function(get_all_gifts,string=u'Total des dons',method=True,type="float",multi="pgift",store=store_gifts),
        'dernier_don': fields.function(get_all_gifts,string=u'Dernier don',method=True,type="date",multi="pgift",store=store_gifts),
    }
    
# Contraintes de clés étrangères :
#     "res_partner_assistant_id_fkey" FOREIGN KEY (assistant_id) REFERENCES res_partner(id) ON DELETE RESTRICT
#     "res_partner_country_id_fkey" FOREIGN KEY (country_id) REFERENCES res_country(id) ON DELETE SET NULL
#     "res_partner_foyer_id_fkey" FOREIGN KEY (foyer_id) REFERENCES res_partner(id) ON DELETE RESTRICT
#     "res_partner_parents_id_fkey" FOREIGN KEY (parents_id) REFERENCES res_partner(id) ON DELETE RESTRICT
#     "res_partner_state_id_fkey" FOREIGN KEY (state_id) REFERENCES res_country_state(id) ON DELETE SET NULL
#     "res_partner_title_fkey" FOREIGN KEY (title) REFERENCES res_partner_title(id) ON DELETE SET NULL
# Référencé par :
#    TABLE "account_bank_statement_line" CONSTRAINT "account_bank_statement_line_partner_id_fkey" FOREIGN KEY (partner_id) REFERENCES res_partner(id) ON DELETE SET NULL
#     TABLE "account_invoice" CONSTRAINT "account_invoice_partner_id_fkey" FOREIGN KEY (partner_id) REFERENCES res_partner(id) ON DELETE SET NULL
#     TABLE "account_voucher" CONSTRAINT "account_voucher_partner_id_fkey" FOREIGN KEY (partner_id) REFERENCES res_partner(id) ON DELETE SET NULL
#     TABLE "nf_fgb_inscription" CONSTRAINT "nf_fgb_inscription_partner_id_fkey" FOREIGN KEY (partner_id) REFERENCES res_partner(id) ON DELETE RESTRICT
#     TABLE "nf_fgb_inscription_web" CONSTRAINT "nf_fgb_inscription_web_partner_id_fkey" FOREIGN KEY (partner_id) REFERENCES res_partner(id) ON DELETE RESTRICT
#     TABLE "nf_fundraising_attribution_partner_rel" CONSTRAINT "nf_fundraising_attribution_partner_rel_partner_id_fkey" FOREIGN KEY (partner_id) REFERENCES res_partner(id) ON DELETE CASCADE
#     TABLE "nf_fundraising_gift" CONSTRAINT "nf_fundraising_gift_partner_id_fkey" FOREIGN KEY (partner_id) REFERENCES res_partner(id) ON DELETE RESTRICT
#     TABLE "nf_fundraising_solicitation_partner_rel" CONSTRAINT "nf_fundraising_solicitation_partner_rel_partner_id_fkey" FOREIGN KEY (partner_id) REFERENCES res_partner(id) ON DELETE CASCADE
#     TABLE "res_partner" CONSTRAINT "res_partner_assistant_id_fkey" FOREIGN KEY (assistant_id) REFERENCES res_partner(id) ON DELETE RESTRICT
#     TABLE "res_partner" CONSTRAINT "res_partner_foyer_id_fkey" FOREIGN KEY (foyer_id) REFERENCES res_partner(id) ON DELETE RESTRICT
#     TABLE "res_partner" CONSTRAINT "res_partner_parents_id_fkey" FOREIGN KEY (parents_id) REFERENCES res_partner(id) ON DELETE RESTRICT
#     TABLE "res_partner_res_partner_category_rel" CONSTRAINT "res_partner_res_partner_category_rel_partner_id_fkey" FOREIGN KEY (partner_id) REFERENCES res_partner(id) ON DELETE CASCADE
# 
#     
    
    
    def _merge(self,cr,uid,ids,context={}):
        if len(ids) < 2:
            raise orm.except_orm(_('Configuration Error!'),
                 _('Please select multiple merge partner'))
        #take first as container
        main=self.browse(cr,uid,ids[0])
        vals={}
        for other in self.browse(cr,uid,ids[1:]):
            #keep main address
            if not main.assistant_id and other.assistant_id:
                vals['assistant_id']=other.assistant_id.id
            if not main.country_id and other.country_id:
                vals['country_id']=other.country_id.id
            if not main.foyer_id and other.foyer_id:
                vals['foyer_id']=other.foyer_id.id
            if not main.parents_id and other.parents_id:
                vals['parents_id']=other.parents_id.id
            if not main.state_id and other.state_id:
                vals['state_id']=other.state_id.id
            if not main.title and other.title:
                vals['title']=other.title.id
            if not main.date_naissance and other.date_naissance:
                vals['date_naissance']=other.date_naissance
            if not main.gender and other.gender:
                vals['gender']=other.gender
            if not main.phone and other.phone:
                vals['phone']=other.phone
            if not main.mobile and other.mobile:
                vals['mobile']=other.mobile
            if not main.email and other.email:
                vals['email']=other.email
            if not main.fax and other.fax:
                vals['fax']=other.fax
            if not main.ref and other.ref:
                vals['ref']=other.ref
            if not main.warn_text and other.warn_text:
                vals['warn_text']=other.warn_text
            if not main.street and other.street:
                vals['street']=other.street
            if not main.street2 and other.street2:
                vals['street2']=other.street2
            if not main.zip and other.zip:
                vals['zip']=other.zip
            if not main.city and other.city:
                vals['city']=other.city
            if not main.prenom and other.prenom:
                vals['prenom']=other.prenom
                
            vals['enfant']=main.enfant or other.enfant
            vals['adulte']=main.adulte or other.adulte
            vals['moniteur']=main.moniteur or other.moniteur
            vals['foyer']=main.foyer or other.foyer
            vals['assistant']=main.assistant or other.assistant
            vals['ignore_double']=main.ignore_double or other.ignore_double
            vals['donor']=main.donor or other.donor
            vals['nothanks']=main.nothanks or other.nothanks
            vals['noattestation']=main.noattestation or other.noattestation
            vals['anonymous']=main.anonymous or other.anonymous
            vals['nomail']=main.nomail or other.nomail
            vals['noemail']=main.noemail or other.noemail
            vals['dp_pas_lettre']=main.dp_pas_lettre or other.dp_pas_lettre
            vals['active']=main.active or other.active
            
            
            vals['comment']=(main.comment or "")+(other.comment or "")
            vals['code_dp']=(main.code_dp or "")+(other.code_dp or "")
            vals['history']=(main.history or "")+(other.history or "")
            vals['transit']=(main.transit or "")+(other.transit or "")
                
            other.write({'active':False})
            cr.execute("UPDATE account_bank_statement_line SET partner_id=%s WHERE partner_id=%s"%(main.id,other.id))
            cr.execute("UPDATE account_invoice SET partner_id=%s WHERE partner_id=%s"%(main.id,other.id))
            cr.execute("UPDATE account_voucher SET partner_id=%s WHERE partner_id=%s"%(main.id,other.id))
            cr.execute("UPDATE nf_fgb_inscription SET partner_id=%s WHERE partner_id=%s"%(main.id,other.id))
            cr.execute("UPDATE nf_fgb_inscription_web SET partner_id=%s WHERE partner_id=%s"%(main.id,other.id))
            cr.execute("UPDATE nf_fundraising_attribution_partner_rel SET partner_id=%s WHERE partner_id=%s"%(main.id,other.id))
            cr.execute("UPDATE nf_fundraising_gift SET partner_id=%s WHERE partner_id=%s"%(main.id,other.id))
            cr.execute("UPDATE nf_fundraising_solicitation_partner_rel SET partner_id=%s WHERE partner_id=%s"%(main.id,other.id))
            cr.execute("UPDATE res_partner SET assistant_id=%s WHERE assistant_id=%s"%(main.id,other.id))
            cr.execute("UPDATE res_partner SET foyer_id=%s WHERE foyer_id=%s"%(main.id,other.id))
            cr.execute("UPDATE res_partner SET parents_id=%s WHERE parents_id=%s"%(main.id,other.id))
            cr.execute("UPDATE res_partner_res_partner_category_rel SET partner_id=%s WHERE partner_id=%s"%(main.id,other.id))
        main.write(vals)
        return True
    
    def merge_doubles(self,cr,uid,ids=[],context={}):
        min_ratio=0.9
        emailcnt=0
        #MATCH ON EMAIL
        ids=self.search(cr,uid,[('active','=','t'),('email','!=',False),('donor','=',True)],order="email ASC",context=context)
        merged_ids=[]
        for main in self.browse(cr,uid,ids,context=context):
            other_ids=self.search(cr,uid,[('active','=','t'),('email','=',main.email),('donor','=',False)],order="email ASC",context=context)
            if len(other_ids) > 0:
                for other in self.browse(cr,uid,other_ids,context=context):
                    #match par email+nom+prénom+code postal
                    if main.name and other.name and main.prenom and other.prenom and main.zip and other.zip:
                        name_ratio = difflib.SequenceMatcher(a=main.name.lower(),b=other.name.lower()).ratio() 
                        prenom_ratio = difflib.SequenceMatcher(a=main.prenom.lower(),b=other.prenom.lower()).ratio() 
                        zip_ratio = difflib.SequenceMatcher(a=main.zip.lower(),b=other.zip.lower()).ratio()
                        if min(name_ratio,prenom_ratio,zip_ratio)> min_ratio:
                            
                            print "MERGING (email):"
                            print "     %s %s     with"%(main.name,main.prenom)
                            print "     %s %s     (%s,%s)"%(other.name,other.prenom,main.email,other.email)
                            emailcnt+=1
                            merged_ids.append(main.id)
                            self._merge(cr,uid,[main.id,other.id],context=context) 
            
        #match par date de naissance+nom+prenom+N°Tél épuré ENSUITE
        datecnt=0
        ids=self.search(cr,uid,[('active','=','t'),('date_naissance','!=',False),('donor','=',True),('id','not in',merged_ids)],order="date_naissance ASC",context=context)
        for main in self.browse(cr,uid,ids,context=context):
            if not main.date_naissance:
                continue
            other_ids=self.search(cr,uid,[('active','=','t'),('date_naissance','=',main.date_naissance),('donor','=',False)],order="date_naissance ASC",context=context)
            if len(other_ids) > 0:
                for other in self.browse(cr,uid,other_ids,context=context):
                    #match par email+nom+prénom+code postal
                    if main.name and other.name and main.prenom and other.prenom and main.zip and other.zip:
                        name_ratio = difflib.SequenceMatcher(a=main.name.lower(),b=other.name.lower()).ratio() 
                        prenom_ratio = difflib.SequenceMatcher(a=main.prenom.lower(),b=other.prenom.lower()).ratio() 
                        zip_ratio = difflib.SequenceMatcher(a=main.zip.lower(),b=other.zip.lower()).ratio()
                        if min(name_ratio,prenom_ratio,zip_ratio)> min_ratio:
                            
                            print "MERGING (date):"
                            print "     %s %s     with"%(main.name,main.prenom)
                            print "     %s %s     (%s,%s)"%(other.name,other.prenom,main.date_naissance,other.date_naissance)
                            datecnt+=1
                            merged_ids.append(main.id)
                            self._merge(cr,uid,[main.id,other.id],context=context) 

        namecnt=0
        ids=self.search(cr,uid,[('active','=','t'),('prenom','!=',False),('donor','=',True),('id','not in',merged_ids)],order="prenom ASC",context=context)
        for main in self.browse(cr,uid,ids,context=context):
            other_ids=self.search(cr,uid,[('active','=','t'),('prenom','=',main.prenom),('donor','=',False)],order="prenom ASC",context=context)
            if len(other_ids) > 0:
                for other in self.browse(cr,uid,other_ids,context=context):
                    #match par email+nom+prénom+code postal
                    if main.name and other.name and main.phone and other.phone and main.zip and other.zip:
                        name_ratio = difflib.SequenceMatcher(a=main.name.lower(),b=other.name.lower()).ratio() 
                        phone_ratio = difflib.SequenceMatcher(a=main.phone.lower(),b=other.phone.lower()).ratio() 
                        zip_ratio = difflib.SequenceMatcher(a=main.zip.lower(),b=other.zip.lower()).ratio()
                        if min(name_ratio,phone_ratio,zip_ratio)> min_ratio:
                            
                            print "MERGING (prenom):"
                            print "     %s %s     with"%(main.name,main.prenom)
                            print "     %s %s     (%s,%s)"%(other.name,other.prenom,main.prenom,other.prenom)
                            namecnt+=1
                            merged_ids.append(main.id)
                            self._merge(cr,uid,[main.id,other.id],context=context) 

        name2cnt=0
        ids=self.search(cr,uid,[('active','=','t'),('name','!=',False),('name','!=',''),('donor','=',True),('id','not in',merged_ids)],order="prenom ASC",context=context)
        for main in self.browse(cr,uid,ids,context=context):
            other_ids=self.search(cr,uid,[('active','=','t'),('name','ilike','%%%s%%'%main.name),('donor','=',False)],order="name ASC",context=context)
            if len(other_ids) > 0 :
                for other in self.browse(cr,uid,other_ids,context=context):
                    #match par email+nom+prénom+code postal
                    if main.prenom and other.prenom and main.zip and other.zip:
                        name_ratio = difflib.SequenceMatcher(a=main.name.lower(),b=other.name.lower()).ratio() 
                        prenom_ratio = difflib.SequenceMatcher(a=main.prenom.lower(),b=other.prenom.lower()).ratio() 
                        zip_ratio = difflib.SequenceMatcher(a=main.zip.lower(),b=other.zip.lower()).ratio()
                        if min(name_ratio,prenom_ratio,zip_ratio)> min_ratio:
                            
                            print "MERGING (nom):"
                            print "     %s %s     with"%(main.name,main.prenom)
                            print "     %s %s     (%s,%s)"%(other.name,other.prenom,main.prenom,other.prenom)
                            name2cnt+=1
                            merged_ids.append(main.id)
                            self._merge(cr,uid,[main.id,other.id],context=context) 

            
        print "merged %d partners with email and %d with birthdate and %d with name (phone) and %d with name (zip only)"%(emailcnt,datecnt,namecnt,name2cnt)
        return True
                
            
    
    _defaults = {
                 'code_dp': False,
                 'anonymous': False,
                 'nomail': False,
                 'noemail': False,
                 'total_dons': 0.0,
 #                'nothanks': False,
                 }
    

    def open_gift_view(self,cr,uid,ids,context={}):
        if "search_default_unclosed" in context:
            del(context['search_default_unclosed'])
        context['search_default_closed']=1
        return {
            'type': 'ir.actions.act_window',
            'name': 'Dons',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'nf_fundraising.gift',
            'src_model': 'res.partner',
            'nodestroy': 'true',
            'domain':[('partner_id','=',ids[0])],
#            'target': 'new',
            'context':context,
#            'views': [(False, 'form')],
        }
    def open_attribution_view(self,cr,uid,ids,context={}):
        if "search_default_unclosed" in context:
            del(context['search_default_unclosed'])
        context['search_default_closed']=1
        context['search_default_gbyattribution']=1
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attribution',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'nf_fundraising.gift.attribution',
            'src_model': 'res.partner',
            'nodestroy': 'true',
            'domain':[('partner_id','=',ids[0])],
#            'target': 'new',
            'context':context,
#            'views': [(False, 'form')],
        }
    
    
        
#     def create(self,cr,uid,vals,context={}):
#         if not 'install_mode' in context or not context['install_mode']: 
#             check,double_partner = self.check_doubles(cr,uid,vals,context=context)
#             if not check:
#                 raise osv.except_osv(u"Doublon détecté", u"Vous pouvez choisir d'ignorer les doublons en cochant la case dans l'onglet camps. Le partenaire concerné est : %s %s (id:%s)"%(double_partner.prenom,double_partner.name,double_partner.id))
#             else:
#                 return super(res_partner,self).create(cr,uid,vals,context)
#         else:
#             res=super(res_partner,self).create(cr,uid,vals,context)
#             print "inserted ",res
#             return res
#     def write(self,cr,uid,ids,vals,context={}):
#         
#         if (not 'import_mode' in context or not context['import_mode']) and not 'field_to_read' in context: 
#             for partner in self.browse(cr,uid,ids):
#                 if partner.code_dp != False :
#                     raise osv.except_osv(u"Erreur", u"UImpossible de modifier une entrée provenant de donor perfect\n (donateur : %s)"%(partner.name_get()[0][1]))
#         return super(res_partner,self).write(cr,uid,ids,vals,context)

    
    def import_dp(self,cr,uid,ids,context={}):
        #read all donors
        context['install_mode']=True
        context['import_mode']=True
        import os
        print "Working in ", os.getcwd()
        print "IMPORTING dp.dbf"
        db = dbf.Dbf("nf_fundraising/import/dp.dbf")
#        for key in db.fieldNames:
        partner_ids={}
        max_items=150000
        cnt=0
        for rec in db:
            id=rec['DONOR2'].strip()
            lang_cmp=rec['LANGUAGE']
            lang="fr_FR"
            if lang_cmp=="A" or lang_cmp=="D":
                lang="de_DE"
            elif lang_cmp=="E":
                lang="en_US"
            elif lang_cmp=="I":
                lang="it_IT"
            gender=""
            if rec['SEXE'].lower()=="f":
                gender="f"
            elif rec['SEXE'].lower()=="h" or rec['SEXE'].lower()=="m":
                gender="h" 
            res=cr.execute("SELECT id FROM res_partner WHERE code_dp='%s'"%id.replace("'","\\'"))
            rows=cr.fetchall()
            
            tag_eglise=False
            if "S" in rec['REF_PROV']:
                tag_eglise=True
                
            tag_lettre=False
            if "F" in rec['LETTRE_NV']:
                tag_lettre=True
            
            cat_ids=[]
            if tag_eglise:
                cat_ids.append((4,34))
            if tag_lettre:
                cat_ids.append((4,33))
                
                
            
            active=(tag_eglise or tag_lettre) and (rec['DELETED_DT']==False or rec['DELETED_DT'] is None)
            values={
                    'name':"NO NAME (DP : %s)"%id,
                    'date_naissance':rec['NAIS_DT'],
                    'gender':gender,
                    
                    'nomail':rec['NOMAIL'],
                    'noemail':rec['NOEMAIL'],
                    'anonymous':rec['ANONYME'],
                    'dp_pas_lettre':rec['PAS_LETTRE'],
                    
                    'lang':lang,
                    'active':active,
                    'donor':True,
                    'dp_text':"TYPE: %s\n"%rec['TYPE'],
                    'ignore_double':True,
                    'category_id':cat_ids,
                    }
            if len(rows)>1:
                raise Exception("Too many results searching for donor with ID %s"%id)
            elif len(rows)==0:
                print "No donor %s, creating new"%id
                new_values={'code_dp':id}
                new_values.update(values)
                new_id=self.create(cr,uid,new_values,context=context)
                partner_ids[id]={'id':new_id,'values':values}
            else:
#                print "Updating donor %s (id : %s)"%(id,rows[0][0])
#                self.write(cr,uid,rows[0]['id'],values)
                partner_ids[id]={'id':rows[0][0],'values':values}
            cnt+=1
            if cnt>max_items:
                print "MAX REACHED..."
                break
        print "%d entities reviewed"%cnt
            
            
        res=cr.execute("SELECT * FROM res_country_state")
        states = cr.dictfetchall()
        
        res=cr.execute("SELECT * FROM res_country")
        countries = cr.dictfetchall()
            
        print "IMPORTING DPADD.dbf"
        db = dbf.Dbf("nf_fundraising/import/dpadd.dbf")
        cnt=0
        for rec in db:
            cnt+=1
            if cnt>max_items:
                print "MAX REACHED..."
                break
            id=rec['DONOR'].strip()
            if id not in partner_ids:
#                print "No dp partner for address (DONOR : %s)"%id
                continue
            if not rec['DEL_DT'] is None:
#                print "Address has been deleted"
                continue
            country_id=""
            state_id=""
            for country in countries:
                if rec['COUNTRY'] and country['code'] and country['code'].lower()==rec['COUNTRY'].lower():
                    country_id=country['id']
                    break
            for state in states:
                if rec['ST'] and state['code'] and str(country_id)==str(state['country_id']) and state['code'].lower()==rec['ST'].lower():
                    state_id=state['id']
                    break
            address_values={
                        'name':rec['LNAME'],
                        'prenom':rec['FNAME'],
                        'street':rec['ADD'],
                        'street2':rec['ADD2'],
                        'city':rec['CITY'],
                        'zip':rec['ZIP'],
                        'state_id':state_id,
                        'country_id':country_id,
#                        'create_date':rec['CR_DT'],
#                        'write_date':rec['MOD_DT'],
                        }
            partner_ids[id]['values'].update(address_values)
        print "%d entities reviewed"%cnt

        print "IMPORTING DPPHONE"
        db = dbf.Dbf("nf_fundraising/import/dpphone.dbf")
        cnt=0
        for rec in db:
            cnt+=1
            if cnt>max_items:
                print "MAX REACHED..."
                break
            id=rec['DONOR'].strip()
            if id not in partner_ids:
                print "No dp partner for phone (DONOR : %s)"%id
                continue
            if not rec['DEL_DT'] is None:
#                print "Phone has been deleted"
                continue
            address_values={}
            if rec['PHTYPE']=="EMAIL":
                address_values['email']=rec['PHONE']
            elif rec['PHTYPE']=="FAX":
                address_values['fax']=rec['PHONE']
            elif rec['PHTYPE']=="NATL":
                address_values['mobile']=rec['PHONE']
            elif rec['PHTYPE']=="PRIVÉ":
                address_values['phone']=rec['PHONE']
            elif rec['PHTYPE']=="PROF.":
                address_values['phone']=rec['PHONE']
                
            partner_ids[id]['values'].update(address_values)
            
        print "%d entities reviewed"%cnt

            
        print "IMPORTING DPOTHER"
        db = dbf.Dbf("nf_fundraising/import/dpother.dbf")
        cnt=0
        for rec in db:
            cnt+=1
            if cnt>max_items:
                print "MAX REACHED..."
                break

            id=rec['DONOR'].strip()
            if id not in partner_ids:
                print "No dp partner for dpother (DONOR : %s)"%id
                continue
            if not rec['DEL_DT'] is None:
#                print "Other has been deleted"
                continue
            
            text=partner_ids[id]['values']['dp_text']
            text+=u"DESCR_F: %s\nGROUPE: %s\n"%(rec['DESCR_F'].decode('latin-1'),rec['GROUPE'].decode('latin-1'))
            
            address_values={
                            'dp_text':text
                            }
            partner_ids[id]['values'].update(address_values)
            
        print "%d entities reviewed"%cnt

        print "WRITING FINAL RESULTS"
        cnt=0
        for id in partner_ids:
            cnt+=1
            print "%d of %d\r"%(cnt,len(partner_ids)),
            self.write(cr,uid,partner_ids[id]['id'],partner_ids[id]['values'],context=context)
        print ""
        return True
res_partner()





