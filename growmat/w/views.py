from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
#from django.template.context import RequestContext
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy


 
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Instrument
from .models import InstrumentForm
from .models import InstrumentList

from .models import Rule
from .models import RuleForm

from .models import Archive

#from test.utils import instrumented_test_render


class InstrumentCreate(CreateView):
    model = Instrument
    fields = ['address', 'type', 'index', 'name']
    #success_url('w')
    def get_success_url(self):
        return reverse('w:list')

class InstrumentUpdate(UpdateView):
    model = Instrument
    fields = ['address', 'type', 'index', 'name']
    def get_success_url(self):
        return reverse('w:list')

class InstrumentDelete(DeleteView):
    model = Instrument
    success_url = reverse_lazy('w:list')   


class RuleDelete(DeleteView):
    model = Rule
    success_url = reverse_lazy('w:rule/0')   

# Create your views here.
def archive(request, pk=None):
    return render(request, 'w/archive.html')
    
    if pk:
        instrument0 = Instrument.objects.get(pk=pk)
        archives = Archive.objects.filter(instrument=instrument0).order_by('datetime')
    else:
        archives = Archive.objects.order_by('datetime', 'instrument')
    
    context = RequestContext(request, {
        'archives': archives
    })

    return render(request, 'w/archive.html', context)
   

def webcam(request, pk=None):
	return render(request, 'w/webcam.html')
	
def index(request, pk=None):
    #print pk
    #if request.method == 'POST':
    #    form = InstrumentForm(request.POST, instance=instrument)
    
    #objects = Instrument.objects.order_by('address')



    

    
    form = InstrumentForm()

   
    if request.method == 'POST':
        if 'create' in request.POST:
        #if int(pk)==0:
            form = InstrumentForm(request.POST)
            #form = InstrumentForm(request.POST, instance=instrument)
            #form.value = 0.0
            #form.status = 1
            if form.is_valid():
                form.save()
            #print form.is_valid()
                return HttpResponseRedirect('/w/')
            form.pk = 0
            instruments = Instrument.objects.order_by('pk')    
            context = RequestContext(request, {
                'instruments': instruments, 'form':form
            })
            return render(request, 'w/index.html', context)

        #else:
        if 'save' in request.POST:
            #print pk
            instrument = Instrument.objects.get(pk=pk)
            form = InstrumentForm(request.POST, instance = instrument)
            #form.value = 0.0
            #form.status = 1
            if form.is_valid():
                #print 'update'
                form.save()
                #print form.is_valid()
                return HttpResponseRedirect('/w/')
            
            form.pk = pk
            instruments = Instrument.objects.order_by('pk')    
            context = RequestContext(request, {
                'instruments': instruments, 'form':form
            })
            return render(request, 'w/index.html', context)


                
        if 'delete' in request.POST:
            #print pk
            instrument = Instrument.objects.get(pk=pk)
            instrument.delete()
            pk=0
            return HttpResponseRedirect('/w/')
    
    else:
        instruments = Instrument.objects.order_by('pk')
        if pk:
            if int(pk)== 0:
                form0 = InstrumentForm()
                context = RequestContext(request, {
                    'instruments': instruments, 'form0':form0 })
                return render(request, 'w/index.html', context)
            
            if int(pk)>0:
                #print pk
                instrument = Instrument.objects.get(pk=pk)
                form = InstrumentForm(instance = instrument)
            
                form.pk=int(pk)
                context = RequestContext(request, {
                    'instruments': instruments, 'form':form })
                return render(request, 'w/index.html', context)

        context = RequestContext(request, {
            'instruments': instruments })
        return render(request, 'w/index.html', context)           
        #if request.method == 'POST':
        #    form = InstrumentForm(request.POST)
            #form = InstrumentForm(request.POST, instance=instrument)
        #    if form.is_valid():
        #        form.save()
                
        #    context = RequestContext(request, {
         #                                      'instruments': objects, 'list':list, 'form0':form0, 'form':form
        #    })
        #    return render(request, 'w/index.html', context)
                #print 'frfrf'
        #print error_message
        #return render(request, 'w:index', {'form': form, 'instrument': instrument})
        #form.pk=int(pk)
    
        #else:
        #    form = InstrumentForm()
    
    #list = InstrumentList.as_view()
    instruments = Instrument.objects.order_by('pk')
    
    #for object in objects:
    #    object.fields = dict((field.name, field.value_to_string(object))
    #    for field in object._meta.fields)

    
    form0 = InstrumentForm()
    #context = RequestContext(request, {
	#	'instruments': instruments, 'list':list, 'form0':form0, 'form':form
	#})
    context = RequestContext(request, {
        'instruments': instruments, 'form0':form0, 'form':form
    })

    return render(request, 'w/index.html', context)
	
    for object in objects:
		object.fields = dict((field.name, field.value_to_string(object))
			for field in object._meta.fields)

    template = loader.get_template('w/index.html')
    return render_to_response(template, { 'objects':objects },
		context_instance=RequestContext(request))
		
        
        
