from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class TutorsDetails(models.Model):
    _name = "tutors.details"
    _description = "This class stores the information of Tutors."

    tutors_name = fields.Char(string="Student Name")
    last_name = fields.Char(string="Tutors Name")
    tutors_image = fields.Image(string="", max_height=0, max_weidth=0)
    tutors_class = fields.Selection([('10th', '10th'), ('11th', '11th'), ('12th', '12th')], string="Class")
    tutor_unique_id = fields.Integer(string="Unique Id")
    # student_associated = fields.Many2many('student.details')
    tutors_email = fields.Char(string="Email Id")
    tutors_phone = fields.Char(string = "Phone No.")
    tutors_gender = fields.Selection([("male","Male"),("female","Female"),("other","other")],string="Gender")
    tutors_salary = fields.Float(string="Salary of Tutors")
    tutors_age = fields.Integer(string="Tutors Age")
    birth_date = fields.Date(string="Date Of Birth")
    students = fields.One2many("student.information", inverse_name='teachers')
    _sql_constraints = [
    ('check_age', 'CHECK(tutors_age >= 18 AND tutors_age <= 100)', 'Age must be between 18 and 100.')
]
    @api.constrains('tutors_email')
    def check_email(self):
        for record in self:
            if record.tutors_email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.tutors_email):
                raise ValidationError("Invalid email format")
        
    @api.constrains('tutors_phone')
    def check_phone(self):
            for record in self:
                if record.tutors_phone and not re.match(r"(0|91)?[6-9][0-9]{9}", record.tutors_phone):
                    raise ValidationError("Please enter a valid phone number")
                
    @api.onchange('tutors_class')
    def onchange_salary_of_tutors(self):
         if self.tutors_class == "10th":
              self.tutors_salary = 500000
         elif self.tutors_class == "11th":
              self.tutors_salary = 1000000
         elif self.tutors_class == "12th":
              self.tutors_salary = 1200000
         else:
              self.tutors_salary = 0 
    
    @api.model
    def create(self, vals):
         if "tutor_unique_id" in vals:
            existing_record = self.env['tutors.details'].search([("tutor_unique_id", "=", vals["tutor_unique_id"])])
            if existing_record:
                raise ValidationError("A teacher with same record is exists.")
            return super(TutorsDetails, self).create(vals)
