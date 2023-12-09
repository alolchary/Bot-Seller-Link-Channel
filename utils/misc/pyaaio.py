import hashlib
from urllib.parse import urlencode
import httpx


class Aaio:
    API_URL = 'https://aaio.io/api/'

    def __init__(self, secret_key: str, merchant_id: str, api_key: str) -> None:
        self.secret_key = secret_key
        self.merchant_id = merchant_id
        self.api_key = api_key
        self.client = httpx.AsyncClient()

    async def api_request(self, method: str, **data):
        data.update({'merchant_id': self.merchant_id})
        response = await self.client.post(self.API_URL + method, data=data, headers={
            "Accept": "application/json",
            "X-Api-Key": self.api_key
        })
        return response.json()

    async def get_order(self, payment_id: str):
        response = await self.api_request('info-pay', order_id=payment_id)
        return response

    def build_form_url(self, amount: int, desc: str, order_id: str, currency: str = 'RUB') -> str:

        sign = f':'.join([
            str(self.merchant_id),
            str(amount),
            str(currency),
            str(self.secret_key),
            str(order_id)
        ])

        params = {
            'merchant_id': self.merchant_id,
            'amount': amount,
            'currency': currency,
            'order_id': order_id,
            'sign': hashlib.sha256(sign.encode('utf-8')).hexdigest(),
            'desc': desc,
            'lang': 'ru'
        }

        url = 'https://aaio.io/merchant/pay?' + urlencode(params)

        return url

 