# Create your views here.
def rule(request, pk=None):
    form = RuleForm()
   
    if request.method == 'POST':
        if 'create' in request.POST:
            form = RuleForm(request.POST)
            if form.is_valid():
                form.save()
            #print form.errors
                return HttpResponseRedirect('/w/rule/')
            
            form.pk = 0
            rules = Rule.objects.order_by('pk')    
            context = RequestContext(request, {
                'rules': rules, 'form':form
            })
            return render(request, 'w/rule.html', context)
    
        if 'save' in request.POST:
            rule = Rule.objects.get(pk=pk)
            form = RuleForm(request.POST, instance = rule)
            if form.is_valid():
                form.save()

                return HttpResponseRedirect('/w/rule/')
            form.pk = pk
            rules = Rule.objects.order_by('pk')    
            context = RequestContext(request, {
                'rules': rules, 'form':form
            })
            return render(request, 'w/rule.html', context)
                
        if 'delete' in request.POST:
            rule = Rule.objects.get(pk=pk)
            rule.delete()
            return HttpResponseRedirect('/w/rule/')
        
    else:
        rules = Rule.objects.order_by('pk')
        
        if pk:
            if int(pk)>0:
                rule = Rule.objects.get(pk=pk)
                form = RuleForm(instance = rule)
            
                form.pk=int(pk)
                
                context = RequestContext(request, {
                    'rules': rules,  'form':form
                })

                return render(request, 'w/rule.html', context)
             
            if int(pk)==0: 
                form = RuleForm() 
                form.pk = 0
                context = RequestContext(request, {
                    'rules': rules,  'form':form
                })

                return render(request, 'w/rule.html', context) 

        context = RequestContext(request, {
                    'rules': rules
                })

        return render(request, 'w/rule.html', context) 
                
    rules = Rule.objects.order_by('pk')
    
    #for object in objects:
    #    object.fields = dict((field.name, field.value_to_string(object))
    #    for field in object._meta.fields)

    
    #context = RequestContext(request, {
    #    'instruments': instruments, 'list':list, 'form0':form0, 'form':form
    #})
    context = RequestContext(request, {
        'rules': rules, 'form':form
    })

    return render(request, 'w/rule.html', context)

        

	
#	output = ', '.join([p.user_name for p in instrument_list])
#	return HttpResponse(output)

def instrumentAdd(request):
	#if 'addTemperature' in request.POST:
		#instrument = InstrumentTemperature.objects.create()
	#	instrument = InstrumentTemperature.objects.create()
		#instrument = Instrument()
		#form = InstrumentTemperatureForm()
		#return render(request, 'w/instrument.html', {'form': form})	#return render(request, 'w/instrument.html', {'form': form})
		#return render(request, 'w/instrument.html', {'form': form, 'instrument': instrument})
	#return HttpResponseRedirect('/w')
	instrument = Instrument(pk=0)
	#form = InstrumentForm()
	form = InstrumentCreate()
	return render(request, 'w/instrument.html', {'form': form, 'instrument': instrument})
	
def instrument(request, instrument_id):
	
	if int(instrument_id)>0:
		instrument = Instrument.objects.get(pk=instrument_id)
		
	
	#try:
	#	a = InstrumentTemperature.objects.get(pk=instrument_id)
	#except InstrumentTemperature.DoesNotExist:
	#	a = Instrument.objects.get(pk=instrument_id)
			
	if request.method == 'POST':
		#if 'addTemperature' in request.POST:
		#	form = InstrumentTemperatureForm()
			#return render(request, 'w/instrument.html', {'form': form})
	
		#try:
		#	a = InstrumentTemperature.objects.get(pk=instrument_id)
		#except InstrumentTemperature.DoesNotExist:
		#	a = Instrument.objects.get(pk=instrument_id)
		
		#print 'ssfsf' 
		#a = Instrument.objects.get(pk=instrument_id)
		#print isinstance(a, InstrumentTemperature)
		#print a.self
		#print type(a).__name__
		if 'delete' in request.POST:
			instrument.delete()
			return HttpResponseRedirect('/w')
			#return render(request, 'w/index.html')				return HttpResponseRedirect('/w')
			# create a form instance and populate it with data from the request
		
			
			#a.delete()
		if 'copy' in request.POST:
			form = InstrumentForm(request.POST)
		
		if 'save'in request.POST:
			
			if int(instrument_id)>0:
				form = InstrumentForm(request.POST, instance=instrument)
			else:
				form = InstrumentForm(request.POST)
			
					
		# check whether it's valid:
		#print 'XXXd2'
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			#return HttpResponseRedirect(reverse('w:instrument', args=(instrument.id,)))
			#print form.fields['user_name'].value
			#form.save(commit=False)
			
			saved_instrument = form.save()
			
			instrument = get_object_or_404(Instrument, pk=saved_instrument.pk)
			
			#+--	print 'fdfdfdf'#instrument=(InstrumentTemperature)instrument
			#return HttpResponseRedirect('/')
			
			#instrument = get_object_or_404(Instrument, pk=instrument_id)
			#print '!!!'
			return render(request, 'w/instrument.html', {'form': form, 'instrument': instrument})
		#print 'XXXd3'
		#print form.errors
		return render(request, 'w/instrument.html', {'form': form, 'instrument': instrument})
	# if a GET (or any other method) we'll create a blank form
	else:
		#instrument = get_object_or_404(Instrument, pk=instrument_id)		
			
		#try:
		#	instrument = InstrumentTemperature.objects.get(pk=instrument_id)	
		#except InstrumentTemperature.DoesNotExist:
		#	instrument = get_object_or_404(Instrument, pk=instrument_id)	
		
		#try:
		#	instrument2 = Instrument.objects.get(instrument_id=instrument.id)
		#except:
		#	instrument2 = None
		#if isinstance(instrument, InstrumentTemperature):
		#	form = InstrumentTemperatureForm(instance = instrument)
		#else:
		#form = InstrumentForm(instance = instrument)
		#form = InstrumentForm(instance = insrument2)
		
		form = InstrumentForm(instance = instrument)
		return render(request, 'w/instrument.html', {'form': form, 'instrument': instrument})
