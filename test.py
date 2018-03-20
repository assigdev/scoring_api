import unittest
import api


class BaseFieldTestCase(unittest.TestCase):
    def setUp(self):
        class ChildBaseField(api.BaseField):
            child_error = 'have error'
            is_error = True

            def clean(self):
                if self.is_error:
                    self.errors.append(self.child_error)
        self.field_class = ChildBaseField

    def test_require_is_true(self):
        field = self.field_class(required=True)
        field._restore_errors()
        field.validate()
        self.assertEqual(field.errors, ['is require'])

    def test_require_is_false(self):
        field = self.field_class(required=False)
        field._restore_errors()
        field.is_error = False
        field.validate()
        self.assertFalse(field.errors)

    def test_nullable_is_false(self):
        field = self.field_class(required=False, nullable=False)
        field.__set__(field, [])
        field.validate()
        self.assertEqual(field.errors, ['is not nullable'])
        field.__set__(field, False)
        field.validate()
        self.assertEqual(field.errors, ['is not nullable'])
        field.__set__(field, '')
        field.validate()
        self.assertEqual(field.errors, ['is not nullable'])

    def test_nullable_is_true(self):
        field = self.field_class(required=False, nullable=True)
        field.is_error = False
        field.__set__(field, [])
        field.validate()
        self.assertFalse(field.errors)
        field.__set__(field, False)
        field.validate()
        self.assertFalse(field.errors)
        field.__set__(field, '')
        field.validate()
        self.assertFalse(field.errors)

    def test_clean_method_error_is_false(self):
        field = self.field_class(required=False, nullable=True)
        field.is_error = False
        field._restore_errors()
        field.value = 'test_text'
        field.validate()
        self.assertFalse(field.errors)

    def test_clean_method_error_is_true(self):
        field = self.field_class(required=False, nullable=True)
        field.is_error = True
        field._restore_errors()
        field.value = 'test_text'
        field.validate()
        self.assertEqual(field.errors, ['have error'])


class CharFieldTestCase(unittest.TestCase):

    def test_value_with_string(self):
        field = api.CharField(required=True, nullable=False)
        field.__set__(field, 'test text')
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_dict(self):
        field = api.CharField(required=True, nullable=False)
        field.__set__(field, {'test_key': 'test_value'})
        field.validate()
        self.assertEquals(field.errors, ['Is not a string'])

    def test_value_with_int(self):
        field = api.CharField(required=True, nullable=False)
        field.__set__(field, 1)
        field.validate()
        self.assertEquals(field.errors, ['Is not a string'])

    def test_value_with_list(self):
        field = api.CharField(required=True, nullable=False)
        field.__set__(field, [1])
        field.validate()
        self.assertEquals(field.errors, ['Is not a string'])


class ArgumentsFieldTestCase(unittest.TestCase):

    def test_value_with_string(self):
        field = api.ArgumentsField(required=True, nullable=False)
        field.__set__(field, 'test text')
        field.validate()
        self.assertEquals(field.errors, ['Is not dict with arguments'])

    def test_value_with_dict(self):
        field = api.ArgumentsField(required=True, nullable=False)
        field.__set__(field, {'test_key': 'test_value'})
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_int(self):
        field = api.ArgumentsField(required=True, nullable=False)
        field.__set__(field, 1)
        field.validate()
        self.assertEquals(field.errors, ['Is not dict with arguments'])

    def test_value_with_list(self):
        field = api.ArgumentsField(required=True, nullable=False)
        field.__set__(field, [1])
        field.validate()
        self.assertEquals(field.errors, ['Is not dict with arguments'])


class EmailFieldTestCase(unittest.TestCase):

    def test_value_with_string(self):
        field = api.EmailField(required=True, nullable=False)
        field.__set__(field, 'test text')
        field.validate()
        self.assertEquals(field.errors, ['Is not email'])

    def test_value_with_dict(self):
        field = api.EmailField(required=True, nullable=False)
        field.__set__(field, {'test_key': 'test_value'})
        field.validate()
        self.assertEquals(field.errors, ['Is not a string'])

    def test_value_with_int(self):
        field = api.EmailField(required=True, nullable=False)
        field.__set__(field, 1)
        field.validate()
        self.assertEquals(field.errors, ['Is not a string'])

    def test_value_with_list(self):
        field = api.EmailField(required=True, nullable=False)
        field.__set__(field, [1])
        field.validate()
        self.assertEquals(field.errors, ['Is not a string'])

    def test_value_with_email(self):
        field = api.EmailField(required=True, nullable=False)
        field.__set__(field, 'tester@gmail.com')
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_bad_email(self):
        field = api.EmailField(required=True, nullable=False)
        field.__set__(field, 'testergmail.com')
        field.validate()
        self.assertEquals(field.errors, ['Is not email'])


