{
        "name" : "humancapital",
        "version" : "0.1",
        "author" : "NF informatique",
        "website" : "http://www.nfinformatique.ch",
        "category" : "Unknown",
        "description": """ Management of job seeking """,
        "depends" : ['base','crm'],
        "init_xml" : [ ],
        "demo_xml" : [ ],
        "update_xml" : [
                        'humancapital_view.xml',
                        'humancapital_dashboard.xml',
                        'wizards/humancapital_wizards.xml',
                        'workflows/entreprise.xml',
                        'workflows/request.xml',
                        'workflows/advert.xml',
                        'workflows/candidate.xml',
                        'workflows/linking.xml',
                        'security/hc_security.xml',
                        ],
        "installable": True
}