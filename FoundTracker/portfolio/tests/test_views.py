from django.test import TestCase, Client
from django.contrib.auth.models import User
from portfolio.models import AssetClass, Currency, Operation, Pocket, Asset, AssetAllocation
from django.urls import reverse


class MainDashboardViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('main_dashboard')

    def test_get_login(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/main_dashboard.html')

    def test_get_not_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        
    def test_post(self):
        pass


class PocketViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')


        self.url = reverse('pocket')

    def test_get_with_pocket_name(self):
        """
        Test case to check the behavior of the view when a pocket name is set in the session.
        """
        # Test the behavior when the user is not logged in
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password')

        session = self.client.session
        session['pocket_name'] = 'TestPocket'
        session.save()

        # Test the behavior when the user is logged in
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('asset_classes', response.context)
        self.assertIn('currencies', response.context)
        self.assertIn('pocket_name', response.context)
        self.assertIn('operations', response.context)


    def test_post(self):

        self.client.login(username='testuser', password='password')
        session = self.client.session
        session['pocket_name'] = 'NAME'
        session.save()
        self.pocket = Pocket.objects.create(name='NAME', owner=self.user, fees = 0)
        
        response = self.client.post(self.url, {
            'operation': 'buy',
            'ticker': 'AAPL',
            'date': '2022-01-01',
            'currency': 'USD',
            'quantity': '10',
            'price': '100',
            'fee': '5',
            'comment': 'Test comment',
            'asset_class': 'Equity',
            'owner': self.user,
            'pocket_name': 'NAME'

        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/pocket.html')

        operation = Operation.objects.filter(ticker='AAPL').first()

        self.assertTrue(operation)
        self.assertEqual(operation.owner, self.user)


    def test_post_process_asset_data_first_operation(self):
        '''
        Test case to check the behavior of the view when the asset does not exist in the database and it is the first operation for the asset
        '''
        self.assertEqual(AssetAllocation.objects.all().count(), 0)
        self.client.login(username='testuser', password='password')
        session = self.client.session
        session['pocket_name'] = 'NAME'
        session.save()
        self.pocket = Pocket.objects.create(name='NAME', owner=self.user, fees = 0)
        
        response = self.client.post(self.url, {
            'operation': 'buy',
            'ticker': 'AAPL',
            'date': '2022-01-01',
            'currency': 'USD',
            'quantity': '10',
            'price': '100',
            'fee': '5',
            'comment': 'Test comment',
            'asset_class': 'Equity',
            'owner': self.user,
            'pocket_name': 'NAME'

        })


        asset = Asset.objects.filter(ticker='AAPL').first()
        self.assertTrue(asset)
        self.assertEqual(asset.name, 'Apple Inc.')
        self.assertEqual(asset.currency, 'USD')

        pocket = Pocket.objects.get(name='NAME')
        self.assertEqual(pocket.fees, 5)

        asset_allocation = AssetAllocation.objects.filter(pocket=self.pocket, asset=asset).first()
        self.assertTrue(asset_allocation)
        self.assertEqual(asset_allocation.quantity, 10)
        self.assertEqual(asset_allocation.average_price, 100)

        

    def test_post_process_asset_data_not_first_operation(self):
        self.assertEqual(AssetAllocation.objects.all().count(), 0)

        self.client.login(username='testuser', password='password')
        session = self.client.session
        session['pocket_name'] = 'NAME'
        session.save()
        self.pocket = Pocket.objects.create(name='NAME', owner=self.user, fees = 0)
    
        
        self.client.post(self.url, {
            'operation': 'buy',
            'ticker': 'AAPL',
            'date': '2022-01-01',
            'currency': 'USD',
            'quantity': '10',
            'price': '100',
            'fee': '3',
            'comment': 'Test comment',
            'asset_class': 'Equity',
            'owner': self.user,
            'pocket_name': 'NAME'
        })

        self.client.post(self.url, {
            'operation': 'buy',
            'ticker': 'AAPL',
            'date': '2022-01-01',
            'currency': 'USD',
            'quantity': '40',
            'price': '150',
            'fee': '9',
            'comment': 'Test comment',
            'asset_class': 'Equity',
            'owner': self.user,
            'pocket_name': 'NAME'
        })

        pocket = Pocket.objects.get(name='NAME')
        self.assertEqual(pocket.fees, 12)
        
        asset = Asset.objects.filter(ticker='AAPL').first()
        asset_allocation = AssetAllocation.objects.filter(pocket=self.pocket, asset=asset).first()
        self.assertEqual(asset_allocation.quantity, 50)
        self.assertEqual(asset_allocation.average_price, 140)


    def setDown(self):
        AssetClass.objects.all().delete()
        Currency.objects.all().delete()
        Operation.objects.all().delete()
        Pocket.objects.all().delete()
        Asset.objects.all().delete()
        AssetAllocation.objects.all().delete()
        User.objects.all().delete()

    


