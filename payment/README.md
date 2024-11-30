## Setup
- create a stripe account, get Api keys
- Add produts in product catalogue
- get price_id and add to model in payment plan
- setup backend url webhook in `developers/events/` and also endpoint signing secret
- Port forward in Vs-code since we need https to make requests 
- attach forwarded backend port to frontend post request

```
credit card 4242 4242 4242 4242 with a valid expired date in the future.
```
[Stripe react and django blog]('https://medium.com/@ato.deshi/stripe-subscriptions-with-django-and-react-76dcf201d84b')