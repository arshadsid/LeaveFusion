from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import csv

from eis import admin
from user_app.models import ExtraInfo
from .models import *
from .forms import *

# Create your views here

# Main profile landing view
def profile(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print (user)
    pf = user.unique_id

    form = ConfrenceForm()

    journal = emp_research_papers.objects.filter(pf_no=pf, rtype='Journal').order_by('-year')
    conference = emp_research_papers.objects.filter(pf_no=pf, rtype='Conference').order_by('-year')
    books = emp_published_books.objects.filter(pf_no=pf).order_by('-pyear')
    projects = emp_research_projects.objects.filter(pf_no=pf).order_by('-start_date')
    consultancy = emp_consultancy_projects.objects.filter(pf_no=pf).order_by('-date_entry')
    patents = emp_patents.objects.filter(pf_no=pf).order_by('-date_entry')
    techtransfers = emp_techtransfer.objects.filter(pf_no=pf).order_by('-date_entry')
    mtechs = emp_mtechphd_thesis.objects.filter(pf_no=pf, degree_type=1).order_by('-date_entry')
    phds = emp_mtechphd_thesis.objects.filter(pf_no=pf, degree_type=2).order_by('-date_entry')
    fvisits = emp_visits.objects.filter(pf_no=pf, v_type=2).order_by('-entry_date')
    countries = {
        'AF': 'Afghanistan',
        'AX': 'Aland Islands',
        'AL': 'Albania',
        'DZ': 'Algeria',
        'AS': 'American Samoa',
        'AD': 'Andorra',
        'AO': 'Angola',
        'AI': 'Anguilla',
        'AQ': 'Antarctica',
        'AG': 'Antigua And Barbuda',
        'AR': 'Argentina',
        'AM': 'Armenia',
        'AW': 'Aruba',
        'AU': 'Australia',
        'AT': 'Austria',
        'AZ': 'Azerbaijan',
        'BS': 'Bahamas',
        'BH': 'Bahrain',
        'BD': 'Bangladesh',
        'BB': 'Barbados',
        'BY': 'Belarus',
        'BE': 'Belgium',
        'BZ': 'Belize',
        'BJ': 'Benin',
        'BM': 'Bermuda',
        'BT': 'Bhutan',
        'BO': 'Bolivia',
        'BA': 'Bosnia And Herzegovina',
        'BW': 'Botswana',
        'BV': 'Bouvet Island',
        'BR': 'Brazil',
        'IO': 'British Indian Ocean Territory',
        'BN': 'Brunei Darussalam',
        'BG': 'Bulgaria',
        'BF': 'Burkina Faso',
        'BI': 'Burundi',
        'KH': 'Cambodia',
        'CM': 'Cameroon',
        'CA': 'Canada',
        'CV': 'Cape Verde',
        'KY': 'Cayman Islands',
        'CF': 'Central African Republic',
        'TD': 'Chad',
        'CL': 'Chile',
        'CN': 'China',
        'CX': 'Christmas Island',
        'CC': 'Cocos (Keeling) Islands',
        'CO': 'Colombia',
        'KM': 'Comoros',
        'CG': 'Congo',
        'CD': 'Congo, Democratic Republic',
        'CK': 'Cook Islands',
        'CR': 'Costa Rica',
        'CI': 'Cote D\'Ivoire',
        'HR': 'Croatia',
        'CU': 'Cuba',
        'CY': 'Cyprus',
        'CZ': 'Czech Republic',
        'DK': 'Denmark',
        'DJ': 'Djibouti',
        'DM': 'Dominica',
        'DO': 'Dominican Republic',
        'EC': 'Ecuador',
        'EG': 'Egypt',
        'SV': 'El Salvador',
        'GQ': 'Equatorial Guinea',
        'ER': 'Eritrea',
        'EE': 'Estonia',
        'ET': 'Ethiopia',
        'FK': 'Falkland Islands (Malvinas)',
        'FO': 'Faroe Islands',
        'FJ': 'Fiji',
        'FI': 'Finland',
        'FR': 'France',
        'GF': 'French Guiana',
        'PF': 'French Polynesia',
        'TF': 'French Southern Territories',
        'GA': 'Gabon',
        'GM': 'Gambia',
        'GE': 'Georgia',
        'DE': 'Germany',
        'GH': 'Ghana',
        'GI': 'Gibraltar',
        'GR': 'Greece',
        'GL': 'Greenland',
        'GD': 'Grenada',
        'GP': 'Guadeloupe',
        'GU': 'Guam',
        'GT': 'Guatemala',
        'GG': 'Guernsey',
        'GN': 'Guinea',
        'GW': 'Guinea-Bissau',
        'GY': 'Guyana',
        'HT': 'Haiti',
        'HM': 'Heard Island & Mcdonald Islands',
        'VA': 'Holy See (Vatican City State)',
        'HN': 'Honduras',
        'HK': 'Hong Kong',
        'HU': 'Hungary',
        'IS': 'Iceland',
        'IN': 'India',
        'ID': 'Indonesia',
        'IR': 'Iran, Islamic Republic Of',
        'IQ': 'Iraq',
        'IE': 'Ireland',
        'IM': 'Isle Of Man',
        'IL': 'Israel',
        'IT': 'Italy',
        'JM': 'Jamaica',
        'JP': 'Japan',
        'JE': 'Jersey',
        'JO': 'Jordan',
        'KZ': 'Kazakhstan',
        'KE': 'Kenya',
        'KI': 'Kiribati',
        'KR': 'Korea',
        'KW': 'Kuwait',
        'KG': 'Kyrgyzstan',
        'LA': 'Lao People\'s Democratic Republic',
        'LV': 'Latvia',
        'LB': 'Lebanon',
        'LS': 'Lesotho',
        'LR': 'Liberia',
        'LY': 'Libyan Arab Jamahiriya',
        'LI': 'Liechtenstein',
        'LT': 'Lithuania',
        'LU': 'Luxembourg',
        'MO': 'Macao',
        'MK': 'Macedonia',
        'MG': 'Madagascar',
        'MW': 'Malawi',
        'MY': 'Malaysia',
        'MV': 'Maldives',
        'ML': 'Mali',
        'MT': 'Malta',
        'MH': 'Marshall Islands',
        'MQ': 'Martinique',
        'MR': 'Mauritania',
        'MU': 'Mauritius',
        'YT': 'Mayotte',
        'MX': 'Mexico',
        'FM': 'Micronesia, Federated States Of',
        'MD': 'Moldova',
        'MC': 'Monaco',
        'MN': 'Mongolia',
        'ME': 'Montenegro',
        'MS': 'Montserrat',
        'MA': 'Morocco',
        'MZ': 'Mozambique',
        'MM': 'Myanmar',
        'NA': 'Namibia',
        'NR': 'Nauru',
        'NP': 'Nepal',
        'NL': 'Netherlands',
        'AN': 'Netherlands Antilles',
        'NC': 'New Caledonia',
        'NZ': 'New Zealand',
        'NI': 'Nicaragua',
        'NE': 'Niger',
        'NG': 'Nigeria',
        'NU': 'Niue',
        'NF': 'Norfolk Island',
        'MP': 'Northern Mariana Islands',
        'NO': 'Norway',
        'OM': 'Oman',
        'PK': 'Pakistan',
        'PW': 'Palau',
        'PS': 'Palestinian Territory, Occupied',
        'PA': 'Panama',
        'PG': 'Papua New Guinea',
        'PY': 'Paraguay',
        'PE': 'Peru',
        'PH': 'Philippines',
        'PN': 'Pitcairn',
        'PL': 'Poland',
        'PT': 'Portugal',
        'PR': 'Puerto Rico',
        'QA': 'Qatar',
        'RE': 'Reunion',
        'RO': 'Romania',
        'RU': 'Russian Federation',
        'RW': 'Rwanda',
        'BL': 'Saint Barthelemy',
        'SH': 'Saint Helena',
        'KN': 'Saint Kitts And Nevis',
        'LC': 'Saint Lucia',
        'MF': 'Saint Martin',
        'PM': 'Saint Pierre And Miquelon',
        'VC': 'Saint Vincent And Grenadines',
        'WS': 'Samoa',
        'SM': 'San Marino',
        'ST': 'Sao Tome And Principe',
        'SA': 'Saudi Arabia',
        'SN': 'Senegal',
        'RS': 'Serbia',
        'SC': 'Seychelles',
        'SL': 'Sierra Leone',
        'SG': 'Singapore',
        'SK': 'Slovakia',
        'SI': 'Slovenia',
        'SB': 'Solomon Islands',
        'SO': 'Somalia',
        'ZA': 'South Africa',
        'GS': 'South Georgia And Sandwich Isl.',
        'ES': 'Spain',
        'LK': 'Sri Lanka',
        'SD': 'Sudan',
        'SR': 'Suriname',
        'SJ': 'Svalbard And Jan Mayen',
        'SZ': 'Swaziland',
        'SE': 'Sweden',
        'CH': 'Switzerland',
        'SY': 'Syrian Arab Republic',
        'TW': 'Taiwan',
        'TJ': 'Tajikistan',
        'TZ': 'Tanzania',
        'TH': 'Thailand',
        'TL': 'Timor-Leste',
        'TG': 'Togo',
        'TK': 'Tokelau',
        'TO': 'Tonga',
        'TT': 'Trinidad And Tobago',
        'TN': 'Tunisia',
        'TR': 'Turkey',
        'TM': 'Turkmenistan',
        'TC': 'Turks And Caicos Islands',
        'TV': 'Tuvalu',
        'UG': 'Uganda',
        'UA': 'Ukraine',
        'AE': 'United Arab Emirates',
        'GB': 'United Kingdom',
        'US': 'United States',
        'UM': 'United States Outlying Islands',
        'UY': 'Uruguay',
        'UZ': 'Uzbekistan',
        'VU': 'Vanuatu',
        'VE': 'Venezuela',
        'VN': 'Viet Nam',
        'VG': 'Virgin Islands, British',
        'VI': 'Virgin Islands, U.S.',
        'WF': 'Wallis And Futuna',
        'EH': 'Western Sahara',
        'YE': 'Yemen',
        'ZM': 'Zambia',
        'ZW': 'Zimbabwe'
    }
    ivisits = emp_visits.objects.filter(pf_no=pf, v_type=1).order_by('-entry_date')
    for fvisit in fvisits:
        fvisit.countryfull = countries[fvisit.country]
    consymps = emp_confrence_organised.objects.filter(pf_no=pf).order_by('-date_entry')
    awards = emp_achievement.objects.filter(pf_no=pf).order_by('-date_entry')
    talks = emp_expert_lectures.objects.filter(pf_no=pf).order_by('-date_entry')
    chairs = emp_session_chair.objects.filter(pf_no=pf).order_by('-date_entry')
    keynotes = emp_keynote_address.objects.filter(pf_no=pf).order_by('-date_entry')
    events = emp_event_organized.objects.filter(pf_no=pf).order_by('-date_entry')
    y=[]
    for r in range(1995, (datetime.datetime.now().year + 1)):
        y.append(r)

    context = {'user': user,
               'pf':pf,
               'journal':journal,
               'conference': conference,
               'books': books,
               'projects': projects,
               'form':form,
               'consultancy':consultancy,
               'patents':patents,
               'techtransfers':techtransfers,
               'mtechs':mtechs,
               'phds':phds,
               'fvisits':fvisits,
               'ivisits': ivisits,
               'consymps':consymps,
               'awards':awards,
               'talks':talks,
               'chairs':chairs,
               'keynotes':keynotes,
               'events':events,
               'year_range':y,
               }
    return render(request, 'eis/eisModule/profile.html', context)


# Views for deleting the EIS fields
def achievementDelete(request, pk):
    instance = emp_achievement.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_confrence_organisedDelete(request, pk):
    instance = emp_confrence_organised.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_consultancy_projectsDelete(request, pk):
    instance = emp_consultancy_projects.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_event_organizedDelete(request, pk):
    instance = emp_event_organized.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_expert_lecturesDelete(request, pk):
    instance = emp_expert_lectures.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_keynote_addressDelete(request, pk):
    instance = emp_keynote_address.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_mtechphd_thesisDelete(request, pk):
    instance = emp_mtechphd_thesis.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_patentsDelete(request, pk):
    instance = emp_patents.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_published_booksDelete(request, pk):
    instance = emp_published_books.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_research_papersDelete(request, pk):
    instance = emp_research_papers.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_research_projectsDelete(request, pk):
    instance = emp_research_projects.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_session_chairDelete(request, pk):
    instance = emp_session_chair.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_techtransferDelete(request, pk):
    instance = emp_techtransfer.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')

def emp_visitsDelete(request, pk):
    instance = emp_visits.objects.get(pk=pk)
    instance.delete()
    return redirect('eis:profile')


# Views for inserting fields in EIS
def pg_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    if (request.POST.get('pg_id')==None or request.POST.get('pg_id')==""):
        eis = emp_mtechphd_thesis()
    else:
        eis = get_object_or_404(emp_mtechphd_thesis, id=request.POST.get('pg_id'))
    eis.pf_no = pf
    print(eis.pf_no)
    print("--------------ID-----------: "+request.POST.get('pg_id'))
    eis.title = request.POST.get('title')
    print(eis.title)
    eis.s_year = request.POST.get('s_year')
    print(eis.s_year)
    eis.supervisors = request.POST.get('sup')
    print(eis.supervisors)
    eis.rollno = request.POST.get('roll')
    print(eis.rollno)
    eis.s_name = request.POST.get('name')
    print(eis.s_name)

    eis.save()
    return redirect('eis:profile')

def phd_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    if (request.POST.get('phd_id')==None or request.POST.get('phd_id')==""):
        eis = emp_mtechphd_thesis()
    else:
        eis = get_object_or_404(emp_mtechphd_thesis, id=request.POST.get('phd_id'))
    eis.pf_no = pf
    eis.degree_type = 2
    print(eis.pf_no)
    eis.title = request.POST.get('title')
    print(eis.title)
    eis.s_year = request.POST.get('s_year')
    print(eis.s_year)
    eis.supervisors = request.POST.get('sup')
    print(eis.supervisors)
    eis.rollno = request.POST.get('roll')
    print(eis.rollno)
    eis.s_name = request.POST.get('name')
    print(eis.s_name)

    eis.save()
    return redirect('eis:profile')

def fvisit_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    if (request.POST.get('fvisit_id')==None or request.POST.get('fvisit_id')==""):
        eis = emp_visits()
    else:
        eis = get_object_or_404(emp_visits, id=request.POST.get('fvisit_id'))
    eis.pf_no = pf
    eis.v_type = 2
    print(eis.pf_no)
    eis.country = request.POST.get('country').upper()
    print(eis.country)
    eis.place = request.POST.get('place')
    print(eis.place)
    eis.purpose = request.POST.get('purpose')
    print(eis.purpose)
    try:
        eis.start_date = datetime.datetime.strptime(request.POST.get('start'), "%B %d, %Y")
        print(eis.start_date)
    except:
        eis.start_date = datetime.datetime.strptime(request.POST.get('start'), "%b. %d, %Y")
        print(eis.start_date)
    try:
        eis.end_date = datetime.datetime.strptime(request.POST.get('end'), "%B %d, %Y")
        print(eis.end_date)
    except:
        eis.end_date = datetime.datetime.strptime(request.POST.get('end'), "%b. %d, %Y")

    eis.save()
    return redirect('eis:profile')

def ivisit_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    if (request.POST.get('ivisit_id')==None or request.POST.get('ivisit_id')==""):
        eis = emp_visits()
    else:
        eis = get_object_or_404(emp_visits, id=request.POST.get('ivisit_id'))
    eis.pf_no = pf
    eis.v_type = 1
    print(eis.pf_no)
    eis.country = request.POST.get('country')
    print(eis.country)
    eis.place = request.POST.get('place')
    print(eis.place)
    eis.purpose = request.POST.get('purpose')
    print(eis.purpose)
    try:
        eis.start_date = datetime.datetime.strptime(request.POST.get('start'), "%B %d, %Y")
        print(eis.start_date)
    except:
        eis.start_date = datetime.datetime.strptime(request.POST.get('start'), "%b. %d, %Y")
        print(eis.start_date)
    try:
        eis.end_date = datetime.datetime.strptime(request.POST.get('end'), "%B %d, %Y")
        print(eis.end_date)
    except:
        eis.end_date = datetime.datetime.strptime(request.POST.get('end'), "%b. %d, %Y")

    eis.save()
    return redirect('eis:profile')

def journal_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_research_papers()
    eis.pf_no = pf
    eis.rtype = 'Journal'
    print(eis.pf_no)
    eis.authors = request.POST.get('authors')
    print('Authors: '+eis.authors)
    eis.title_paper = request.POST.get('title')
    print('Title: '+eis.title_paper)
    eis.name_journal = request.POST.get('name')
    print('Journal Name: '+eis.name_journal)
    eis.volume_no = request.POST.get('volume')
    print('Volume: '+eis.volume_no)
    eis.page_no = request.POST.get('page')
    print('PAge: '+eis.page_no)
    eis.is_sci = request.POST.get('sci')
    print('SCI: '+eis.is_sci)
    eis.year = request.POST.get('year')
    print('Year: '+eis.year)
    eis.doc_id = request.POST.get('doc_id')
    print('DOC ID: '+str(eis.doc_id))
    eis.doc_description = request.POST.get('doc_description')
    print('DOC Description: '+str(eis.doc_description))
    eis.status = request.POST.get('status')
    print('Status: '+eis.status)
    eis.reference_number = request.POST.get('ref')
    print('Refrence: '+eis.reference_number)

    if(request.POST.get('doi') != None and request.POST.get('doi') != ''):
        eis.doi = datetime.datetime.strptime(request.POST.get('doi'), "%B %d, %Y")
    if (request.POST.get('doa') != None and request.POST.get('doa') != ''):
        eis.date_acceptance = datetime.datetime.strptime(request.POST.get('doa'), "%B %d, %Y")
    if (request.POST.get('dop') != None and request.POST.get('dop') != ''):
        eis.date_publication = datetime.datetime.strptime(request.POST.get('dop'), "%B %d, %Y")
    if (request.POST.get('dos') != None and request.POST.get('dos') != ''):
        eis.date_submission = datetime.datetime.strptime(request.POST.get('dos'), "%B %d, %Y")

    eis.save()
    return redirect('eis:profile')

def confrence_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_research_papers()
    eis.pf_no = pf
    eis.rtype = 'Conference'
    print(eis.pf_no)
    eis.authors = request.POST.get('authors')
    print(eis.authors)
    eis.title_paper = request.POST.get('title')
    print(eis.title_paper)
    eis.name_journal = request.POST.get('name')
    print(eis.name_journal)
    eis.venue = request.POST.get('venue')
    print(eis.venue)
    eis.volume_no = request.POST.get('volume')
    print(eis.volume_no)
    eis.page_no = request.POST.get('page')
    print(eis.page_no)
    eis.is_sci = request.POST.get('sci')
    print(eis.is_sci)
    eis.issn_no = request.POST.get('isbn')
    print(eis.issn_no)
    eis.year = request.POST.get('year')
    print(eis.year)
    eis.doc_id = request.POST.get('doc_id')
    print(eis.doc_id)
    eis.doc_description = request.POST.get('doc_description')
    print(eis.doc_description)
    eis.status = request.POST.get('status')
    print(eis.status)
    eis.reference_number = request.POST.get('reference_number')
    print(eis.reference_number)

    if (request.POST.get('doi') != None and request.POST.get('doi') != ''):
        eis.doi = datetime.datetime.strptime(request.POST.get('doi'), "%B %d, %Y")
    if (request.POST.get('doa') != None and request.POST.get('doa') != ''):
        eis.date_acceptance = datetime.datetime.strptime(request.POST.get('doa'), "%B %d, %Y")
    if (request.POST.get('dop') != None and request.POST.get('dop') != ''):
        eis.date_publication = datetime.datetime.strptime(request.POST.get('dop'), "%B %d, %Y")
    if (request.POST.get('dos') != None and request.POST.get('dos') != ''):
        eis.date_submission = datetime.datetime.strptime(request.POST.get('dos'), "%B %d, %Y")
    eis.save()
    return redirect('eis:profile')

def book_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_published_books()
    eis.pf_no = pf
    print(eis.pf_no)
    eis.p_type = request.POST.get('type')
    print(eis.p_type)
    eis.title = request.POST.get('title')
    print(eis.title)
    eis.publisher = request.POST.get('publisher')
    print(eis.publisher)
    eis.pyear = request.POST.get('year')
    print(eis.pyear)
    eis.co_authors = request.POST.get('co_authors')
    print(eis.co_authors)

    eis.save()
    return redirect('eis:profile')

def consym_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_confrence_organised()
    eis.pf_no = pf
    print(eis.pf_no)
    eis.name = request.POST.get('name')
    eis.venue = request.POST.get('venue')
    eis.role1 = request.POST.get('role')
    if(eis.role1 == 'Any Other'):
        eis.role2 = request.POST.get('other')
    if(eis.role1 == 'Organised'):
        if(request.POST.get('role2') == 'Any Other'):
            eis.role2 = request.POST.get('other')
        else:
            eis.role2 = request.POST.get('role2')
    eis.start_date = datetime.datetime.strptime(request.POST.get('start'), "%B %d, %Y")
    print(eis.start_date)
    eis.end_date = datetime.datetime.strptime(request.POST.get('end'), "%B %d, %Y")
    print(eis.end_date)

    eis.save()
    return redirect('eis:profile')

def event_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_event_organized()
    eis.pf_no = pf
    print(eis.pf_no)
    eis.type = request.POST.get('type')
    if(eis.type == 'Any Other'):
        eis.type = request.POST.get('other')
    eis.sponsoring_agency = request.POST.get('sponsoring_agency')
    eis.name = request.POST.get('name')
    eis.venue = request.POST.get('venue')
    eis.role = request.POST.get('role')
    eis.start_date = datetime.datetime.strptime(request.POST.get('start'), "%B %d, %Y")
    print(eis.start_date)
    eis.end_date = datetime.datetime.strptime(request.POST.get('end'), "%B %d, %Y")
    print(eis.end_date)

    eis.save()
    return redirect('eis:profile')

def award_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_achievement()
    eis.pf_no = pf
    print(eis.pf_no)
    eis.a_type = request.POST.get('type')
    eis.a_day = request.POST.get('a_day')
    eis.a_month = request.POST.get('a_month')
    eis.a_year = request.POST.get('a_year')
    eis.details = request.POST.get('details')

    eis.save()
    return redirect('eis:profile')

def talk_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_expert_lectures()
    eis.pf_no = pf
    print(eis.pf_no)
    eis.l_type = request.POST.get('type')
    eis.place = request.POST.get('place')
    eis.title = request.POST.get('title')
    eis.l_date = datetime.datetime.strptime(request.POST.get('l_date'), "%B %d, %Y")

    eis.save()
    return redirect('eis:profile')

def chaired_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_session_chair()
    eis.pf_no = pf
    print(eis.pf_no)
    eis.event = request.POST.get('event')
    eis.name = request.POST.get('name')
    eis.s_year = request.POST.get('s_year')
    eis.start_date = datetime.datetime.strptime(request.POST.get('start'), "%B %d, %Y")
    print(eis.start_date)
    eis.end_date = datetime.datetime.strptime(request.POST.get('end'), "%B %d, %Y")
    print(eis.end_date)

    eis.save()
    return redirect('eis:profile')

def keynote_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_keynote_address()
    eis.pf_no = pf
    print(eis.pf_no)
    eis.type = request.POST.get('type')
    eis.name = request.POST.get('name')
    eis.title = request.POST.get('title')
    eis.venue = request.POST.get('venue')
    eis.page_no = request.POST.get('page_no')
    eis.isbn_no = request.POST.get('isbn_no')
    eis.k_year = request.POST.get('k_year')
    eis.start_date = datetime.datetime.strptime(request.POST.get('start'), "%B %d, %Y")
    print(eis.start_date)

    eis.save()
    return redirect('eis:profile')

def project_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_research_projects()
    eis.pf_no = pf
    print(eis.pf_no)
    eis.pi = request.POST.get('pi')
    eis.co_pi = request.POST.get('co_pi')
    eis.title = request.POST.get('title')
    eis.financial_outlay = request.POST.get('financial_outlay')
    eis.funding_agency = request.POST.get('funding_agency')
    eis.status = request.POST.get('status')
    eis.start_date = datetime.datetime.strptime(request.POST.get('start'), "%B %d, %Y")
    print(eis.start_date)
    if (request.POST.get('end') != None and request.POST.get('end') != ''):
        eis.finish_date = datetime.datetime.strptime(request.POST.get('end'), "%B %d, %Y")
    if (request.POST.get('sub') != None and request.POST.get('sub') != ''):
        eis.date_submission = datetime.datetime.strptime(request.POST.get('sub'), "%B %d, %Y")

    eis.save()
    return redirect('eis:profile')

def consult_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_consultancy_projects()
    eis.pf_no = pf
    print(eis.pf_no)
    eis.consultants = request.POST.get('consultants')
    eis.client = request.POST.get('client')
    eis.title = request.POST.get('title')
    eis.financial_outlay = request.POST.get('financial_outlay')
    eis.start_date = datetime.datetime.strptime(request.POST.get('start'), "%B %d, %Y")
    print(eis.start_date)
    eis.end_date = datetime.datetime.strptime(request.POST.get('end'), "%B %d, %Y")
    eis.save()
    return redirect('eis:profile')

def patent_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_patents()
    eis.pf_no = pf
    print(eis.pf_no)
    eis.p_no = request.POST.get('p_no')
    eis.earnings = request.POST.get('earnings')
    eis.title = request.POST.get('title')
    eis.p_year = request.POST.get('year')
    eis.status = request.POST.get('status')
    eis.save()
    return redirect('eis:profile')

def transfer_insert(request):
    user = get_object_or_404(ExtraInfo, user=request.user)
    print(user)
    pf = user.unique_id

    eis = emp_techtransfer()
    eis.pf_no = pf
    print(eis.pf_no)
    eis.details = request.POST.get('details')
    eis.save()
    return redirect('eis:profile')

def achievement(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            c=1
            for row in reader:
                e = emp_achievement()
                e.pf_no = row['pf_no']
                e.details = row['details']

                if (row['a_type'] == '1'):
                    e.a_type = 'Award'
                elif (row['a_type'] == '2'):
                    e.a_type = 'Honour'
                elif (row['a_type'] == '3'):
                    e.a_type = 'Prize'
                elif (row['a_type'] == '4'):
                    e.a_type = 'Other'

                if (row['a_day'] != '0' and row['a_day'] != None and row['a_day'] != ''):
                    e.a_day = int(row['a_day'])

                if (row['a_month'] != '0' and row['a_month'] != None and row['a_month'] != ''):
                    e.a_month = int(row['a_month'])

                if (row['a_year'] != '0' and row['a_year'] != None and row['a_year'] != ''):
                    e.a_year = int(row['a_year'])

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.date_entry = row['date_entry']
                        e.date_entry=e.date_entry[:10]
                        e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1
                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})


