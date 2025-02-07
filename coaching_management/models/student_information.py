from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class StudentInformation(models.Model):
    _name = "student.information"
    _description = "This class stores the information of student."
    _rec_name = "student_name"

    student_name = fields.Char(string="Student Name")
    teachers = fields.Many2one('tutors.details')
    last_name = fields.Char(string="Student Last Name")
    unique_id = fields.Char(string="Unique Enrollment Number")
    student_class = fields.Selection([('10', '10th'), ('11', '11th'), ('12', '12th')], string="Class")
    student_email = fields.Char(string="Email Id")
    student_phone = fields.Char(string = "Phone No.")
    student_image = fields.Image(string="", max_height=0, max_weidth=0)
    student_gender = fields.Selection([("male","Male"),("female","Female"),("other","Other")],string="Gender")
    age = fields.Integer(string="Age",compute= "_compute_age")
    student_fees = fields.Integer(string="Student Fees") 
    birth_date = fields.Date(string="Date Of Birth")
    subject_associate = fields.Many2many(comodel_name="subject.details")
    _sql_constraints = [('unique_id', 'unique(unique_id)', "The id should be unique for each student")]
    onboarding_status = fields.Selection(
        [('confirmed', 'Confirmed'), ('unconfirmed', 'Unconfirmed')],
        string="Onboarding Status",
        compute="_compute_onboarding_status"
    )
    confirm_date = fields.Date(string = "Confirmation Date")


    @api.constrains('student_email')
    def check_email(self):
        for record in self:
            if record.student_email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.student_email):
                raise ValidationError("Invalid email format")
        
    @api.constrains('student_phone')
    def check_phone(self):
            for record in self:
                if record.student_phone and not re.match(r"(0|91)?[6-9][0-9]{9}", record.student_phone):
                    raise ValidationError("Please enter a valid phone number")
    
    @api.onchange('student_class')
    def onchange_fees_of_student(self):
         if self.student_class == "10":
              self.student_fees = 10000
         elif self.student_class == "11":
              self.student_fees = 150000
         elif self.student_class == "12":
              self.student_fees = 20000
         else:
              self.student_fees = 0

    
    @api.depends('birth_date')
    def _compute_age(self):
        """Calculate age using birth_date and current date with validations."""
        for student in self:
            if student.birth_date:
                today = fields.Date.today()
                birth_date = student.birth_date
                if birth_date > today:
                    raise ValidationError("Birth date cannot be in the future.")
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                student.age = age
            else:
                student.age = 0

          
        # New computed field for onboarding status

    @api.depends('confirm_date')
    def _compute_onboarding_status(self):
        for record in self:
            record.onboarding_status = 'confirmed' if record.confirm_date else 'unconfirmed'
    

    def action_verify_wizard_button(self):
        return {
            'name': 'Verify Students Onboarding',
            'type': 'ir.actions.act_window',
            'res_model': 'onboard.student',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_student_ids': [(6, 0, self.ids)]},
        }
