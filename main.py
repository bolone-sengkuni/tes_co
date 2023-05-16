from paper import *
from os import system, name
import random, re, uuid



def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def banner():
    print("""\
=============================
VOCHER DIGITAL BLIBLI x PAPER
=============================
""")

def banner2():
    print("""\
=============================
      LOGIN AKUN PAPER
=============================
""")
    
    
def hapus_line():
    print ("\033[A                                                                                                      \033[A")

def cari_harga(persen: int, maxs: int) -> int:
    hasil = [i for i in range(5000, 900000, 5000) if i * persen/100 == maxs]
    return int(hasil[0])



def random_user_agent(userId: str) -> str:
    while True:
        try:
            resp = requests.get(
                'https://raw.githubusercontent.com/Magisk-Modules-Repo/MagiskHidePropsConf/master/common/prints.sh'
            )
            bahan = resp.text.splitlines()[13:-2]
            break
        except:continue
    
    ngrandom = random.choice(bahan)
    if re.search(r';', ngrandom):
        finger = ngrandom.split(';')[1].split('/')
    else:
        finger = ngrandom.split('=')[1].split('/')
    
    x = finger[2]
    model = x.split(':')[0]
    android = x.split(':')[1]
    build_id = finger[3]
    return f"BlibliAndroid/9.8.0(6029) {userId} Dalvik/2.1.0 (Linux; U; Android {android}; {model} Build/{build_id})"


class LoginBlibli:
    def __init__(self) -> None:
        self.uuid = str(uuid.uuid4())
    
    def getToken(self, email: str , sandi: str) -> dict:
        headers = {
            "Host": "account.blibli.com",
            "accept": "application/json",
            "x-userid": self.uuid,
            "x-sessionid": str(uuid.uuid4()),
            "x-requestid": str(uuid.uuid4()),
            "user-agent": random_user_agent(userId=self.uuid),
            "accept-language": "id",
            "build-no":"6029",
            "channelid": "android",
            "storeid": "10001",
            "content-type": "application/x-www-form-urlencoded",
            "accept-encoding": "gzip",
        }

        resp = requests.post(
            "https://account.blibli.com/gdn-oauth/token", headers=headers,
            data={
                "grant_type": "password",
                "username": email,
                "password": sandi,
                "client_id": "86ad3acb-9ac8-419a-9446-a5828f80137e",
                "client_secret": "q+SPZG94E=gN+Zba"
            }
        )
        res = resp.json()
        try:
            token = res['data']['challenge']['token']
            #GET OTP
            headers = omit(
                headers, "x-requestid", "Host", "content-type"
            )
            headers.update({
                "x-requestid": str(uuid.uuid4()),
                "content-type": "application/json; charset=UTF-8",
                "@": "ignore-auth",
                "Host": "www.blibli.com"
            })
            resp = requests.post(
                "https://www.blibli.com/backend/common/users/_request-challenge-code", headers=headers,
                json={
                    "challenge":{"token": token},
                    "type": "EMAIL"
                }
            )
            print('[*] Otp terkirim')
            
            otp_email = input('[*] Input otp: ')
            
            for x in range(2):
                hapus_line()
            
            
            headers = omit(headers, "x-requestid", "Host", "content-type", "@")
            headers.update({
                "x-requestid": str(uuid.uuid4()),
                "content-type": "application/x-www-form-urlencoded",
                "Host": "account.blibli.com"
            })  
            resp = requests.post(
                "https://account.blibli.com/gdn-oauth/token", headers=headers,
                data={
                    "challenge_token": token,
                    "grant_type": "mfa_otp",
                    "challenge_code": otp_email,
                    "client_secret": "q+SPZG94E=gN+Zba",
                    "client_id": "86ad3acb-9ac8-419a-9446-a5828f80137e",
                    "username": email
                }
            )
            res = resp.json()            
            try:
                accces_token = res['access_token']
                print('[*] Login sukses')
                return {
                    'access_token': accces_token,
                    'user_id': headers["x-userid"],
                    'session_id': headers["x-sessionid"],
                    'user_agent': headers['user-agent']
                }
                
            except:
                print(f'[!] Error => {res}')
            
        except:
            print(f'[!] Error => {res}')
        




