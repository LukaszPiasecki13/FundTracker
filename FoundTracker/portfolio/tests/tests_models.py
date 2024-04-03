from django.test import TestCase
from django.contrib.auth.models import User
from portfolio.models import AssetClass, Currency, Operation, Pocket, Asset, AssetAllocation


class OperationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password = 'password')

    def test_create_model(self):
        operation = Operation.objects.create(
            operation_type = 'Buy',
            asset_class = 'Equity',
            ticker = 'AAPL',
            date = '2021-01-01',
            currency = 'USD',
            quantity = 10,
            price = 100,
            fee = 0,
            comment = 'Comment',
            owner = self.user
        )

        self.assertTrue(isinstance(operation, Operation))
        self.assertEqual(operation.owner, self.user)

class AssetClassModelTestCase(TestCase):
    def setUp(self):
        self.asset_class = AssetClass.objects.create(name='shares')
    
    def test_create_model(self):
        self.assertEqual(str(self.asset_class), 'shares')
        self.assertTrue(isinstance(self.asset_class, AssetClass))
    

class AssetModelTestCase(TestCase):
    def setUp(self):
        self.asset = Asset.objects.create(ticker='AAPL', name='Apple', asset_class='shares', currency='USD')

    def test_create_model(self):
        self.assertEqual(str(self.asset), 'Apple')
        self.assertTrue(isinstance(self.asset, Asset))
    

class PocketModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password = 'password')
        self.pocket = Pocket.objects.create(owner=self.user, name='Pocket', fees=0)

    def test_create_model(self):
        self.assertEqual(str(self.pocket), 'Pocket')
        self.assertTrue(isinstance(self.pocket, Pocket))
        self.assertEqual(self.pocket.owner, self.user)

class AssetAllocationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password = 'password')
        self.pocket = Pocket.objects.create(owner=self.user, name='Pocket', fees=0)
        self.asset = Asset.objects.create(ticker='AAPL', name='Apple', asset_class='shares', currency='USD')
        self.asset_allocation = AssetAllocation.objects.create(pocket=self.pocket, asset=self.asset, quantity=10, average_price=100)

    def test_create_model(self):
        self.assertTrue(isinstance(self.asset_allocation, AssetAllocation))
        self.assertEqual(self.asset_allocation.pocket, self.pocket)
        self.assertEqual(self.asset_allocation.asset, self.asset)
        self.assertEqual(self.asset_allocation.quantity, 10)
        self.assertEqual(self.asset_allocation.average_price, 100)


    def setDown(self):
        self.asset_allocation.delete()
        self.asset.delete()
        self.pocket.delete()
        self.user.delete()

    



        
