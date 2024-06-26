#!/usr/bin/python3
"""Test for the basemodel"""
from models.base_model import BaseModel, Base
import unittest
from datetime import datetime
from uuid import UUID
import json
import os

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 'test of basemodel not supported')
class TestBaseModel(unittest.TestCase):
    """Test class for the BaseModel class"""

    def __init__(self, *args, **kwargs):
        """Initializes the test class for BaseModel"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """Set up method for the test class"""
        pass

    def tearDown(self):
        """Teardown method for the test class"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_init(self):
        """Tests the initialization of the model class"""
        self.assertIsInstance(self.value(), BaseModel)
        if self.value is not BaseModel:
            self.assertIsInstance(self.value(), Base)
        else:
            self.assertNotIsInstance(self.value(), Base)

    def test_default(self):
        """Default testing for the BaseModel"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Testing BaseModel with kwargs"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Testing with specifically int kwargs"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """Testing save method"""
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Testing the str method of the model"""
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """Testing the to_dict method"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)
        # Test if it's a dict
        self.assertIsInstance(self.value().to_dict(), dict)
        # Test if to_dict contains the correct keys
        self.assertIn('id', self.value().to_dict())
        self.assertIn('created_at', self.value().to_dict())
        self.assertIn('updated_at', self.value().to_dict())
        # Test if to_dict contains added attributes
        inst = self.value()
        inst.firstname = 'Reggy'
        inst.lastname = 'Shicky'
        self.assertIn('firstname', inst.to_dict())
        self.assertIn('lastname', inst.to_dict())
        self.assertIn('firstname', self.value(firstname='Beatrice').to_dict())
        self.assertIn('lastname', self.value(lastname='Cheruto').to_dict())
        # Tests to_dict datetime attributes if they are strings
        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)
        # Tests to_dict output
        datetime_ = datetime.today()
        inst = self.value()
        inst.id = '012345'
        inst.created_at = inst.updated_at = datetime_
        to_dict = {
            'id': '012345',
            '__class__': inst.__class__.__name__,
            'created_at': datetime_.isoformat(),
            'updated_at': datetime_.isoformat(),
            'firstname': 'Reggy',
            'lastname': 'Shicky'
        }
        self.assertDictEqual(inst.to_dict(), to_dict)
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertDictEqual(
               self.value(id='v-c45', age=13).to_dict(),
               {
                   '__class__': inst.__class__.__name__,
                   'id': 'v-c45',
                   'age': 13
               }
            )

            self.assertDictEqual(
                self.value(id='v-c45', age=None).to_dict(),
                {
                    '__class__': inst.__class__.__name__,
                    'id': 'v-c45',
                    'age': None
                }
            )
        # Test to_dict output contradiction
        mdl = self.value()
        self.assertIn('__class__', self.value().to_dict())
        self.assertNotIn('__class__', self.value().__dict__)
        self.assertNotEqual(mdl.to_dict(), mdl.__dict__)
        self.assertNotEqual(
            mdl.to_dict()['__class__'],
            mdl.__class__
        )
        # Tests to_dict with args
        with self.assertRaises(TypeError):
            self.value().to_dict(None)
        with self.assertRaises(TypeError):
            self.value().to_dict(self.value())
        with self.assertRaises(TypeError):
            self.value().to_dict(35)
        self.assertNotIn('_sa_instance_state', n)

    def test_kwargs_none(self):
        """Testing kwargs with None"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """Testing kwargs with one arg"""
        n = {'name': 'test'}
        new = self.value(**n)
        self.assertEqual(new.name, n['name'])

    def test_id(self):
        """Testing id attribute of the model"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Testing created_at attribute"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """Testing updated_at attribute"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

if __name__ == '__main__':
    unittest.main()