class PhoneFieldTestCase(unittest.TestCase):

    def test_value_with_string(self):
        field = api.PhoneField(required=True, nullable=False)
        field.__set__(field, 'test text')
        field.validate()
        self.assertEquals(field.errors, ['Is not phone number'])

    def test_value_with_dict(self):
        field = api.PhoneField(required=True, nullable=False)
        field.__set__(field, {'test_key': 'test_value'})
        field.validate()
        self.assertEquals(field.errors, ['Is not phone number'])

    def test_value_with_int(self):
        field = api.PhoneField(required=True, nullable=False)
        field.__set__(field, 1)
        field.validate()
        self.assertEquals(field.errors, ['Is not phone number'])

    def test_value_with_list(self):
        field = api.PhoneField(required=True, nullable=False)
        field.__set__(field, [1])
        field.validate()
        self.assertEquals(field.errors, ['Is not phone number'])

    def test_value_is_true_phone(self):
        field = api.PhoneField(required=True, nullable=False)
        field.__set__(field, 79644261355)
        field.validate()
        self.assertFalse(field.errors)

    def test_value_is_true_phone_2(self):
        field = api.PhoneField(required=True, nullable=False)
        field.__set__(field, '79644261355')
        field.validate()
        self.assertFalse(field.errors)

    def test_value_is_false_phone(self):
        field = api.PhoneField(required=True, nullable=False)
        field.__set__(field, 7964426135)
        field.validate()
        self.assertEquals(field.errors, ['Is not phone number'])

    def test_value_is_false_phone_2(self):
        field = api.PhoneField(required=True, nullable=False)
        field.__set__(field, '89634261355')
        field.validate()
        self.assertEquals(field.errors, ['Is not phone number'])

    def test_value_is_false_phone_3(self):
        field = api.PhoneField(required=True, nullable=False)
        field.__set__(field, '7963426135_')
        field.validate()
        self.assertEquals(field.errors, ['Is not phone number'])

    def test_value_is_false_phone_4(self):
        field = api.PhoneField(required=True, nullable=False)
        field.__set__(field, 7963426.1355)
        field.validate()
        self.assertEquals(field.errors, ['Is not phone number'])

    def test_value_is_false_phone_5(self):
        field = api.PhoneField(required=True, nullable=False)
        field.__set__(field, 79634261355.5)
        field.validate()
        self.assertEquals(field.errors, ['Is not phone number'])


class DateFieldTestCase(unittest.TestCase):

    def test_value_with_string(self):
        field = api.DateField(required=True, nullable=False)
        field.__set__(field, 'test text')
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])

    def test_value_with_dict(self):
        field = api.DateField(required=True, nullable=False)
        field.__set__(field, {'test_key': 'test_value'})
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])

    def test_value_with_int(self):
        field = api.DateField(required=True, nullable=False)
        field.__set__(field, 1)
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])

    def test_value_with_list(self):
        field = api.DateField(required=True, nullable=False)
        field.__set__(field, [1])
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])

    def test_value_with_date(self):
        field = api.DateField(required=True, nullable=False)
        field.__set__(field, '30.01.2017')
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_date_2(self):
        field = api.DateField(required=True, nullable=False)
        field.__set__(field, '1.2.2017')
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_bad_date(self):
        field = api.DateField(required=True, nullable=False)
        field.__set__(field, '1.2.17')
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])

    def test_value_with_bad_date_2(self):
        field = api.DateField(required=True, nullable=False)
        field.__set__(field, '01.02.17')
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])

    def test_value_with_bad_date_3(self):
        field = api.DateField(required=True, nullable=False)
        field.__set__(field, '2017.2017.2017')
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])

    def test_value_with_bad_date_4(self):
        field = api.DateField(required=True, nullable=False)
        field.__set__(field, '10.2017')
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])


