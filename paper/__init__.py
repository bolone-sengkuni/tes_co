import requests, random
from openpyxl import Workbook
from datetime import datetime
import string, os
from requests_toolbelt import MultipartEncoder
from pydash import omit
import urllib, json

DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PAPER = f'{DIR}/paper.xlsx'

DIR = os.path.dirname(os.path.abspath(__file__))
class GetAuth:
    def login__(email, sandi):
        headers = {
            'content-type':'application/json; charset=utf-8',
            'INGRESSCOOKIE':'cfda8846bc7be3bb28fdb63987c9c3ea|15c4a256545252d8d9c6fbf36d3467c6; Path=/; Secure; HttpOnly',
            'access-control-allow-origin':'http://localhost',
            'etag':'W/"44-mPTbBrZpvWCI9OOcqUINEogywEs"'
        }
        res = requests.post(
            url = 'https://api.paper.id/api/v1/auth/paper-chain-status',
            headers = headers,
            json ={"email":email}
        )
        INGRESS = headers['INGRESSCOOKIE']
        headers = {
            "Host": "api.paper.id",
            "accept": "application/json, text/plain, */*",
            "authorization": "null",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; POCO F2 Pro Build/QKQ1.191117.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.120 Mobile Safari/537.36",
            "content-type": "application/json",
            "origin": "http://localhost",
            "x-requested-with": "id.paper.invoicer",
            "referer": "http://localhost/auth/login",
            "accept-encoding": "gzip, deflate",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        res = requests.post(
            url = "https://api.paper.id/api/v1/auth/login",
            headers = headers,
            json = {"email":email,"password":sandi,"ttl":31104000}
        )
        data = res.json()
        auth = data['id']
        headers = omit(headers, "authorization")
        headers.update({
            "authorization": auth
        })
        with open(f'{DIR}/auth.json', 'w') as f:
            f.write(json.dumps(
                {
                    "auth": auth,
                },
                indent=4
            ))



class Auth:
    def headers_paper():
        auth_token = json.load(open(f'{DIR}/auth.json'))['auth']
        return {
            "Host": "api.paper.id",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; POCO F2 Pro Build/QKQ1.191117.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.120 Mobile Safari/537.36",
            "content-type": "application/json",
            "origin": "http://localhost",
            "x-requested-with": "id.paper.invoicer",
            "referer": "http://localhost/auth/login",
            "accept-encoding": "gzip, deflate",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": auth_token
        }

class GeneratePaper:
    def __init__(self, harga: int):
        self.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': Auth.headers_paper()["authorization"],
            'Content-Type': 'application/json',
            'Origin': 'https://www.paper.id',
            'Referer': 'https://www.paper.id/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        }
        self.harga = int(harga)

    def waktu(self):
        now = datetime.now()
        huruf = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
        number = ''.join(random.choice(string.digits) for _ in range(6))
        return [
            "{}/{}/{}".format(huruf, now.strftime('%Y'), number),
            now.strftime('%d/%m/%Y')
        ]

    def get_patner(self) -> dict:
        data = '{"filters":{"number":{"matchMode":"undefined","value":""},"global":{"matchMode":"undefined","value":""},"name":{"matchMode":"undefined","value":null},"email":{"matchMode":"undefined","value":""},"phone":{"matchMode":"undefined","value":""},"country":{"matchMode":"undefined","value":""},"type":{"matchMode":"undefined","value":""}},"first":0,"rows":100,"sortOrder":1,"sortField":"name","type":"","includes":[]}'
        response = requests.post(
            'https://api.paper.id/api/v1/invoicer/partners/all-clients', headers=self.headers, data=data
        )
        hasil = response.json()
        return random.choice(hasil['partners'])

    
    def get_produk(self):
        data = '{"filters":{"name":{"matchMode":"undefined","value":""},"global":{"matchMode":"undefined","value":""},"code":{"matchMode":"undefined","value":""},"sales_price":{"matchMode":"undefined","value":""},"category_name":{"matchMode":"undefined","value":""},"purchase_price":{"matchMode":"undefined","value":""},"uom_name":{"matchMode":"undefined","value":""},"track_stock":{"matchMode":"undefined","value":""}},"first":0,"rows":100,"sortOrder":1,"sortField":"name"}'
        response = requests.post(
            'https://api.paper.id/api/v1/inventory/products/all', headers=self.headers, data=data
        )
        hasil = response.json()
        return random.choice(hasil["products"])


    def write_invoices(self):
        # print(self.harga)
        for _ in range(9999999):
            try:
                patner = self.get_patner()
                produk = self.get_produk()
                break
            except:continue

        book  = Workbook()
        sheet = book.active
        sheet.append([
            '*Client Name','*Partner Telephone Number','*No. Invoice','*Date',
            '*Due Date','*Item Name','*Item Description','*Qty','*Price'
        ])
        
        nomer_invoices = self.waktu()[0]
        sheet.append([
            patner['name'], patner['phone'], nomer_invoices, 
            self.waktu()[1], self.waktu()[1], produk['name'], produk['description'],
            '1', self.harga
            
        ])
        sheet.title = 'format_bulk'
        book.save(FILE_PAPER)
        return nomer_invoices
    
    def uploud_invoices(self):
        fields = {
            "Content-Disposition": "form-data",
            "name": "file",
            "filename": "paper.xlsx",
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "file": ("paper.xlsx", open(FILE_PAPER, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        
        boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
        data = MultipartEncoder(fields=fields, boundary=boundary)
        
        headers = omit(Auth.headers_paper(), 'content-type')
        headers.update({'content-type': f'multipart/form-data; boundary={boundary}'})

        invo = requests.post(
            url="https://api.paper.id/api/v1/import-data/invoice/upload",
            headers=headers,
            data=data
        )
        batch_id = invo.json()['arango_batch_id']
        #save
        
        save = requests.post(
            "https://api.paper.id/api/v1/import-data/invoice/save",
            headers=Auth.headers_paper(),
            json={
            "arango_batch_id": batch_id,
            "room": "16808051444487163"
            }
        )
        
        
    def cari_url_pembayaran(self, nomer_invoices) -> str:
        while True:
            try:
                respon = requests.post(
                    'https://api.paper.id/api/v1/invoicer/sales-invoices/all',
                    headers=Auth.headers_paper(),
                    json={
                        "filters": {
                            "number": {
                                "matchMode": "undefined",
                                "value": nomer_invoices
                            },
                            "global": {
                                "matchMode": "undefined",
                                "value": ""
                            },
                            "client_name": {
                                "matchMode": "undefined",
                                "value": ""
                            },
                            "partner_id": {
                                "matchMode": "undefined",
                                "value": ""
                            },
                            "status": {
                                "matchMode": "undefined",
                                "value": []
                            },
                            "invoice_total": {
                                "matchMode": "undefined",
                                "value": ""
                            },
                            "send_status": {
                                "matchMode": "undefined",
                                "value": []
                            },
                            "start_invoice_date": {
                                "matchMode": "undefined",
                                "value": ""
                            },
                            "end_invoice_date": {
                                "matchMode": "undefined",
                                "value": ""
                            }
                        },
                        "first": 0,
                        "rows": 8,
                        "sortOrder": -1,
                        "sortField": "created_at",
                        "file_type": "csv"
                    }
                )
                hasil = respon.json()['invoices']
                uuid_sales = hasil[0]['uuid']
                break
            except:continue

        
        resp = requests.post(
            f'https://api.paper.id/api/v1/invoicer/single-link-invoice/{uuid_sales}', headers=Auth.headers_paper(),json={
                "share_type": "android"
            }
        )
        return resp.json()['url']
        
        
    def get_kode(self, url: str):
        resp = requests.get(
            url=f'https://{url}', allow_redirects=True
        )
        parares = urllib.parse.parse_qs(str(resp.url))['https://payment.paper.id/single-invoice?ParaRes'][0]
        
        headers = {
            "accept":"application/json, text/plain, */*",
            "accept-encoding":"gzip, deflate, br",
            "accept-language":"en-US,en;q=0.9",
            "content-type":"application/json",
            "host":"api.paper.id",
            "origin":"https://payment.paper.id",
            "referer":"https://payment.paper.id/",
            "token":"null",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }
        resp = requests.post(
            "https://api.paper.id/api/v1/payper-api/authorization", headers=headers, json={
                "ParaRes": parares
            }
        )
        bes         = resp.json()
        golang_data = bes['golang_data']
        parares     = bes['data']
        headers     = omit(headers, "token")
        headers.update({"token": parares})
        
        resp = requests.post(
            "https://api.paper.id/api/v1/payper-api/single-invoice", headers=headers, json={
                    "data":golang_data,
                    "link_source": "email",
                    "parares": parares
            }
        )
        
        fullInvoices = resp.json()['full_invoice']['data']
        _id = fullInvoices['_id']
        
        resp = requests.post(
            "https://api.paper.id/api/v1/payper-api/single-invoice/payment-method-all", headers=headers, json={
                    "data":golang_data,
                    "link_source": "email",
                    "parares": parares
            }
        )
        body = resp.json()['body']
        sup_id  = body['company_id']
        buyer_id= body['partner_company_id']
        
        resp = requests.post(
            "https://api.paper.id/api/v1/payper-api/payment-request/create", headers=headers, json={
                    "supplier_id": sup_id,
                    "buyer_id": buyer_id,
                    "invoices": [
                        {
                        "invoice_id": _id
                    }
                ],
                    "source": "payper"
            }
        )
        paper_key = resp.json()['data']['payment_request']['_key']
        
        resp = requests.post(
            "https://api.paper.id/api/v1/payper-api/payment-request/payment-method/choose", headers=headers, json={
                    "promotion_id": "",
                    "payment_method": "mitra_pembayaran_digital",
                    "payment_provider": "blibli",
                    "payment_request_key": paper_key,
                    "paper_customer_id": buyer_id
            }
        )
        data = resp.json()['data']
        
        hasil = requests.get(
            f"https://api.paper.id/api/v1/payper-api/payment-request/key/{paper_key}", headers=headers
        )
        return hasil.json()['data']["external_id"]

    def running(self) -> list:
        nomer_invoices = self.write_invoices()
        self.uploud_invoices()
        url = self.cari_url_pembayaran(nomer_invoices=nomer_invoices)
        kode = self.get_kode(url=url)
        return kode, url
        





