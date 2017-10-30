from django import forms
from leave_application.models import CurrentLeaveRequest, LeavesCount
from django.contrib.auth.models import User
from user_app.models import Administration
from leave_application.helpers import get_object_or_none, count_work_days
from django.db.models import Q
from calender.models import RestrictedHoliday


import datetime

class LeaveForm(forms.Form):

    # def __init__(self, *args, **kwargs):
    #     super(LeaveForm, self).__init__(*args, **kwargs)
    start_date = forms.DateField(label='From', widget=forms.widgets.DateInput())
    end_date = forms.DateField(label='Upto', widget=forms.widgets.DateInput())
    leave_address = forms.CharField(label='Leave Address',
                                    widget=forms.TextInput(attrs={
                                                                    'placeholder': 'Address of leave'
                                                                 }
                                                          ),
                                    max_length=100, required=False)
    purpose = forms.CharField(label='Purpose', widget=forms.Textarea, max_length=300)

    def not_dates_valid(self, user):
        from leave_application.models import Leave
        start_date, end_date = self.cleaned_data['start_date'], self.cleaned_data['end_date']

        objects = Leave.objects.filter(
            Q(applicant = user)
            & Q(start_date__year = start_date.year)
            & ~Q(status = 'rejected')
        )
        # print(objects)
        if objects:
            for obj in objects:
                s_date = obj.start_date
                e_date = obj.end_date
                if max(start_date, s_date) <= min(end_date, e_date):
                    return [s_date, e_date]
        return False

    def clean(self):
        # print(self.cleaned_data)
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if not (start_date or end_date):
            raise forms.ValidationError({'start_date': ['Dates must not be empty']})

        today = datetime.date.today()

        if start_date > end_date or start_date < today or end_date < today \
           or [start_date.year, end_date.year] != [today.year, today.year]:

           raise forms.ValidationError({'start_date': ['Past Dates or next year dates not allowed',]})

        type_of_leave = self.cleaned_data.get('type_of_leave')
        if type_of_leave == 'restricted':
            tmp_date = start_date
            restricted_holidays = RestrictedHoliday.objects.filter(date__gte=today)
            # print(restricted_holidays)
            while tmp_date <= end_date:
                if not restricted_holidays.filter(date=tmp_date):
                    raise forms.ValidationError({'type_of_leave': ['Choose a restricted holiday']})
                tmp_date = tmp_date + datetime.timedelta(days=1)

        valid_dates = self.not_dates_valid(self.user)
        if valid_dates:
            valid_dates[0] = valid_dates[0].strftime('%d/%m/%Y')
            valid_dates[1] = valid_dates[1].strftime('%d/%m/%Y')
            raise forms.ValidationError({'start_date': ['You already have a leave from {} to {}, overlapping '
                                        'with the requested leave dates' \
                                        .format(valid_dates[0], valid_dates[1])]})

        if type_of_leave == 'vacation':

            vac_start_date_sum = datetime.date(today.year, 5, 1)
            vac_end_date_sum = datetime.date(today.year, 7, 30)
            vac_start_date_win = datetime.date(today.year, 12, 1)
            vac_end_date_win = datetime.date(today.year, 12, 31)
            if not ((start_date >= vac_start_date_sum and end_date <= vac_end_date_sum) or (start_date >= vac_start_date_win and end_date <= vac_end_date_win)):
                raise forms.ValidationError({'type_of_leave': ['Vacation Leave can only be taken in vacation time']})

    # def get_date_format(self, )

    def user_on_leave(self, rep_user):

        if rep_user:
            rep_user = User.objects.get(username=rep_user)
            valid_dates = self.not_dates_valid(rep_user)
            if valid_dates:
                valid_dates[0] = valid_dates[0].strftime('%d/%m/%Y')
                valid_dates[1] = valid_dates[1].strftime('%d/%m/%Y')
                print('hello')
                raise forms.ValidationError({'admin_rep': ['Mr/Mrs/Ms {} {} is/might be on leave between {} and {}' \
                                             .format(rep_user.first_name,
                                                     rep_user.last_name,
                                                     valid_dates[0], valid_dates[1])]})


