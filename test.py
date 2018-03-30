import unittest
import api
import functools


def cases(case_list):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            for case in case_list:
                new_args = args + (case,)
                try:
                    func(*new_args)
                except AssertionError:
                    print "Error in case: %s" % (case,)
                    raise
            return
        return wrapper
    return decorator


class BaseFieldTestCase(unittest.TestCase):
    def setUp(self):
        class ChildBaseField(api.BaseField):
            child_error = 'have error'
            is_error = True

            def clean(self):
                if self.is_error:
                    self.errors.append(self.child_error)
        self.field_class = ChildBaseField

    @cases([
        (True, ['is require']),
        (False, []),
    ])
    def test_require(self, case):
        required, error = case
        field = self.field_class(required=required)
        field._restore_errors()
        field.validate()
        self.assertEqual(field.errors, error)

    @cases([
        (False, [], ['is not nullable']),
        (False, False, ['is not nullable']),
        (False, '', ['is not nullable']),
        (True, [], []),
        (True, False, []),
        (True, '', []),
    ])
    def test_nullable(self, case):
        nullable, value, error = case
        field = self.field_class(required=False, nullable=nullable)
        field.value = value
        field.validate()
        self.assertEqual(field.errors, error)

    @cases([
        (True, ['have error']),
        (False, []),
    ])
    def test_clean_method_error(self, case):
        status, error = case
        field = self.field_class(required=False, nullable=True)
        field.is_error = status
        field._restore_errors()
        field.value = 'test_text'
        field.validate()
        self.assertEqual(field.errors, error)


class CharFieldTestCase(unittest.TestCase):

    @cases([
        'test text',
        's'
    ])
    def test_valid_value(self, case):
        field = api.CharField(required=True, nullable=False)
        field.value = case
        field.validate()
        self.assertFalse(field.errors)

    @cases([
        ({'key': 'value'}, 'Is not a string'),
        (100, 'Is not a string'),
        (('string',), 'Is not a string'),
        ([1, 2, 3], 'Is not a string'),
        ({}, 'is not nullable'),
    ])
    def test_invalid_value_(self, case):
        value, error = case
        field = api.CharField(required=True, nullable=False)
        field.value = value
        field.validate()
        self.assertEquals(field.errors, [error])


class ArgumentsFieldTestCase(unittest.TestCase):

    @cases([
        {'test_key': 'test_value'},
        {'test_key': 'test_value', 'key2': 'value2'}
    ])
    def test_valid_value(self, case):
        field = api.ArgumentsField(required=True, nullable=False)
        field.value = case
        field.validate()
        self.assertFalse(field.errors)

    @cases([
        ('string', 'Is not dict with arguments'),
        (100, 'Is not dict with arguments'),
        (('string',), 'Is not dict with arguments'),
        ([1, 2, 3], 'Is not dict with arguments'),
        ({}, 'is not nullable'),
        ((), 'is not nullable'),
    ])
    def test_invalid_value_(self, case):
        value, error = case
        field = api.ArgumentsField(required=True, nullable=False)
        field.value = value
        field.validate()
        self.assertEquals(field.errors, [error])


class EmailFieldTestCase(unittest.TestCase):

    @cases([
        'testmail@mail.ru',
        'gmail@gmail.com',
    ])
    def test_valid_value(self, case):
        field = api.EmailField(required=True, nullable=False)
        field.value = case
        field.validate()
        self.assertFalse(field.errors)

    @cases([
        ('string', 'Is not email'),
        ('mail.ru', 'Is not email'),
        (100, 'Is not a string'),
        (('string',), 'Is not a string'),
        ([1, 2, 3], 'Is not a string'),
        ({}, 'is not nullable'),
        ((), 'is not nullable'),
    ])
    def test_invalid_value_(self, case):
        value, error = case
        field = api.EmailField(required=True, nullable=False)
        field.value = value
        field.validate()
        self.assertEquals(field.errors, [error])


