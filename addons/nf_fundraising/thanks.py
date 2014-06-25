# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from datetime import date,datetime

class thanks(osv.osv):
    _name = 'nf_fundraising.thanks'
    _columns = {
                'name': fields.char('Nom',required=True),
                'date': fields.date(u"Date",required=True),
                'gift_ids':fields.one2many('nf_fundraising.gift','thanks_id','Dons concernés',ondelete="restrict"),
                'intro_single':fields.text("Intro don unique",translate=True),
                'intro_multiple':fields.text("Intro dons multiples",translate=True),
                'main_text':fields.html("Texte principal",translate=True),
                'signature':fields.html("Signature",translate=True),
                'image':fields.binary('image'),
                'state': fields.selection((("draft","Brouillon"),("listed","Listée"),("printed","Imprimée")),u"État",readonly=True),
                }
    _defaults = {
                 'state':'draft',
                 'intro_single':"Votre don de:",
                 'intro_multiple':"Vos dons de:",
                 'main_text':"""Chers Amis,<br/><br/>Nous tenons à vous dire merci pour votre investissement et votre contribution dans notre fondation. Grâce à vous nous allons pouvoir avancer dans nos différents projets.<br/><br/>C'est grâce à des personnes comme vous que nous pouvons accompagner tous les ans de plus en plus d'enfants et leur permetttre de vivre des moments d'exceptions.<br/><br/>Nous vous remercions de tout notre coeur et ne manquerons pas de vous communiquer l'évolution de nos projets.<br/><br/>Encore merci pour votre générosité et vos prières.<br/><br/>Avec nos fraternelles salutations.""",
                 'signature':"""<b>Fondation le Grain de Blé</b><br/>Paul de Montmollin<br/>Directeur""",

                 }
    
    def open_list(self,cr,uid,ids,context={}):
        context["search_default_unclosed"]=0
        return {
            'type': 'ir.actions.act_window',
            'name': 'Dons liés au remerciement',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'nf_fundraising.gift',
#            'target': 'new',
            'context':context,
            'domain':[('thanks_id','=',ids[0])],
        }        
    
    def _print(self,cr,uid,ids,context={}):
#        print context,ids
        datas = {
            'ids': ids,
            'model': 'nf_fundraising.thanks',
            'form': self.read(cr, uid, ids, context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'nf_fundraising.thanks.report',
            'datas': datas,
            'nodestroy' : True
        }


    def printit(self,cr,uid,ids,context={}):
#         if isinstance(ids, (list, tuple)):
#             print "INSTANCE : ",ids
        self.write(cr,uid,ids,{'state':'printed'},context=context)
        return self._print(cr,uid,ids,context)
    def reprintit(self,cr,uid,ids,context={}):
        return self._print(cr,uid,ids,context)
    
    
thanks()

