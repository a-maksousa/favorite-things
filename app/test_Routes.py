import json
import unittest
from app import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    # Categories Routes Test Cases

    def test_GetAllCategories(self):
        # Get All Categories
        resp = self.client.get(path='/GetAllCategories', content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

    def test_AddCategory(self):
        # Add New Category
        resp = self.client.post(path='/AddCategory',data = dict(strCategoryTitle = 'TestCase1'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

        # Add Same Category
        resp = self.client.post(path='/AddCategory',data = dict(strCategoryTitle = 'TestCase1'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

    def test_DeleteCategory(self):
        # Add New Category
        resp = self.client.post(path='/AddCategory',data = dict(strCategoryTitle = 'TestCase2'))
        intCatID =  resp.json['data']['id']

        # Delete Category
        resp = self.client.post(path='/DeleteCategory',data = dict(id = intCatID))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

        # Delete Same Category
        resp = self.client.post(path='/DeleteCategory',data = dict(id = intCatID))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

    # Favorites Routes Test Cases

    def test_AddFavByCatID(self):
        # Add New Category
        resp = self.client.post(path='/AddCategory',data = dict(strCategoryTitle = 'TestCase3'))
        intCatID =  resp.json['data']['id']

        # Add New Favorite
        resp = self.client.post(path='/AddFavByCatID',data = dict(intCatID = intCatID, strFavoriteTitle = "TestCase3", strDescription = "Desc", intRanking = 1))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

        # Add Same Favorite
        resp = self.client.post(path='/AddFavByCatID',data = dict(intCatID = intCatID, strFavoriteTitle = "TestCase3", strDescription = "Desc", intRanking = 1))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

        # Delete Category
        resp = self.client.post(path='/DeleteCategory',data = dict(id = intCatID))

        # Add New Favorite for Deleted Category
        resp = self.client.post(path='/AddFavByCatID',data = dict(intCatID = intCatID, strFavoriteTitle = "TestCase3", strDescription = "Desc", intRanking = 1))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

    def test_GetFavByCatID(self):
        # Add New Category
        resp = self.client.post(path='/AddCategory',data = dict(strCategoryTitle = 'TestCase4'))
        intCatID =  resp.json['data']['id']

        # Add New Favorite
        resp = self.client.post(path='/AddFavByCatID',data = dict(intCatID = intCatID, strFavoriteTitle = "TestCase4", strDescription = "Desc", intRanking = 1))

        # Get Favorite by Category ID
        resp = self.client.get(path='/GetFavByCatID',query_string = dict(intCategoryID = intCatID), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)
        
        # Delete Category
        resp = self.client.post(path='/DeleteCategory',data = dict(id = intCatID))

        # Get Favorite by Deleted Category ID
        resp = self.client.get(path='/GetFavByCatID',query_string = dict(intCategoryID = intCatID), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

    def test_DeleteFavorite(self):
        # Add New Category
        resp = self.client.post(path='/AddCategory',data = dict(strCategoryTitle = 'TestCase5'))
        intCatID =  resp.json['data']['id']

        # Add New Favorite
        resp = self.client.post(path='/AddFavByCatID',data = dict(intCatID = intCatID, strFavoriteTitle = "TestCase5", strDescription = "Desc", intRanking = 1))
        intFavID = resp.json['data']['id']

        # Delete Favorite
        resp = self.client.post(path='/DeleteFavorite',data = dict(intFavID = intFavID))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

        # Delete Same Favorite
        resp = self.client.post(path='/DeleteFavorite',data = dict(intFavID = intFavID))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

    def test_UpdateFavorite(self):
        # Add New Category
        resp = self.client.post(path='/AddCategory',data = dict(strCategoryTitle = 'TestCase6'))
        intCatID =  resp.json['data']['id']

        # Add New Favorite
        resp = self.client.post(path='/AddFavByCatID',data = dict(intCatID = intCatID, strFavoriteTitle = "TestCase6", strDescription = "Desc", intRanking = 1))
        intFavID = resp.json['data']['id']

        # Update Favorite
        resp = self.client.post(path='/UpdateFavorite',data = dict(intFavID = intFavID, strTitle = "TestCase6", strDescription = "Desc", intRank = 1))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

        # Update Favorite with Same Name
        resp = self.client.post(path='/UpdateFavorite',data = dict(intFavID = intFavID, strTitle = "TestCase6", strDescription = "Desc", intRank = 1))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

        # Delete Favorite
        resp = self.client.post(path='/DeleteFavorite',data = dict(intFavID = intFavID))

        # Update Deleted Favorite
        resp = self.client.post(path='/UpdateFavorite',data = dict(intFavID = intFavID, strTitle = "TestCase6", strDescription = "Desc", intRank = 1))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

    # Meta Data Routes Test Cases

    def test_AddMetaData(self):
        # Add New Category
        resp = self.client.post(path='/AddCategory',data = dict(strCategoryTitle = 'TestCase7'))
        intCatID =  resp.json['data']['id']

        # Add New Favorite
        resp = self.client.post(path='/AddFavByCatID',data = dict(intCatID = intCatID, strFavoriteTitle = "TestCase7", strDescription = "Desc", intRanking = 1))
        intFavID = resp.json['data']['id']

        # Add New MetaData
        resp = self.client.post(path='/AddMetaData',data = dict(intFavID = intFavID, key = "TestCase7", value = "Desc", intRanking = 1))
        intFavID = resp.json['data']['id']
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

        # Delete Favorite
        resp = self.client.post(path='/DeleteFavorite',data = dict(intFavID = intFavID))

        # Add New MetaData
        resp = self.client.post(path='/AddMetaData',data = dict(intFavID = intFavID, key = "TestCase7", value = "Desc", intRanking = 1))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

    def test_GetMetaDataByFavID(self):
        # Add New Category
        resp = self.client.post(path='/AddCategory',data = dict(strCategoryTitle = 'TestCase8'))
        intCatID =  resp.json['data']['id']

        # Add New Favorite
        resp = self.client.post(path='/AddFavByCatID',data = dict(intCatID = intCatID, strFavoriteTitle = "TestCase8", strDescription = "Desc", intRanking = 1))
        intFavID = resp.json['data']['id']

        # Add New MetaData
        resp = self.client.post(path='/AddMetaData',data = dict(intFavID = intFavID, key = "TestCase8", value = "Desc", intRanking = 1))

        # Get MetaData
        resp = self.client.get(path='/GetMetaDataByFavID',query_string = dict(intFavoriteID = intFavID), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

        # Delete Favorite
        resp = self.client.post(path='/DeleteFavorite',data = dict(intFavID = intFavID))

        # Get MetaData
        resp = self.client.get(path='/GetMetaDataByFavID',query_string = dict(intFavoriteID = intFavID), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

    def test_DeleteMetaData(self):
        # Add New Category
        resp = self.client.post(path='/AddCategory',data = dict(strCategoryTitle = 'TestCase9'))
        intCatID =  resp.json['data']['id']

        # Add New Favorite
        resp = self.client.post(path='/AddFavByCatID',data = dict(intCatID = intCatID, strFavoriteTitle = "TestCase9", strDescription = "Desc", intRanking = 1))
        intFavID = resp.json['data']['id']

        # Add New MetaData
        resp = self.client.post(path='/AddMetaData',data = dict(intFavID = intFavID, key = "TestCase9", value = "Desc", intRanking = 1))
        intMetaDataID = resp.json['data']['id']

        # Delete Meta Data for Incorrect Favorite
        resp = self.client.post(path='/DeleteMetaData',data = dict(intFavID = 0, intMetaDataID = intMetaDataID))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

        # Delete Same Meta Data for Incorrect Category
        resp = self.client.post(path='/DeleteMetaData',data = dict(intFavID = intFavID, intMetaDataID = 0))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

        # Delete Meta Data
        resp = self.client.post(path='/DeleteMetaData',data = dict(intFavID = intFavID, intMetaDataID = intMetaDataID))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

        # Delete Same Meta Data
        resp = self.client.post(path='/DeleteMetaData',data = dict(intFavID = intFavID, intMetaDataID = intMetaDataID))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

    def test_UpdateMetaData(self):
        # Add New Category
        resp = self.client.post(path='/AddCategory',data = dict(strCategoryTitle = 'TestCase10'))
        intCatID =  resp.json['data']['id']

        # Add New Favorite
        resp = self.client.post(path='/AddFavByCatID',data = dict(intCatID = intCatID, strFavoriteTitle = "TestCase10", strDescription = "Desc", intRanking = 1))
        intFavID = resp.json['data']['id']

        # Add New MetaData
        resp = self.client.post(path='/AddMetaData',data = dict(intFavID = intFavID, key = "TestCase9", value = "Desc", intRanking = 1))
        intMetaDataID = resp.json['data']['id']

        # Update MetaData
        resp = self.client.post(path='/UpdateMetaData',data = dict(intFavID = intFavID,intMetaDataID = intMetaDataID, key = "TestCase10", value = "Desc", intRanking = 1))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

        # Delete Meta Data
        resp = self.client.post(path='/DeleteMetaData',data = dict(intFavID = intFavID, intMetaDataID = intMetaDataID))

        # Update Same MetaData
        resp = self.client.post(path='/UpdateMetaData',data = dict(intFavID = intFavID,intMetaDataID = intMetaDataID, key = "TestCase10", value = "Desc", intRanking = 1))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 0)

    # Logs Routes Test Cases

    def test_GetLogs(self):
        resp = self.client.get(path="/GetLogs", content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)

    def test_ClearLogs(self):
        resp = self.client.post(path="/ClearLogs", content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['code'], 1)