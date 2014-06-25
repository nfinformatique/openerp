# file: Unicode1.py
# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2004 TINY SPRL. (http://tiny.be) All Rights Reserved.
#                    Fabien Pinckaers <fp@tiny.Be>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import osv, fields
from crm import crm
from wizards import hc_common
from time import strftime



class humancapital_functions(osv.osv):
    _name = 'humancapital.functions'
    _columns = {
        'name': fields.char('Nom',size=64),
        'code': fields.char('Code',size=64),
    }
humancapital_functions()

class humancapital_formations(osv.osv):
    _name = 'humancapital.formations'
    _columns = {
        'name': fields.char('Nom',size=64),
        'code': fields.char('Code',size=64),
    }
humancapital_formations()

class humancapital_workpermits(osv.osv):
    _name = 'humancapital.workpermits'
    _columns = {
        'name': fields.char('Nom',size=64),
        'code': fields.char('Code',size=64),
    }
humancapital_workpermits()

class humancapital_contracttypes(osv.osv):
    _name = 'humancapital.contracttypes'
    _columns = {
        'name': fields.char('Nom',size=64),
        'code': fields.char('Code',size=64),
    }
humancapital_contracttypes()

class humancapital_nationalities(osv.osv):
    _name = 'humancapital.nationalities'
    _columns = {
        'name': fields.char('Nom',size=64),
        'code': fields.char('Code',size=64),
    }
humancapital_nationalities()

class humancapital_regions(osv.osv):
    _name = 'humancapital.regions'
    _columns = {
        'name': fields.char('Nom',size=64),
        'code': fields.char('Code',size=64),
    }
humancapital_regions()

class humancapital_sectors(osv.osv):
    _name = 'humancapital.sectors'
    _columns = {
        'name': fields.char('Nom',size=64),
        'code': fields.char('Code',size=64),
    }
humancapital_sectors()

class humancapital_origin(osv.osv):
    """(NULL)"""
    _name = 'humancapital.origin'
    _columns = {
        'name': fields.char('Nom',size=64),
        'code': fields.char('Code',size=64),
        'description': fields.text('Description'),
    }
humancapital_origin()


class humancapital_languages(osv.osv):
    _name = 'humancapital.languages'
    _columns = {
        'name': fields.char('Nom',size=64),
        'code': fields.char('Code',size=64),
    }
humancapital_languages()


class hc_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {
        'candidate': fields.boolean('Candidate'),
        'advertiser': fields.boolean('Advertiser'),
        'entreprise': fields.boolean('Entreprise'),
    }
    _defaults={
              'candidate': lambda *a: False,
              'advertiser': lambda *a: False,
              'entreprise': lambda *a: False,
              }
hc_partner()

class humancapital_advert(osv.osv):
    """(NULL)"""
    _name = 'humancapital.advert'
    _columns = {
        'name': fields.char('Nom',size=64,required=True),
        'texte': fields.text('texte'),
        'partner_id': fields.many2one('res.partner','Prestataire',required=True),
        'date_from': fields.date('De'),
        'date_to': fields.date('A'),
        'state': fields.selection((('d','Brouillon'),('w','En attente'),('p','Publié'),('u','Non publié'),('c','Fermé')),'Etat'),
        'request_id': fields.many2one('humancapital.request','Demande',required=True)
    }
    _defaults={
              'state': lambda *a: 'd',
              }
    
    def advert_draft(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'd' })
         return True
    def advert_waiting(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'w' })
         return True
    def advert_published(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'p' })
         return True
    def advert_unpublished(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'u' })
         return True
    def advert_closed(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'c' })
         return True
    