def confrence(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            c=1
            for row in reader:
                e = emp_confrence_organised()
                e.pf_no = row['pf_no']
                e.venue = row['venue']
                e.name = row['name']
                e.k_year = int(row['k_year'])
                e.role1 = row['role1']
                e.role2 = row['role2']

                try:
                    if (row['start_date'] == ' ' or row['start_date'] == ''):
                        a=1
                    elif (row['start_date'] != '0000-00-00 00:00:00' and row['start_date'] != '0000-00-00'):
                        e.start_date = row['start_date']
                        e.start_date = e.start_date[:10]
                        if (row['start_date'] != '0000-00-00'):
                            e.start_date = datetime.datetime.strptime(e.start_date, "%Y-%m-%d").date()
                except:
                    a=1
                try:
                    if (row['end_date'] == ' ' or row['end_date'] == ''):
                        a = 1
                    elif (row['end_date']!='0000-00-00 00:00:00' and row['end_date'] != '0000-00-00'):
                        e.end_date = row['end_date']
                        e.end_date = e.end_date[:10]
                        if (row['end_date'] != '0000-00-00'):
                            e.end_date = datetime.datetime.strptime(e.end_date, "%Y-%m-%d").date()

                except:
                    a=1

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.date_entry = row['date_entry']
                        e.date_entry=e.date_entry[:10]
                        e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1
                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})


