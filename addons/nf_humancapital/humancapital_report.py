# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from dateutil.relativedelta import relativedelta
from osv import fields,osv
import tools


class humancapital_report(osv.osv):
    """ Human Capital Request Report """
    _name = "humancapital.request.report"
    _auto = False
    _description = "Human Capital Request Report "
    
    _columns = {
        'name': fields.char('Nom', size=64, required=False, readonly=True),
        'nbr': fields.integer('# of Cases', readonly=True),
        'linkings': fields.integer('# of Linkings', readonly=True),
        'correspondances': fields.integer('# of Correspondances', readonly=True),
        'state': fields.selection((('d','Brouillon'),('o','En cours'),('w','Gagné'),('l','Perdu'),('s','Abandon')),'Etat'),
        'partner_id':fields.many2one('res.partner', 'User', readonly=True),
        'create_date':fields.datetime("Date de création"),
    }
    def init(self, cr):

        """
            HumanCapital request report
            @param cr: the current row, from the database cursor
        """
        tools.drop_view_if_exists(cr, 'humancapital_request_report')
        cr.execute("""
            CREATE OR REPLACE VIEW humancapital_request_report AS (
                SELECT
                    date_trunc('day',r.create_date) AS create_date,
                    id,
                    r.state AS state,
                    r.name AS name,
                    r.partner_id AS partner_id,
                    (SELECT count(id) FROM humancapital_linking WHERE request_id=r.id) AS linkings,
                    (SELECT count(id) FROM humancapital_correspondance WHERE request_id=r.id) AS correspondances,
                    1 as nbr
                FROM
                    humancapital_request r
            )""")

humancapital_report()





class humancapital_linkings_report(osv.osv):
    """ Human Capital Request Report """
    _name = "humancapital.linking.report"
    _auto = False
    _description = "Human Capital Linkings Report "
    
    _columns = {
        'nbr': fields.integer('# Nbr of linkings', readonly=True),
        'candidate_id':fields.many2one('res.partner', 'Candidat', readonly=True),        
        'request_id':fields.many2one('humancapital.request', 'Demande', readonly=True),
        'create_date':fields.datetime("Date de création"),        
        'date_conclusion':fields.datetime("Date de conclusion"),        
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
    def init(self, cr):

        """
            HumanCapital linkings report
            @param cr: the current row, from the database cursor
        """
        tools.drop_view_if_exists(cr, 'humancapital_linking_report')
        cr.execute("""
            CREATE OR REPLACE VIEW humancapital_linking_report AS (
                SELECT
                    date_trunc('day',l.create_date) AS create_date,
                    date_trunc('day',l.date_conclusion) AS date_conclusion,
                    id,
                    l.state AS state,
                    l.candidate_id AS candidate_id,
                    l.request_id AS request_id,
                    1 as nbr
                FROM
                    humancapital_linking l
            )""")

humancapital_linkings_report()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: