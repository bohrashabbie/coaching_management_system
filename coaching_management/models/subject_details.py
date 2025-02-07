from odoo import fields, models

class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "This class is used to assign the subject to the student"

    subject = fields.Selection([('Physics', '"PHYSICS'), ('Chemestry', "CHEMESTRY"), ("math", "MATHS"), ("science", "SCIENCE(complete)"), ("english", "ENGLISH"), ("social science", "SOCIAL SCIENCE")])
    class_subject = fields.Selection([('10th', '10th'), ('11th', '11th'), ('12th', '12th')], string="Subject as per classes")

