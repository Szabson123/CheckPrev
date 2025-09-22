from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import requests

from .models import Famili, Product, Composition, ProductMedia, Category
from .forms import FamiliForm, ProductForm, CompositionForm, ProductMediaForm
import json
from django.utils.timezone import now

def add_famili(request):
    if request.method == 'POST':
        form = FamiliForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('choose_form')
    else:
        form = FamiliForm()
    return render(request, 'forms/add_family.html', {'form': form})


def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        media_form = ProductMediaForm(request.POST, request.FILES)

        if product_form.is_valid() and media_form.is_valid():
            product = product_form.save()
            media = media_form.save(commit=False)
            media.product = product
            media.save()
            return redirect('choose_form')

    else:
        product_form = ProductForm()
        media_form = ProductMediaForm()

    return render(request, 'forms/add_prod.html', {
        'product_form': product_form,
        'media_form': media_form
    })


def add_composition(request):
    if request.method == 'POST':
        form = CompositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('choose_form')
    else:
        form = CompositionForm()
    return render(request, 'forms/add_comp.html', {'form': form})


def choose_form(request):
    return render(request, 'choose_form.html')


def redi(request):
    return redirect('/generate')


def base_page(request):
    return render(request, 'base.html')

        
def generate_page(request):
    categories = Category.objects.all()
    return render(request, 'generate_page.html', {'categories': categories})


def family_for_categories(request):
    """Ajax: lista rodziny dla danej kategori."""
    category_id = request.GET.get('category_id')
    famili = Famili.objects.filter(category_id=category_id).values('id','name')
    return JsonResponse({'famili': list(famili)})


def products_for_family(request):
    """Ajax: lista produktów dla danej rodziny."""
    family_id = request.GET.get('family_id')
    products = Product.objects.filter(check_prev_id=family_id).values('id','name')
    return JsonResponse({'products': list(products)})


def compositions_for_product(request):
    """Ajax: lista kompozycji dla danego produktu."""
    product_id = request.GET.get('product_id')
    comps = Composition.objects.filter(check_prev_id=product_id).values('id','name')
    return JsonResponse({'compositions': list(comps)})


def is_change(serial_number, flag):
    prefix = serial_number[:-8]
    number_part = serial_number[-8:]
    try:
        number = int(number_part)
    except ValueError:
        return serial_number
    if flag == 'down':
        number -= 1
    elif flag == 'up':
        number += 1
    new_number_part = str(number).zfill(8)
    return prefix + new_number_part

def crate_new_boards(prepared_serial, how_many_boards):
    boards = []
    for i in range(1, how_many_boards + 1):
        new_middle = str(i).zfill(2)
        new_serial = prepared_serial[:9] + new_middle + prepared_serial[11:]
        boards.append(new_serial)
    return boards


@csrf_exempt
def prepare_serials(request):
    """Ajax: oblicza seriale na podstawie wybranej kompozycji."""
    if request.method == 'POST':
        data = json.loads(request.body)
        serial_number = data.get('serial_number')
        composition_id = data.get('composition_id')

        comp = get_object_or_404(Composition, id=composition_id)
        product = comp.check_prev 
        flag = comp.is_change_down_flag
        rows = product.rows
        cols = product.cols

        prepared_serial = is_change(serial_number, flag)
        how_many = rows * cols
        serials  = crate_new_boards(prepared_serial, how_many)

        return JsonResponse({'serials': serials})
    
    
def set_phase_if_exist(comp, serial):
    if not comp.set_phase:
        return {"status": "skipped", "reason": "set_phase is empty"}

    insert_data = {
        "testName": comp.set_phase,
        "assemblyFormId": 0,
        "idParts": comp.name,
        "msn": serial,
        "testDatetime": timezone.localtime(timezone.now()).isoformat(),
        "result": 1
    }

    try:
        insert_url = 'http://10.140.13.11:5556/api/insertdata'
        response = requests.post(insert_url, json=insert_data)
        response.raise_for_status()
        return {"status": "sent", "response": response.json()}
    except requests.RequestException as e:
        return {"status": "error", "error": str(e)}

@csrf_exempt
def send_one_serial(request):
    """Ajax: wysyła pojedynczy serial do API i zawsze insertuje dane."""
    if request.method == 'POST':
        data = json.loads(request.body)
        serial = data.get('serial')
        composition_id = data.get('composition_id')
        use_set_phase = data.get('use_set_phase', True)

        comp = get_object_or_404(Composition, id=composition_id)
        apiURL = 'http://10.140.13.11:5556/api/checkprevphase'
        json_data = {
            'phaseID': comp.phase,
            'internalCode': comp.name,
            'serialNumber': serial,
            'level': '0',
            'resultType': '-1'
        }

        try:
            response = requests.post(apiURL, json=json_data)
            response.raise_for_status()
            result_data = response.json()
            if use_set_phase:
                phase_result = set_phase_if_exist(comp, serial)
            else:
                phase_result = {"status": "skipped", "reason": "manual skip"}
                
            return JsonResponse({
                'status': 'success' if result_data.get('returnCode') == 0 else 'error',
                'serial': serial,
                'code': result_data.get('returnCode'),
                'description': result_data.get('returnCodeDescription'),
                'phase_action': phase_result
            })

        except requests.RequestException as e:
            return JsonResponse({
                'status': 'request_failed',
                'serial': serial,
                'error': str(e)
            })
            
            
def get_product_dimensions(request):
    product_id = request.GET.get('product_id')
    try:
        product = Product.objects.get(id=product_id)
        media = ProductMedia.objects.get(product=product)

        comp = Composition.objects.filter(check_prev=product).first()
        upper_snake = comp.upper_snake if comp else True
        
        return JsonResponse({
            'rows': product.rows,
            'cols': product.cols,
            'img_width': product.img_width,
            'img_height': product.img_height,
            'image_none': media.image_none.url,
            'image_true': media.image_true.url,
            'image_false': media.image_false.url,
            'upper_snake': upper_snake
        })
    except (Product.DoesNotExist, ProductMedia.DoesNotExist):
        return JsonResponse({'error': 'Brak danych'}, status=404)