from odoo import models, fields, api
from odoo.exceptions import UserError

class OnboardStudents(models.TransientModel):
    _name = 'onboard.student'
    _description = 'Wizard to Confirm Student Onboarding if Fees are Set'
    _rec_name = "student_ids"

    student_ids = fields.Many2many('student.information', string="Students to Onboard")

    def action_confirm_onboarding(self):
        """Confirm onboarding for students with non-null fees."""
        if not self.student_ids:
            raise UserError("Please select at least one student.")

        for student in self.student_ids:
            if student.student_fees:
                student.write({
                    'confirm_date': fields.Date.today(),
                })
            else:
                raise UserError(f"Student '{student.student_name}' has no fees set. Cannot confirm onboarding.")
        
        return {'type': 'ir.actions.act_window_close'}