humancapital_advert()

    
class humancapital_comparison(osv.osv):
    _name="humancapital.comparison"
    _columns = {
        'name': fields.char('Nom',size=64),
        'description':fields.text("Description"),
                
        'knownlanguages': fields.float('Langues maîtrisées'),
        'approxlanguages': fields.float('Langues connues'),
        'sectors': fields.float('Secteurs'),
        'functions': fields.float('Fonctions'),
        'formations': fields.float('Formations'),
        'workpermits': fields.float('Permis de travail'),
        'contracttypes': fields.float('Types de contrat'),
        'nationalities': fields.float('Nationalités'),
        'age_min': fields.float("Age"),
        'experience': fields.float("Années minimum d'expérience"),
                }
    
    _defaults={
        'knownlanguages': lambda *a: 1,
        'approxlanguages': lambda *a: 1,
        'sectors':lambda *a: 1,
        'functions': lambda *a: 1,
        'formations': lambda *a: 1,
        'workpermits': lambda *a: 1,
        'contracttypes': lambda *a: 1,
        'nationalities': lambda *a: 1,
        'age_min': lambda *a: 1,
        'experience': lambda *a: 1,
              }
        
humancapital_comparison()

class humancapital_request(crm.crm_case, osv.osv):
    """(NULL)"""
    _name = 'humancapital.request'
#    _inherit = 'crm_case'
    _columns = {
        'name': fields.char('Nom',size=64,required=True),
        'partner_id': fields.many2one('res.partner','Entreprise',required=True),
        
        'state': fields.selection((('d','Brouillon'),('o','En cours'),('w','Gagné'),('l','Perdu'),('s','Abandon')),'Etat'),
        
        'knownlanguages': fields.many2many('humancapital.languages','rel_knownlanguagesrequest','request_id','language_id','Langues maîtrisées'),
        'fix_knownlanguages': fields.boolean('Langues maîtrisées nécessaires'),
        'approxlanguages': fields.many2many('humancapital.languages','rel_approxlanguagesrequest','request_id','language_id','Langues connues'),
        'fix_approxlanguages': fields.boolean('Langues connues nécessaires'),
        'sectors': fields.many2many('humancapital.sectors','rel_sectorsrequest','request_id','sector_id','Secteurs'),
        'fix_sectors': fields.boolean('Secteurs nécessaires'),
        'functions': fields.many2many('humancapital.functions','rel_functionsrequest','request_id','function_id','Fonctions'),
        'fix_functions': fields.boolean('Fonctions nécessaires'),
        'formations': fields.many2many('humancapital.formations','rel_formationsrequest','request_id','formation_id','Formations'),
        'fix_formations': fields.boolean('Formations nécessaires'),
        'workpermits': fields.many2many('humancapital.workpermits','rel_workpermitrequest','request_id','workpermit_id','Permis de travail'),
        'fix_workpermits': fields.boolean('Permis de travail nécessaires'),
        'contracttypes': fields.many2many('humancapital.contracttypes','rel_contracttyperequest','request_id','contracttype_id','Types de contrat'),
        'fix_contracttypes': fields.boolean('Types de contrat nécessaires'),
        'nationalities': fields.many2many('humancapital.nationalities','rel_nationalitiesrequest','request_id','nationalitie_id','Nationalités'),
        'fix_nationalities': fields.boolean('Nationalités nécessaires'),
        'age_min': fields.integer("Age minimum"),
        'age_max': fields.integer("Age maximum"),
        'fix_age': fields.boolean('Ages nécessaires'),
        'experience': fields.integer("Années minimum d'expérience"),
        'fix_experience': fields.boolean('Expérience nécessaire'),
        'notes':fields.text("Notes"),
    }
    _defaults={
              'state': lambda *a: 'd',
              }

    def request_draft(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'd' })
         return True
    
    def request_ongoing(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'o' })
         return True
    
    def request_won(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'w' })
         return True
    
    def request_lost(self, cr, uid, ids):
         print "HELLO GUYS"
         self.write(cr, uid, ids, { 'state' : 'l' })
         return True
     
    def request_surrender(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 's' })
         return True

humancapital_request()

