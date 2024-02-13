from __future__ import unicode_literals, absolute_import

import logging

from flask import (jsonify, json, request)
from flask.views import MethodView

from backend.apps.masters.models.companies import Company
from backend.apps.masters.models.customers import Customer
from backend.apps.sales.models.orders import Order
from backend.apps.sales.models.order_items import OrderItem


from backend.logs import FILE_HANDLER

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)

class OrderItemListMethodView(MethodView):
    """
    Class OrderItemListMethodView, Is display OrderItem base MethodView
    """
    model = OrderItem
    page = 1
    per_page = 5
    
    
    def queryset(self):
        # Get the parameters filter
        company = str(request.args.get("company") or "")
        customer = str(request.args.get("customer") or "")
        part = str(request.args.get("part") or "")
        
        
        if company:
            queryset = OrderItem.query.filter(
                            OrderItem.order.has(
                                Order.customer.has(
                                    Customer.company.has(
                                        Company.name.icontains(company)
                                    ))))
        else:
            queryset = OrderItem.query
            
        if customer:
            queryset = queryset.filter(
                            OrderItem.order.has(
                                Order.customer.has(
                                    Customer.name.icontains(customer)
                                )))
        if part:
            queryset = queryset.filter(
                OrderItem.product.icontains(part)
                )
        
        queryset = queryset.paginate(
                page=self.page, 
                per_page=self.per_page,
                error_out=False
                )
        
        return queryset
    
    def get(self):
        # Filter Parameters
        company = str(request.args.get("company") or "")
        customer = str(request.args.get("customer") or "")
        part = str(request.args.get("part") or "")
        
         # Active page
        try:
            self.page = int(request.args.get("page") or 1)
        except:
            self.page = 1
            
        meta = dict()
        filter_by = dict()
        url_base = request.base_url
        params_filter = []
        
        if company:
            filter_by.update(company=company)
            params_filter.append("company={}".format(company))
            
        if customer:
            filter_by.update(customer=customer)
            params_filter.append("customer={}".format(customer))
            
        if part:
            filter_by.update(part=part)
            params_filter.append("part={}".format(part))
        
        if filter_by:
            meta.update(filter_by=filter_by)
        
        
         # Get data records
        queryset = self.queryset()
        
        
        if params_filter:
            first = "{}?page=1&{}".format(
                    url_base,"&".join(params_filter))
            
            last = "{}?page={}&{}".format(
                    url_base, queryset.pages,"&".join(params_filter))
            
            if queryset.has_next:
                next = "{}?page={}&{}".format(
                    url_base, int(self.page) + 1 ,"&".join(params_filter))
            else:
                next = None
                
            if queryset.has_prev:
                prev = "{}?page={}&{}".format(
                    url_base, int(self.page) - 1 ,"&".join(params_filter))
            else:
                prev = None
        else:
            first = "{}?page=1".format(
                    url_base)
            
            last = "{}?page={}".format(
                    url_base, queryset.pages)
            
            if queryset.has_next:
                next = "{}?page={}".format(
                    url_base, int(self.page) + 1)
            else:
                next = None
                
            if queryset.has_prev:
                prev = "{}?page={}".format(
                    url_base, int(self.page) - 1)
            else:
                prev = None
            
            
        links = dict(first=first,
                   prev=prev,
                   next=next,
                   last=last
                   )
        
        # Pagination
        pagination = dict(
            page=self.page,
            per_page=self.per_page,
            pages=queryset.pages,
            count=queryset.total
            )
        
        meta.update(pagination=pagination)
        
        # Data
        data = []
        start_no = (self.page - 1 * self.per_page)
        for index, q in enumerate(queryset):
            data.append(
                dict(
                    no=start_no+(index+1), 
                    row=q.to_dict()
                    )
                )
        
        context = dict(
                links=links,
                data=data,
                meta=meta
            )
        
        return jsonify(context),200
        
        