def consultancy(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            c=1
            for row in reader:
                e = emp_consultancy_projects()
                e.pf_no = row['pf_no']
                e.consultants = row['consultants']
                e.title = row['title']
                e.client = row['client']
                e.financial_outlay = row['financial_outlay']
                e.duration = row['duration']

                try:
                    if (row['start_date'] == ' ' or row['start_date'] == ''):
                        a=1
                    elif (row['start_date'] != '0000-00-00 00:00:00' and row['start_date'] != '0000-00-00'):
                        e.start_date = row['start_date']
                        e.start_date = e.start_date[:10]
                        if (row['start_date'] != '0000-00-00'):
                            e.start_date = datetime.datetime.strptime(e.start_date, "%Y-%m-%d").date()
                except:
                    a=1
                try:
                    if (row['end_date'] == ' ' or row['end_date'] == ''):
                        a = 1
                    elif (row['end_date']!='0000-00-00 00:00:00' and row['end_date'] != '0000-00-00'):
                        e.end_date = row['end_date']
                        e.end_date = e.end_date[:10]
                        if (row['end_date'] != '0000-00-00'):
                            e.end_date = datetime.datetime.strptime(e.end_date, "%Y-%m-%d").date()

                except:
                    a=1

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.date_entry = row['date_entry']
                        e.date_entry=e.date_entry[:10]
                        e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1
                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})



def event(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            c=1
            for row in reader:
                e = emp_event_organized()
                e.pf_no = row['pf_no']
                e.type = row['type']
                e.name = row['name']
                e.sponsoring_agency = row['sponsoring_agency']
                e.venue = row['venue']
                e.role = row['role']

                try:
                    if (row['start_date'] != '0000-00-00 00:00:00' and row['start_date'] != '0000-00-00'):
                        e.start_date = row['start_date']
                        e.start_date = e.start_date[:10]
                        if (row['start_date'] != '0000-00-00'):
                            e.start_date = datetime.datetime.strptime(e.start_date, "%Y-%m-%d").date()
                except:
                    a=1
                try:
                    if (row['end_date']!='0000-00-00 00:00:00' and row['end_date'] != '0000-00-00'):
                        e.end_date = row['end_date']
                        e.end_date = e.end_date[:10]
                        if (row['end_date'] != '0000-00-00'):
                            e.end_date = datetime.datetime.strptime(e.end_date, "%Y-%m-%d").date()

                except:
                    a=1

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.date_entry = row['date_entry']
                        e.date_entry=e.date_entry[:10]
                        e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1
                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})


def lecture(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            c=1
            for row in reader:
                e = emp_expert_lectures()
                e.pf_no = row['pf_no']
                e.l_type = row['l_type']
                e.title = row['title']
                e.place = row['place']
                e.l_year = row['l_year']

                try:
                    if (row['l_date'] != '0000-00-00 00:00:00' and row['l_date'] != '0000-00-00'):
                        e.l_date = row['l_date']
                        e.l_date = e.l_date[:10]
                        if (row['l_date'] != '0000-00-00'):
                            e.l_date = datetime.datetime.strptime(e.l_date, "%Y-%m-%d").date()
                except:
                    a=1

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.date_entry = row['date_entry']
                        e.date_entry=e.date_entry[:10]
                        e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1
                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})


def keynote(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            c=1
            for row in reader:
                e = emp_keynote_address()
                e.pf_no = row['pf_no']
                e.type = row['type']
                e.title = row['title']
                e.name = row['name']
                e.venue = row['venue']
                e.page_no = row['page_no']
                e.isbn_no = row['isbn_no']

                e.k_year = int(row['k_year'])

                try:
                    if (row['start_date'] != '0000-00-00 00:00:00' and row['start_date'] != '0000-00-00'):
                        e.start_date = row['start_date']
                        e.start_date = e.start_date[:10]
                        if (row['start_date'] != '0000-00-00'):
                            e.start_date = datetime.datetime.strptime(e.start_date, "%Y-%m-%d").date()
                except:
                    a=1
                try:
                    if (row['end_date']!='0000-00-00 00:00:00' and row['end_date'] != '0000-00-00'):
                        e.end_date = row['end_date']
                        e.end_date = e.end_date[:10]
                        if (row['end_date'] != '0000-00-00'):
                            e.end_date = datetime.datetime.strptime(e.end_date, "%Y-%m-%d").date()

                except:
                    a=1

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.date_entry = row['date_entry']
                        e.date_entry=e.date_entry[:10]
                        e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1
                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})


def thesis(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            c=1
            for row in reader:
                e = emp_mtechphd_thesis()
                e.pf_no = row['pf_no']
                e.degree_type = int(row['degree_type'])
                e.title = row['title']
                e.supervisors = row['supervisors']
                e.co_supervisors = row['co_supervisors']
                e.rollno = row['rollno']
                e.s_name = row['s_name']

                if(row['s_year'] != '0'):
                    e.s_year = int(row['s_year'])

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.date_entry = row['date_entry']
                        e.date_entry=e.date_entry[:10]
                        e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1
                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})


def patents(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            c=1
            for row in reader:
                e = emp_patents()
                e.pf_no = row['pf_no']
                e.p_no = row['p_no']
                e.title = row['title']
                e.earnings = row['earnings']
                e.p_year = int(row['p_year'])

                if(row['status'] == '1'):
                    e.status = 'Filed'
                elif(row['status'] == '2'):
                    e.status = 'Granted'
                elif(row['status'] == '3'):
                    e.status = 'Published'
                elif(row['status'] == '4'):
                    e.status = 'Owned'

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.date_entry = row['date_entry']
                        e.date_entry=e.date_entry[:10]
                        e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1
                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})


def published_books(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            c=1
            for row in reader:
                e = emp_published_books()
                e.pf_no = row['pf_no']
                e.title = row['title']
                e.publisher = row['publisher']
                e.co_authors = row['co_authors']
                e.pyear = int(row['pyear'])

                if(row['p_type'] == '1'):
                    e.p_type = 'Book'
                elif(row['p_type'] == '2'):
                    e.p_type = 'Monograph'
                elif(row['p_type'] == '3'):
                    e.p_type = 'Book Chapter'
                elif(row['p_type'] == '4'):
                    e.p_type = 'Handbook'
                elif(row['p_type'] == '5'):
                    e.p_type = 'Technical Report'

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.date_entry = row['date_entry']
                        e.date_entry=e.date_entry[:10]
                        e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1
                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            c=1
            for row in reader:
                e = emp_research_papers()
                e.pf_no = row['pf_no']
                e.authors = row['authors']
                e.rtype = row['rtype']
                e.title_paper = row['title_paper']
                e.name_journal = row['name_journal']
                e.volume_no = row['volume_no']
                e.venue = row['venue']
                e.page_no = row['page_no']
                e.issn_no = row['issn_no']
                e.doi = row['doi']
                e.doc_id = row['doc_id']
                e.doc_description = row['doc_description']
                e.reference_number = row['reference_number']
                e.year = int(row['year'])
                if(row['is_sci'] == 'Yes' or row['is_sci'] == 'No'):
                    e.is_sci = row['is_sci']

                if (row['status'] == 'Published' or row['status'] == 'Accepted' or row['status'] == 'Communicated'):
                    e.status = row['status']

                try:
                    if(str(row['date_submission']) == ' ' or str(row['date_submission']) == '' or row['date_submission'] == None):
                        a=1
                    else:
                        if (row['date_submission'] != '0000-00-00 00:00:00'  and row['date_submission'] != '0000-00-00'):
                            e.date_submission = row['date_submission']
                            e.date_submission = datetime.datetime.strptime(e.date_submission, "%Y-%m-%d").date()

                except:
                    a=1

                try:
                    if (row['start_date'] != '0000-00-00 00:00:00' and row['start_date'] != '0000-00-00'):
                        e.start_date = row['start_date']
                        e.start_date = e.start_date[:10]
                        if (row['start_date'] != '0000-00-00'):
                            e.start_date = datetime.datetime.strptime(e.start_date, "%Y-%m-%d").date()
                except:
                    a=1
                try:
                    if (row['end_date']!='0000-00-00 00:00:00' and row['end_date'] != '0000-00-00'):
                        e.end_date = row['end_date']
                        e.end_date = e.end_date[:10]
                        if (row['end_date'] != '0000-00-00'):
                            e.end_date = datetime.datetime.strptime(e.end_date, "%Y-%m-%d").date()

                except:
                    a=1
                e.save()

                try:
                    if (row['date_acceptance'] == ' ' or row['date_acceptance'] == ''):
                        a = 1
                    else:
                        if (row['date_acceptance'] != '0000-00-00 00:00:00'):
                            e.date_acceptance = row['date_acceptance']
                            e.date_acceptance = e.date_acceptance[:10]
                            e.date_acceptance = datetime.datetime.strptime(e.date_acceptance, "%Y-%m-%d").date()
                except:
                    a=1

                try:
                    if (row['date_publication'] == ' ' or row['date_publication'] == ''):
                        a = 1
                    else:
                        if(row['date_publication']!='0000-00-00 00:00:00'):
                            e.date_publication = row['date_publication']
                            e.date_publication = e.end_date[:10]
                            e.date_publication = row['date_publication']

                            e.date_publication = datetime.datetime.strptime(e.date_publication, "%Y-%m-%d").date()

                except:
                    a=1

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.date_entry = row['date_entry']
                        e.date_entry=e.date_entry[:10]
                        e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1
                a = e.start_date
                b = e.end_date
                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})