class BirthDayFieldTestCase(unittest.TestCase):

    def test_value_with_string(self):
        field = api.BirthDayField(required=True, nullable=False)
        field.__set__(field, 'test text')
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])

    def test_value_with_dict(self):
        field = api.BirthDayField(required=True, nullable=False)
        field.__set__(field, {'test_key': 'test_value'})
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])

    def test_value_with_int(self):
        field = api.BirthDayField(required=True, nullable=False)
        field.__set__(field, 1)
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])

    def test_value_with_list(self):
        field = api.BirthDayField(required=True, nullable=False)
        field.__set__(field, [1])
        field.validate()
        self.assertEquals(field.errors, ['Is note date'])

    def test_value_with_true_birthday(self):
        field = api.BirthDayField(required=True, nullable=False)
        field.__set__(field, '30.01.2017')
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_true_birthday_2(self):
        field = api.BirthDayField(required=True, nullable=False)
        field.__set__(field, '30.12.1948')
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_false_birthday(self):
        field = api.BirthDayField(required=True, nullable=False)
        field.__set__(field, '25.12.1947')
        field.validate()
        self.assertEquals(field.errors, ['Not a birthday'])


class GenderFieldTestCase(unittest.TestCase):

    def test_value_with_string(self):
        field = api.GenderField(required=True, nullable=False)
        field.__set__(field, 'test text')
        field.validate()
        self.assertEquals(field.errors, ['is not a gender number'])

    def test_value_with_dict(self):
        field = api.GenderField(required=True, nullable=False)
        field.__set__(field, {'test_key': 'test_value'})
        field.validate()
        self.assertEquals(field.errors, ['is not a gender number'])

    def test_value_with_int(self):
        field = api.GenderField(required=True, nullable=False)
        field.__set__(field, 2)
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_list(self):
        field = api.GenderField(required=True, nullable=False)
        field.__set__(field, [1])
        field.validate()
        self.assertEquals(field.errors, ['is not a gender number'])

    def test_value_with_true_gender(self):
        field = api.GenderField(required=True, nullable=False)
        field.__set__(field, 0)
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_true_gender_2(self):
        field = api.GenderField(required=True, nullable=False)
        field.__set__(field, 1)
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_false_gender(self):
        field = api.GenderField(required=True, nullable=False)
        field.__set__(field, '3')
        field.validate()
        self.assertEquals(field.errors, ['is not a gender number'])

    def test_value_with_false_gender_2(self):
        field = api.GenderField(required=True, nullable=False)
        field.__set__(field, 3)
        field.validate()
        self.assertEquals(field.errors, ['is not a gender number'])

    def test_value_with_false_gender_3(self):
        field = api.GenderField(required=True, nullable=False)
        field.__set__(field, 4)
        field.validate()
        self.assertEquals(field.errors, ['is not a gender number'])


class ClientIDsFieldTestCase(unittest.TestCase):

    def test_value_with_string(self):
        field = api.ClientIDsField(required=True, nullable=False)
        field.__set__(field, 'test text')
        field.validate()
        self.assertEquals(field.errors, ['Is not list of client ids'])

    def test_value_with_dict(self):
        field = api.ClientIDsField(required=True, nullable=False)
        field.__set__(field, {'test_key': 'test_value'})
        field.validate()
        self.assertEquals(field.errors, ['Is not list of client ids'])

    def test_value_with_int(self):
        field = api.ClientIDsField(required=True, nullable=False)
        field.__set__(field, 2)
        field.validate()
        self.assertEquals(field.errors, ['Is not list of client ids'])

    def test_value_with_list(self):
        field = api.ClientIDsField(required=True, nullable=False)
        field.__set__(field, [1])
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_true_gender(self):
        field = api.ClientIDsField(required=True, nullable=False)
        field.__set__(field, [1, 2, 10, 3, 4, 5, 6, 90])
        field.validate()
        self.assertFalse(field.errors)

    def test_value_with_false_gender(self):
        field = api.ClientIDsField(required=True, nullable=False)
        field.__set__(field, [])
        field.validate()
        self.assertEquals(field.errors, ['is not nullable'])

    def test_value_with_false_gender_2(self):
        field = api.ClientIDsField(required=True, nullable=False)
        field.__set__(field, [3, '3', '44'])
        field.validate()
        self.assertEquals(field.errors, ['Is not list of client ids'])

    def test_value_with_false_gender_3(self):
        field = api.ClientIDsField(required=True, nullable=False)
        field.__set__(field, [1, [12, 3]])
        field.validate()
        self.assertEquals(field.errors, ['Is not list of client ids'])

    def test_value_with_false_gender_4(self):
        field = api.ClientIDsField(required=True, nullable=False)
        field.__set__(field, (1,))
        field.validate()
        self.assertEquals(field.errors, ['Is not list of client ids'])