class Tuku:
    def __init__(
        self, email, access_token, user_id, session_id, user_agent
    ) -> None:
        self.model_hp = user_agent.split()[-2]
        self.cookies = {
            'Blibli-Access-Token': access_token,
            'Blibli-Device-Model': self.model_hp,
            'Blibli-Device-ID': user_id,
        }
        self.user_agent = user_agent
        self.session_id = session_id
        self.email = email
        
    
    def cek_vocher(self):
        headers = {
            "Host": "www.blibli.com",
            "accept": "application/json",
            "x-blibli-user-email": self.email,
            "x-userid": self.cookies['Blibli-Device-ID'],
            "x-sessionid": self.session_id,
            "user-agent": self.user_agent,
            "build-no": "6029",
            "authorization": f"bearer {self.cookies['Blibli-Access-Token']}",
            "channelid": "android",
            "storeid": "10001",
            "content-type": "application/json; charset=UTF-8",
            "accept-encoding": "gzip",
            "accept-language": "id",
            "x-requestid":str(uuid.uuid4())
        }
        resp = requests.get(
            'https://www.blibli.com/backend/member-voucher/vouchers?origin=BLIBLI&itemPerPage=25', headers=headers
        )
        try:
            vochermu = []
            hasil = resp.json()['data']
            for i, x in enumerate(hasil):
                i += 1
                vochermu.append((i, x))
            
            if len(vochermu) == 0:
                print(f'[!] Vocher kosong')
            else:
                print(f'[*] Pilih vocher')
                for x in vochermu:
                    print(f'    {x[0]}. {x[1]["name"]}')
                while True:
                    try:
                        pilih = input(f"Pilihamu: ")
                        if int(pilih) <= len(vochermu):
                            hapus_line()
                            break
                        hapus_line()
                    except:
                        hapus_line()
                        continue
                
                
                jum = len(vochermu) + 1
                for _ in range(jum):
                    hapus_line()
                pilihan = [x[1] for x in vochermu if int(pilih) == int(x[0])][0]
                persen = int(pilihan['rewardMessage'].split(' ')[-1].replace('%', ''))
                maxs = int(pilihan['maximumDiscount'].split('Rp')[1].replace('.', ''))        
                harga = cari_harga(persen=persen, maxs=maxs)
                print(f'[*] Pilihanmu {pilihan["name"]}')
                return {
                    'code_vocher': pilihan["code"],
                    'harga': harga,
                }
        except:
            print('[!] Error => Ra enek vocher')

    def co_paper(self, list_data: dict):
        headers = {
            'Host': 'www.blibli.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en',
            'X-Requested-With': 'blibli.mobile.commerce',
            'Accept-Encoding': 'gzip, deflate',
        }
        params = (
            ('appsWebview', 'true'),
            ('exitOnBack-ccc42d8f-362f-4ffe-89e4-82f97a325c1b', '1'),
        )
        resp = requests.get(
            'https://www.blibli.com/digital/p/invoicing/paper-id', headers=headers, params=params, cookies=self.cookies
        )
        hasil = resp.cookies.get_dict()
        self.cookies.update({
            'ak_bmsc': hasil['ak_bmsc']
        })
        
        headers = {
            'Host': 'www.blibli.com',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': self.user_agent,
            'Referer': 'https://www.blibli.com/digital/p/invoicing/paper-id?appsWebview=true&exitOnBack-ccc42d8f-362f-4ffe-89e4-82f97a325c1b=1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en,en-US;q=0.9',
        }        
        resp = requests.get('https://www.blibli.com/backend/common/users', headers=headers, cookies=self.cookies)
        data = resp.cookies.get_dict()
        self.cookies.update(data)
        
        
        harga = list_data['harga']
        kode_vocher = list_data['code_vocher']
        
        print('[*] Generate kode paper')
        kode_paper = GeneratePaper(harga=harga).running()
        # print(f'    ● kode: {kode_paper[0]}  ● url: {kode_paper[1]}')
        
        resp = requests.post(
            'https://www.blibli.com/backend/digital-product/carts/_customer-number', headers=headers, cookies=self.cookies,json={
                "customerNumber": kode_paper[0],
                "operatorName": "Paper id",
                "productType": "INVOICING"
            }
        )        

        resp = requests.post(
            "https://www.blibli.com/backend/digital-product/coupons/_apply", headers=headers, cookies=self.cookies, json={
                "id": kode_vocher
            }
        )
        
        hasil = resp.json()
        try:
            print(f"[!] Error => {hasil['errors']}")
        except:
            resp = requests.put(
                'https://www.blibli.com/backend/digital-product/carts/_payment',headers=headers, cookies=self.cookies, json={
                    "paymentMethod": "BNIVA"
                }
            )
            data = resp.json()["data"]
            print('[*] Info checkout')
            print(f'    ● produk: {data["inquiryInfo"]["operator"]["name"]}')            
            print(f"    ● kode: {data['customerNumber']}")
            print(f"    ● customer: {data['inquiryInfo']['additionalData']['CUSTOMER_EMAIL']}")
            print(f"    ● company: {data['inquiryInfo']['additionalData']['COMPANY_EMAIL']}")
            print(f"    ● apply vocher: {data['appliedCouponAndValue'][0]['name']}")
            print(f"    ● casback: Rp.{int(data['walletCashbackAmount'])}")    
            
            
            resp = requests.post(
                'https://www.blibli.com/backend/digital-product/orders', headers=headers, cookies=self.cookies, json={
                    "extendedData":{
                        "PAYMENT_ACTION":"NORMAL"
                    }
                }
            )
            hasil = resp.json()
            order_id = hasil['data']["orderId"]

            resp = requests.get(
                f"https://www.blibli.com/backend/digital-product/orders/{order_id}", headers=headers, cookies=self.cookies
            )
            result = resp.json()['data']
            print('[*] Info pembayaran')
            print(f'    ● Bank: {result["payment"]["description"]}')            
            print(f"    ● Total order: Rp.{int(data['inquiryInfo']['additionalData']['TOTAL_AMOUNT_WITH_ADMIN_CHARGE'])}")
            print(f'    ● NomerVa: {result["payment"]["extendedData"]["VIRTUAL_ACCOUNT_NUMBER"]}')               
            
            
    def gas_mas(self):
        hasil = self.cek_vocher()
        self.co_paper(list_data=hasil)