#
#class humancapital_quest(crm.crm_case, osv.osv):
#    _name = 'humancapital.quest'
#    #_inherit = 'crm_case'
#    _columns = {
#        'partner_id': fields.many2one('res.partner','Candidat',required=True),
#    }
#humancapital_quest()

class humancapital_linking(osv.osv):
    """(NULL)"""
    _name = 'humancapital.linking'
    _columns = {
        'negotiatedsalary': fields.integer('Salaire Négocié'),
        'commission': fields.float('Commission'),
        'date_conclusion': fields.date('Date du dernier changement d\'état'),
        'request_id': fields.many2one('humancapital.request','Request',required=True),
        'candidate_id': fields.many2one('res.partner','Candidat',required=True),

        'entreprise_id': fields.related('request_id','partner_id',type="many2one",relation='res.partner',string='Entreprise',store=True,readonly=True),
        'state': fields.selection((
                                   ('d','Brouillon'),
                                   ('c','Convoqué'),
                                   ('cs','Abandon à l\'entretien chrysalys'),
                                   ('f','Dossier en préparation'),
                                   ('fs','Dossier envoyé'),
                                   ('fnok','Réponse au dossier négative'),
                                   ('fnokf','Candidat informé'),
                                   ('fok','Réponse positive'),
                                   ('fokf','Candidat informé'),
                                   ('i1','1er entretien en entreprise'),
                                   ('i2','2ème entretien en entreprise'),
                                   ('i3','3ème entretien en entreprise'),
                                   ('ienok','Réponse négative par l\'entreprise'),
                                   ('icnok','Réponse négative du candidat'),
                                   ('iok','Gagné')),
                                'Etat'),
    }
    _defaults={
              'state': lambda *a: 'd',
              }
    
    def linking_d(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'd','date_conclusion': strftime('%Y-%m-%d')})
         return True

    def linking_c(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'c' ,'date_conclusion': strftime('%Y-%m-%d')})
         return True
    def linking_cs(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'cs' })
         return True
    def linking_f(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'f' })
         return True
    def linking_fs(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'fs' })
         return True
    def linking_fnok(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'fnok' })
         return True
    def linking_fnokf(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'fnokf' })
         return True
    def linking_fok(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'fok' })
         return True
    def linking_fokf(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'fokf' })
         return True
    def linking_i1(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'i1' })
         return True
    def linking_i2(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'i2' })
         return True
    def linking_i3(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'i3' })
         return True
    def linking_ienok(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'ienok' })
         return True
    def linking_icnok(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'state' : 'icnok' })
         return True
    def linking_iok(self, cr, uid, ids):
        for linking in self.browse(cr,uid,ids):
            linking.candidate_id.write({'candidate_state':'c'})
        self.write(cr, uid, ids, { 'state' : 'iok' })
        return True
    
    
humancapital_linking()

#class crm_case(osv.osv):
#    _name = 'crm_case'
#    _columns = {
#    }
#crm_case()



class humancapital_entreprise(osv.osv):
    """(NULL)"""
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {
        'agreement': fields.boolean('Agreement'),
        'sectors': fields.many2many('humancapital.sectors','rel_sectorsentreprises','entreprise_id','sector_id','Secteurs'),
        'activityregions': fields.many2many('humancapital.regions','rel_regionsentreprises','entreprise_id','region_id','Régions'),
        'entreprise_state': fields.selection((('p','En prospection'),('a','Active'),('i','Inactive')),'Etat'),
    }
    _defaults={
              'entreprise_state': lambda *a: 'p',
              }

    def entreprise_prospecting(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'entreprise_state' : 'p' })
         return True
    
    def entreprise_active(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'entreprise_state' : 'a' })
         return True
    
    def entreprise_inactive(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'entreprise_state' : 'i' })
         return True
    


humancapital_entreprise()