def research_projects(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                e = emp_research_projects()
                e.pf_no = row['pf_no']
                e.pi = row['pi']
                e.co_pi = row['co_pi']
                e.title = row['title']
                e.funding_agency = row['funding_agency']
                e.financial_outlay = row['financial_outlay']
                e.status = row['status']


                try:
                    if(str(row['date_submission']) == ' ' or str(row['date_submission']) == '' or row['date_submission'] == None):
                        a=1
                    else:
                        if (row['date_submission'] != '0000-00-00 00:00:00'):
                            e.date_submission = row['date_submission']
                            e.date_submission = datetime.datetime.strptime(e.date_submission, "%Y-%m-%d").date()

                except:
                    a=1

                try:
                    if (row['start_date'] != '0000-00-00 00:00:00'):
                        e.start_date = row['start_date']
                        e.start_date = e.start_date[:10]
                        e.start_date = datetime.datetime.strptime(e.start_date, "%Y-%m-%d").date()
                except:
                    a=1

                try:
                    if(row['finish_date']!='0000-00-00 00:00:00'):
                        e.finish_date = row['finish_date']
                        e.finish_date = e.finish_date[:10]
                        e.finish_date = row['finish_date']

                        e.finish_date = datetime.datetime.strptime(e.finish_date, "%Y-%m-%d").date()

                except:
                    a=1

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.date_entry = row['date_entry']
                        e.date_entry=e.date_entry[:10]
                        e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1

                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})


