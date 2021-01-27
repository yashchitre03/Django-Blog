from django.test import TestCase
from blog.forms import CommentForm, ReportForm


class CommentFormTest(TestCase):

    def testFormIsValid(self):
        """
        tests whether the comment form is valid for text following the constraints.
        """
        content = 'This is a test comment'
        form_data = {'content': content}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def testFormIsNotValid(self):
          """
        tests whether the comment form is invalid for text exceeding the constraints.
        """
        content = 'This is a test comment' * 12
        form_data = {'content': content}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())


class ReportFormTest(TestCase):

    def testFormIsValid(self):
        """
        tests whether the report form is valid for data following the constraints.
        """
        subject = 'Test subject'
        category = 'Bug'
        message = 'This is a test message for a bug report.'
        form_data = {'subject': subject,
                     'category': category, 'message': message}
        form = ReportForm(data=form_data)
        self.assertTrue(form.is_valid())

    def testFormIsNotValid(self):
        """
        tests whether the report form is invalid for data exceeding the constraints.
        """
        subject = 'Test subject' * 12
        category = 'Bug'
        message = 'This is a test message for a bug report.'
        form_data = {'subject': subject,
                     'category': category, 'message': message}
        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())
