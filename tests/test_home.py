from .base import BaseTests


class HomeEndpointTestCase(BaseTests):
    @classmethod
    def setUpClass(cls):
        super(HomeEndpointTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # type here the logic that evaluates ones after all tests ended
        pass

    def setUp(self):
        # here set the data you need you need unique for each test
        pass
        #  self.account_users = create_dummy_account_users(2, create_one_account_for_all=True)

    def tearDown(self):
        # the code that evaluates after each test
        pass

    def test_home_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