def visits(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                e = emp_visits()
                e.pf_no = row['pf_no']
                e.v_type = row['v_type']
                e.country = row['country']
                e.place = row['place']
                e.purpose = row['purpose']



                try:
                    if(str(row['v_date']) == ' ' or str(row['v_date']) == '' or row['v_date'] == None):
                        a=1
                    else:
                        e.v_date = row['v_date']
                        e.v_date = datetime.datetime.strptime(e.v_date, "%Y-%m-%d").date()

                except:
                    a=1

                try:

                    e.start_date = row['start_date']
                    e.start_date = datetime.datetime.strptime(e.start_date, "%Y-%m-%d").date()
                except:
                    a=1

                try:
                    if(row['end_date']!='0000-00-00 00:00:00'):
                        e.end_date = row['end_date']

                        e.end_date = datetime.datetime.strptime(e.end_date, "%Y-%m-%d").date()

                except:
                    a=1

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        e.entry_date = row['date_entry']
                        e.entry_date=e.entry_date[:10]
                        e.entry_date = datetime.datetime.strptime(e.entry_date, "%Y-%m-%d").date()
                except:
                    a=1

                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})



def session_chair(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['fileUpload']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                e = emp_session_chair()
                e.pf_no = row['pf_no']
                e.name = row['name']
                e.event = row['event']
                e.place = row['s_year']
                e.s_year=int(row['s_year'])

                try:
                    if (row['start_date'] != '0000-00-00 00:00:00'):
                        e.start_date = row['start_date']
                        e.start_date = datetime.datetime.strptime(e.start_date, "%Y-%m-%d").date()
                except:
                    a=1

                try:
                    if(row['end_date']!='0000-00-00 00:00:00'):
                        e.end_date = row['end_date']

                        e.end_date = datetime.datetime.strptime(e.end_date, "%Y-%m-%d").date()

                except:
                    a=1

                try:

                    if (row['date_entry'] == ' ' or row['date_entry'] == ''):
                        a = 1
                    else:
                        if (row['start_date'] != '0000-00-00 00:00:00'):
                            e.date_entry = row['date_entry']
                            e.date_entry=e.date_entry[:10]
                            e.date_entry = datetime.datetime.strptime(e.date_entry, "%Y-%m-%d").date()
                except:
                    a=1

                e.save()
            return HttpResponseRedirect('DONE')
    else:
        form = UploadFileForm()
    return render(request, 'eis/upload.html', {'form': form})