if __name__ == '__main__':
    clear()
    if not os.path.exists(f'{DIR}/auth.json'):
        banner2()
        email = input('[*] Email paper: ')
        sandi = input('[*] Sandi paper: ')
        GetAuth.login__(email=email.strip(), sandi=sandi.strip())
        clear()
    else:
        clear()
    banner()
    
    email = input('[*] Email blibli: ')
    sandi = input('[*] Sandi blibli: ')
    data  = (LoginBlibli().getToken(
        email=email,sandi=sandi
    ))
    # data = {
    #     'access_token': 'AT-121D583F-650C-4A2D-9444-BAE26D19C23C', 
    #     'user_id': '224bd82d-56f3-42ea-8207-9b90188280a4', 
    #     'session_id': '4b5ffb9c-0daa-4c03-8c5b-c0eef9631c30', 
    #     'user_agent': 'BlibliAndroid/9.8.0(6029) 224bd82d-56f3-42ea-8207-9b90188280a4 Dalvik/2.1.0 (Linux; U; Android 8.0.0; greatlte Build/R16NW)'
    #     }
    try:
        Tuku(
            email = email,
            access_token=data["access_token"],
            user_id=data['user_id'],
            session_id=data["session_id"],
            user_agent=data['user_agent']
        ).gas_mas()
    except:
        print('[!] Gagal total')