class PhoneFieldTestCase(unittest.TestCase):
    @cases([
        '79634261358',
        79634261358,
    ])
    def test_valid_value(self, case):
        field = api.PhoneField(required=True, nullable=False)
        field.value = case
        field.validate()
        self.assertFalse(field.errors)

    @cases([
        ('8999934222224', 'Is not phone number'),
        ('7963426135_', 'Is not phone number'),
        (796342613.5, 'Is not phone number'),
        ([1, 2, 3], 'Is not phone number'),
        ({}, 'is not nullable'),
        ((), 'is not nullable'),
    ])
    def test_invalid_value_(self, case):
        value, error = case
        field = api.PhoneField(required=True, nullable=False)
        field.value = value
        field.validate()
        self.assertEquals(field.errors, [error])


class DateFieldTestCase(unittest.TestCase):

    @cases([
        '30.01.2017',
        '1.2.2017',
    ])
    def test_valid_value(self, case):
        field = api.DateField(required=True, nullable=False)
        field.value = case
        field.validate()
        self.assertFalse(field.errors)

    @cases([
        ('01.02.17', 'Is note date'),
        ('1.2.17', 'Is note date'),
        ('10.2017', 'Is note date'),
        ('2017.2017.2017', 'Is note date'),
        (10.2017, 'Is note date'),
        ([1, 2, 3], 'Is note date'),
        ({}, 'is not nullable'),
        ((), 'is not nullable'),
    ])
    def test_invalid_value_(self, case):
        value, error = case
        field = api.DateField(required=True, nullable=False)
        field.value = value
        field.validate()
        self.assertEquals(field.errors, [error])


class BirthDayFieldTestCase(unittest.TestCase):

    @cases([
        '30.01.2017',
        '30.12.1948',
    ])
    def test_valid_value(self, case):
        field = api.BirthDayField(required=True, nullable=False)
        field.value = case
        field.validate()
        self.assertFalse(field.errors)

    @cases([
        ('01.02.1947', 'Not a birthday'),
        ('01.02.1000', 'Not a birthday'),
        ('1.2.17', 'Is note date'),
        ('10.2017', 'Is note date'),
        ('2017.2017.2017', 'Is note date'),
        (10.2017, 'Is note date'),
        ([1, 2, 3], 'Is note date'),
        ({}, 'is not nullable'),
        ((), 'is not nullable'),
    ])
    def test_invalid_value_(self, case):
        value, error = case
        field = api.BirthDayField(required=True, nullable=False)
        field.value = value
        field.validate()
        self.assertEquals(field.errors, [error])


class GenderFieldTestCase(unittest.TestCase):

    @cases([
        2,
        1,
        0,
    ])
    def test_valid_value(self, case):
        field = api.GenderField(required=True, nullable=False)
        field.value = case
        field.validate()
        self.assertFalse(field.errors)

    @cases([
        (3, 'is not a gender number'),
        ('3', 'is not a gender number'),
        ('01.02.1947', 'is not a gender number'),
        ('test text', 'is not a gender number'),
        ('1.2.17', 'is not a gender number'),
        ({'test_key': 'test_value'}, 'is not a gender number'),
        ([1], 'is not a gender number'),
        (10.2017, 'is not a gender number'),
        ([1, 2, 3], 'is not a gender number'),
        ({}, 'is not nullable'),
        ((), 'is not nullable'),
    ])
    def test_invalid_value_(self, case):
        value, error = case
        field = api.GenderField(required=True, nullable=False)
        field.value = value
        field.validate()
        self.assertEquals(field.errors, [error])


class ClientIDsFieldTestCase(unittest.TestCase):

    @cases([
        [2],
        [1, 3, 5, 6],
        [0],
    ])
    def test_valid_value(self, case):
        field = api.ClientIDsField(required=True, nullable=False)
        field.value = case
        field.validate()
        self.assertFalse(field.errors)

    @cases([
        ([1, [2, 3]], 'Is not list of client ids'),
        (3, 'Is not list of client ids'),
        ('3', 'Is not list of client ids'),
        ('01.02.1947', 'Is not list of client ids'),
        ('test text', 'Is not list of client ids'),
        ('1.2.17', 'Is not list of client ids'),
        ({'test_key': 'test_value'}, 'Is not list of client ids'),
        (10.2017, 'Is not list of client ids'),
        ({}, 'is not nullable'),
        ((), 'is not nullable'),
        ([], 'is not nullable'),
    ])
    def test_invalid_value_(self, case):
        value, error = case
        field = api.ClientIDsField(required=True, nullable=False)
        field.value = value
        field.validate()
        self.assertEquals(field.errors, [error])


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
