from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from products.router import get_products

router = APIRouter()

templates = Jinja2Templates(directory="templates")

"""
@router.get("/register", response_class=HTMLResponse)
def registration_form(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})
"""

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/products", response_class=HTMLResponse)
def get_products_page(request: Request, product = Depends(get_products)):
    return templates.TemplateResponse("products.html", {"request": request, "products": product["data"]})


@router.get("/about", response_class=HTMLResponse)
def about_us(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/contacts", response_class=HTMLResponse)
def contacts(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request})


#@router.get("/search/{product_name}")
#def get_search_page(request: Request, products: str = Depends(search)):
 #   return templates.TemplateResponse("search.html", {"request": request, "products": products["data"]})
