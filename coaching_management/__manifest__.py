{
    'name': 'Coaching management system',
    'version': '18.0.0.0',
    'summary': 'Coaching management system that manages the details of the Coaching',
    'description': 'A module to manage college details',
    'author': 'codetrade',
    'website': 'https://codetrade.io',
    'category': 'Education',
    'depends': [],
    'data': [
        #security model
        'security/ir.model.access.csv',    
        #views of model
        'views/student_information_views.xml',
        'views/tutors_details_views.xml',   
        'views/subject_details.views.xml',
        #wizards
        'wizards/onboard_student_views.xml',
    ],
    'installable': True,
    'application': True,
    'license':'LGPL-3',
}