class humancapital_advertiser(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {
    }
humancapital_advertiser()

            
class humancapital_candidate(osv.osv):
    """(NULL)"""
    _name = 'res.partner'
    _inherit = 'res.partner'
    def fnct_search_index(self, cr, uid, obj, name, args, context):
#    def search(self,cr, user, args, offset=0, limit=None, order=None, context=None, count=False):
        where="a.res_model='res.partner'"
        for a in args:
            if a[0]=="text_search":
                keywords=a[2].replace("'","")
                for keyword in keywords.split(" "):
                    if keyword=="":
                        continue
                    where+=" AND index_content ILIKE '%"+keyword+"%'" 
        query="select distinct res_id from \
                ir_attachment AS a \
                JOIN res_partner AS p ON (p.id=a.res_id) \
            WHERE "+where
        cr.execute(query)
        ids=[]
        for res in cr.dictfetchall():
            ids.append(res['res_id'])
#        print args
#        print query
#        cr.execute()
        
#        for a in args:
#            if a[0]==""
#        res= super(humancapital_candidate,self).search(cr,user,args,offset=offset,limit=limit,order=order,context=context,count=count)
#        print res
        return [('id','in',ids)]
    _columns = {
        'mobile': fields.char('Mobile',size=64,required=True),
        'origin': fields.many2one('humancapital.origin','Origine'),
        'candidate_state': fields.selection((('n','Nouveau'),('q','En recherche'),('c','Employé via Chrysalys'),('t','Employé via Autre'),('s','Abandon')),'Etat'),
        'knownlanguages': fields.many2many('humancapital.languages','rel_knownlanguagescandidate','candidate_id','language_id','Langues maîtrisées'),
        'approxlanguages': fields.many2many('humancapital.languages','rel_approxlanguagescandidate','candidate_id','language_id','Langues connues'),
        'sectors': fields.many2many('humancapital.sectors','rel_sectorscandidate','candidate_id','sector_id','Secteurs'),
        'entreprisesectors': fields.many2many('humancapital.sectors','rel_sectorsentreprise','entreprise_id','sector_id','Secteurs'),
        'functions': fields.many2many('humancapital.functions','rel_functionscandidate','candidate_id','function_id','Fonctions'),
        'formations': fields.many2many('humancapital.formations','rel_formationscandidate','candidate_id','formation_id','Formations'),
        'workpermits': fields.many2many('humancapital.workpermits','rel_workpermitcandidate','candidate_id','workpermit_id','Permis de travail'),
        'contracttypes': fields.many2many('humancapital.contracttypes','rel_contracttypecandidate','candidate_id','contracttype_id','Types de contrat'),
        'nationalities': fields.many2many('humancapital.nationalities','rel_nationalitiescandidate','candidate_id','nationalitie_id','Nationalités'),
        'birthdate': fields.date("Date de naissance"),
        'experience': fields.integer("Années d'expérience"),
        'text_search':fields.function(lambda *a: 0.0, type="char",fnct_search=fnct_search_index,method=True,string="Mots clés"),
    }
    
    _import_columns = ["knownlanguages"]
#    _import_columns = ["knownlanguages","approxlanguages","candidatesectors","entreprisesectors",
#                       "functions","formations","workpermits","contracttypes","nationalities","birthdate","experience"]
    _defaults={
              'candidate_state': lambda *a: 'n',
              }
    
    def candidate_new(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'candidate_state' : 'n' })
         return True
    def candidate_questing(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'candidate_state' : 'q' })
         return True
    def candidate_employedviachrysalys(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'candidate_state' : 'c' })
         return True
    def candidate_employedviaother(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'candidate_state' : 't' })
         return True
    def candidate_surrender(self, cr, uid, ids):
         self.write(cr, uid, ids, { 'candidate_state' : 's' })
         return True
    
    
    
humancapital_candidate()


class humancapital_correspondance(osv.osv):
    _name="humancapital.correspondance"
    _order="score DESC"
    _columns = {
        'request_id': fields.many2one("humancapital.request","Demande"),
        'candidate_id': fields.many2one("res.partner","Candidat"),
        'score': fields.float("Score"),
        }
humancapital_correspondance()


