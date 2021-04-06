from django.shortcuts import render

# Create your views here.
from multistepapp.forms import ApplicantDetailsForm,AcademicQualificationForm,AcademicQualificationFormSet 
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request,"home.html")

class ApplicationWizardView(SessionWizardView):

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'files'))
    form_list = [ApplicantDetailsForm,AcademicQualificationFormSet]
    template_name = "form.html"
    initial_dict= initial

    def process_step(self, form):
        #print(form.data)
        """
        This method is used to postprocess the form data. By default, it
        returns the raw `form.data` dictionary.
        """

        #print(form.data)
        #print(self)
        
        institution = {}
        inst_list = []
        if self.steps.current == '1':
            
            institution['institution'] = form.data['1-0-institution']
            institution['date_from'] = form.data['1-0-date_from']
            institution['date_to'] = form.data['1-0-date_to']
            inst_list.append(institution)
            inst_keys = dict(form.data.lists())
            
            #Create dictionary dynamically for the other institutions incase more than two institutions are entered
            if inst_keys.get('1-NaN-institution') and type(inst_keys.get('1-NaN-institution')) is list:
                inst_list2 = []
                #Add institutions 
                for i,insti in enumerate(inst_keys.get('1-NaN-institution')):
                    inst_i = {}
                    #print(i)
                    date_from = inst_keys['1-NaN-date_from'][i]
                    date_to = inst_keys['1-NaN-date_to'][i]
                    course_duration = inst_keys['1-NaN-course_duration'][i]
                    inst_i['institution'] = insti
                    inst_i['date_from'] = date_from
                    inst_i['date_to'] = date_to
                    
                    inst_list2.append(inst_i)
                    #print(inst_list2)
                inst_list.extend(inst_list2)
            #Create dictionary dynamically for the other institutions incase more than two institutions are entered
            if inst_keys.get('1-NaN-institution') and type(inst_keys.get('1-NaN-institution')) is not list:
                inst_0 = {}
                inst_0['institution'] = form.data['1-NaN-institution']
                inst_0['date_from'] = form.data['1-NaN-date_from']
                inst_0['date_to'] = form.data['1-NaN-date_to']
                inst_0['course_duration'] = form.data['1-NaN-course_duration']
                #inst_0['achievements'] = ''
                inst_list.append(inst_0)
            
            #Add the entered information to a session object
            self.request.session['institution'] = inst_list
    
    #Edit the function to process files 
    def process_step_files(self, form):
        if self.steps.current == '1':
            inst_list = []
            inst_list2 = []
            inst_0 = form.files['1-0-achievements']
            inst_keys = dict(form.files.lists())
            inst_list.append(inst_0)
            
            if inst_keys.get('1-NaN-achievements') and type(inst_keys.get('1-NaN-achievements')) is list:
                for insti in  inst_keys.get('1-NaN-achievements'):
                    inst_list2.append(insti)
                   
                inst_list.extend(inst_list2)


            if inst_keys.get('1-NaN-achievements') and type(inst_keys.get('1-NaN-achievements')) is not list:
                inst_list2.append(inst_keys.get('1-NaN-achievements'))
                inst_list.extend(inst_list2)
            print(inst_list)
            


            institutions = self.request.session['institution']
            #Use django file system storage to store the files and get the file path 
            #which we will append to the session created in the previous function ie process_step
          
            fs = FileSystemStorage()
            for i, institution in enumerate(institutions):
                myfile = inst_list[i]
                filename = fs.save(myfile.name, myfile.file)
                print(filename)
                uploaded_file_url = fs.url(filename)
                institution['achievements'] = filename
                print("File URL ",institution['achievements'])
                
            self.request.session['institution'] = institutions
    
    @transaction.atomic
    def done(self, form_list,form_dict, **kwargs):
    	form_dict2 = self.get_all_cleaned_data()
        print(form_dict2)

        #Remove the default formset by django-formtools before entering the record to the db
    	insts = form_dict2.pop('formset-1')
        print("Institutions,",insts)

        #Get the institutions we implemented in the two functions above
        academic_institutions = self.request.session['institution']
        
        #Enter the Application details to the Appl database table
        application, created = Appl.objects.update_or_create(**form_dict2)
        print(created)

        for institution in academic_institutions:
            temp_file = institution['achievements']
            print(type(temp_file))
            #print(academic_institutions)
            academic_institution, created = AcademicInstitution.objects.update_or_create(**institution)
            academic_institution.appl = application
            
            academic_institution.save()
        application.save()

        return redirect('multistepapp:home')