def cases(case_list):
    def decorator(func):
        def wrapper(self):
            result = []
            for case in case_list:
                result.append(func(self, case))
            return result
        return wrapper
    return decorator


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.context = {}
        self.headers = {}
        self.store = None

    def get_response(self, request):
        return api.method_handler({"body": request, "headers": self.headers}, self.context, self.store)

    def test_empty_request(self):
        _, code = self.get_response({})
        self.assertEqual(api.INVALID_REQUEST, code)

    @cases([
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "", "arguments":
            {}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "sdd",
         "arguments": {}},
        {"account": "horns&hoofs", "login": "admin", "method": "online_score", "token": "", "arguments":
            {}},
        {"account": "horns&hoofs", "login": "user", "method": "clients_interests",
         "token": "b52c9f8e9c28b90e93edd9b2e60ad46f1ee7913d8dacbe6878271950660579955e9cc02e13f6a9a3c492ef006b0be9f7c9b7f0015c3110447ce2b0f918d9f0f8",
         "arguments": {"client_ids": [1, 2, 3, 4], "date": "20.07.2017"}}
    ])
    def test_bad_auth(self, request):
        _, code = self.get_response(request)
        self.assertEqual(api.FORBIDDEN, code)

    @cases([
        {"account": "horns&hoofs", "login": "user", "method": "clients_interests",
         "arguments": {"client_ids": [1, 2, 3, 4], "date": "20.07.2017"}},
        {"account": "horns&hoofs", "login": "admin", "method": "online_score",
         "arguments": {}},
    ])
    def test_token_require(self, request):
        _, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code)

    @cases([
        {"account": "horns&hoofs", "login": "h&f", "method": "online",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": "score",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": {}},
    ])
    def test_method_not_found(self, request):
        _, code = self.get_response(request)
        self.assertEqual(api.NOT_FOUND, code)


class TestSuiteWithStore(unittest.TestCase):
    def setUp(self):
        self.context = {}
        self.headers = {}
        self.store = api.Store(api.DEFAULT_CACHE_CLIENT, api.DEFAULT_CACHE_ADDRESS)

    def get_response(self, request):
        return api.method_handler({"body": request, "headers": self.headers}, self.context, self.store)

    @cases([
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": {"phone": 79175002040, "email": "test@otus.ru", "first_name": "TestName",
                       "last_name": "TestSurname", "birthday": "01.01.1990", "gender": 1}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": {"phone": "79175002040", "email": "tester@otus.ru", "first_name": "TestName",
                       "last_name": "TestSurname", "birthday": "01.01.1965", "gender": 1}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": {"phone": "79175002040", "email": "tester@otus.ru", }},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": {"birthday": "01.01.1990", "gender": 1 }},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": {"first_name": "TestName", "last_name": "TestSurname",}},
    ])
    def test_valid_request(self, request):
        _, code = self.get_response(request)
        self.assertEqual(api.OK, code)

    @cases([
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": {"phone": 79175002040, "email": "test@otus.ru", "first_name": "TestName",
                       "last_name": 120, "birthday": "01.01.1990", "gender": 1}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": {"phone": "79175002040", "email": "tester@otus.ru", "first_name": "TestName",
                       "last_name": "TestSurname", "birthday": "01.01.1965", "gender": 10}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": {"phone": "79175002040", "last_name": "TestSurname", "gender": 10}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": { }},
        {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests",
         "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
         "arguments": {"client_ids": 10, "date": "20.07.2017"}},
    ])
    def test_invalid_request(self, request):
        _, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code)


if __name__ == "__main__":
    unittest.main()
