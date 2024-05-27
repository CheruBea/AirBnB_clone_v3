#!/usr/bin/python3
"""Test for the basemodel"""
from models.base_model import BaseModel, Base
import unittest
from datetime import datetime
from uuid import UUID
import json
import os

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'test of basemodel not supported')
class TestBaseModel(unittest.TestCase):
    """Test class for the base_model class"""

    def setUp(self):
        """Set up method for the test class"""
        self.value = BaseModel

    def tearDown(self):
        """Tear down method for the test class"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_init(self):
        """Tests the initialization of the model class"""
        inst = self.value()
        self.assertIsInstance(inst, BaseModel)
        if issubclass(self.value, Base):
            self.assertIsInstance(inst, Base)

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
        self.assertEqual(new.id, i.id)
        self.assertEqual(new.created_at, i.created_at)
        self.assertEqual(new.updated_at, i.updated_at)

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
        old_updated_at = i.updated_at
        i.save()
        self.assertNotEqual(old_updated_at, i.updated_at)
        key = f"{self.value.__name__}.{i.id}"
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Testing the str method of the model"""
        i = self.value()
        self.assertEqual(str(i), f"[{self.value.__name__}] ({i.id}) {i.__dict__}")

    def test_todict(self):
        """Testing the to_dict method"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)
        # Test if it's a dict
        self.assertIsInstance(n, dict)
        # Test if to_dict contains the correct keys
        self.assertIn('id', n)
        self.assertIn('created_at', n)
        self.assertIn('updated_at', n)
        self.assertIn('__class__', n)
        # Test if to_dict contains added attributes
        inst = self.value()
        inst.firstname = 'Reggy'
        inst.lastname = 'Shicky'
        self.assertIn('firstname', inst.to_dict())
        self.assertIn('lastname', inst.to_dict())
        # Test if datetime attributes are strings in to_dict
        self.assertIsInstance(n['created_at'], str)
        self.assertIsInstance(n['updated_at'], str)
        # Test to_dict output
        datetime_ = datetime.now()
        inst.id = '012345'
        inst.created_at = inst.updated_at = datetime_
        to_dict = {
            'id': '012345',
            '__class__': 'BaseModel',
            'created_at': datetime_.isoformat(),
            'updated_at': datetime_.isoformat()
        }
        self.assertDictEqual(inst.to_dict(), to_dict)

    def test_updated_at(self):
        """Testing updated_at attribute"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime)
        old_updated_at = new.updated_at
        new.save()
        self.assertNotEqual(old_updated_at, new.updated_at)
        self.assertGreater(new.updated_at, old_updated_at)

    def test_id(self):
        """Testing id attribute of the model"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Testing created_at attribute"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

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

if __name__ == "__main__":
    unittest.main()