class FacultyLeaveForm(LeaveForm):

    from leave_application.models import Constants as cts
    LEAVE_CHOICES = cts.LEAVE_TYPE
    type_of_leave = forms.CharField(widget=forms.Select(choices=LEAVE_CHOICES))
    station_leave = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')

        try:
            ALL_USERS = User.objects.all()
            USER_CHOICES = list((user.username, '{} {}'.format(user.first_name, user.last_name)) \
                                 for user in ALL_USERS \
                                 if user.extrainfo.user_type == 'faculty' \
                                 and user != self.user)
        except Exception as e:
            USER_CHOICES = []
        super(FacultyLeaveForm, self).__init__(*args, **kwargs)
        self.fields['acad_rep'] = forms.CharField(label = 'Academic Responsibility Assigned To',
                                   widget=forms.Select(choices=USER_CHOICES))
        self.fields['admin_rep'] = forms.CharField(label = 'Administrative Responsibility Assigned To',
                                    widget=forms.Select(choices=USER_CHOICES))


    def clean(self):
        # print(self.cleaned_data)
        super(FacultyLeaveForm, self).clean()

        admin_rep = self.cleaned_data.get('admin_rep', None)
        acad_rep = self.cleaned_data.get('acad_rep', None)

        # if self.user_on_leave(admin_rep)
        self.user_on_leave(admin_rep)
        self.user_on_leave(acad_rep)

        type_of_leave = self.cleaned_data.get('type_of_leave')
        if not type_of_leave:
            raise forms.ValidationError({'type_of_leave': ['Please Provide the type of leave.']})
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        today = datetime.date.today()

        request_leaves = count_work_days(start_date, end_date)

        # if type_of_leave == 'vacation':
        #
        #     vac_start_date = datetime.date(today.year, 5, 1)
        #     vac_end_date = datetime.date(today.year, 7, 30)
        #
        #     if not (start_date >= vac_start_date and end_date <= vac_end_date):
        #         raise forms.ValidationError({'start_date': ['Vacation Leave can only be taken in vacation time']})

        leave_object = LeavesCount.objects.filter(user=self.user).first()

        remaining_leaves = getattr(leave_object, type_of_leave)
        # TODO: User must not have leaves in between start_date and end_date

        if remaining_leaves < request_leaves:
            raise forms.ValidationError({'type_of_leave': ['You have {} remaining {} leaves'.format(remaining_leaves,
                                                                                                    type_of_leave)]})

        if self.cleaned_data['station_leave'] and not self.cleaned_data['leave_address']:
            raise forms.ValidationError({'station_leave': ['Fill Leave Address, if going Out of station']})

        return self.cleaned_data


class StaffLeaveForm(LeaveForm):

    from leave_application.models import Constants as cts
    LEAVE_CHOICE = cts.LEAVE_TYPE
    type_of_leave = forms.CharField(widget=forms.Select(choices=LEAVE_CHOICE))
    station_leave = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')

        super(StaffLeaveForm, self).__init__(*args, **kwargs)

        try:
            USER_CHOICES = tuple((user.username, '{} {}'.format(user.first_name, user.last_name)) \
                                  for user in User.objects.all() \
                                  if user.extrainfo.user_type == 'staff'\
                                  and user != self.user)
        except:
            USER_CHOICES = []

        self.fields['admin_rep'] = forms.CharField(label='Administrative Responsibility Assigned To',
                                        widget=forms.Select(choices=USER_CHOICES))


    def clean(self):

        super(StaffLeaveForm, self).clean()
        admin_rep = self.cleaned_data['admin_rep']
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        today = datetime.datetime.today()

        self.user_on_leave(admin_rep)
        # if start_date > end_date or start_date < today or end_date < today:
        #     raise forms.ValidationError('Invalid Dates')

        if self.cleaned_data['station_leave'] and not self.cleaned_data['leave_address']:
            raise forms.ValidationError({'station_leave': ['Fill Leave Address, if going Out of station']})

        type_of_leave = self.cleaned_data.get('type_of_leave')
        leave_object = LeavesCount.objects.filter(user=self.user).first()#
        request_leaves = count_work_days(start_date, end_date)
        remaining_leaves = getattr(leave_object, type_of_leave)
        # TODO: User must not have leaves in between start_date and end_date

        # type_of_leave = self.cleaned_data.get('type_of_leave')

        if remaining_leaves < request_leaves:
            raise forms.ValidationError({'type_of_leave': ['You have {} remaining {} leaves'.format(remaining_leaves,
                                                                                                    type_of_leave)]})

        return self.cleaned_data


class StudentLeaveForm(LeaveForm):

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')

        super(StudentLeaveForm, self).__init__(*args, **kwargs)

    # def clean(self):
        # super(StudentLeaveForm, self).clean()
