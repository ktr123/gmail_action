import pytest
from emails.models import *
from response_methods import *
from loguru import logger
from django.test.client import encode_multipart, MULTIPART_CONTENT, BOUNDARY
# pytest.mark.django_db(transaction=True)
# If transcation is set to True Then It will insert into db as well
# If transcation is set to False Then It will not insert unit test data into db



@pytest.mark.django_db
def test_primitive_valid_data(end_point,
                              payload,
                              request_method,
                              formdata,
                              content_type,
                              expected_data):
    """
    Used for validating endpoints: Get and post request
    For Post Call It will validate whether the 
    endpoint is inserted in db or not
    For Get Call It will validate the response format

    """
    logger.info(f'Validating end point : {end_point}')
    end_point = end_point + '?'
    for param in payload:
        end_point = end_point + '&' + param + "=" + str(payload[param])
    # Post Method Validations
    logger.info(f'Validating End Point : {end_point}')
    if request_method == 'post' or request_method == 'put':
        if content_type == '':
            content_type = MULTIPART_CONTENT if request_method == 'post'\
                else 'application/octet-stream'
        response = server.post(end_point,
                               data=formdata,
                               HTTP_AUTHORIZATION=auth_token,
                               content_type=content_type,
                               secure=True) if request_method == 'post' \
            else server.put(end_point,
                            data=payload,
                            HTTP_AUTHORIZATION=auth_token,
                            content_type=content_type,
                            secure=True)
        validate_response_status_code(response.status_code)
        model_name = eval(list(expected_data.keys())[0])
        filter_data = list(expected_data.values())[0]
        instance = model_name.objects.filter(**filter_data).all().values()
        if not instance:
            pytest.fail('Data is not inserted into db...!!')

    # Get Method Validations
    else:
        response = server.get(
            end_point, HTTP_AUTHORIZATION=auth_token, secure=True)
        validate_response_status_code(response.status_code)
        response_content = get_response_content(response)
        if {'content_validation': False} == expected_data:
            return ' '
        if 'str' in str(type(expected_data)):
            validate_str_content(actual_data=response_content,
                                 expected_data=expected_data)
        elif 'dict' in str(type(expected_data)):
            validate_response_content(actual_response=response_content,
                                       expected_response=expected_data)
        elif ('list' in str(type(expected_data)) and len(expected_data) == 0)\
                or ('dict' in str(type(expected_data)
                                  ) and len(expected_data) == 0):
            validate_str_content(actual_data=response_content,
                                  expected_data=expected_data)
        elif 'dict' in str(type(expected_data[0])):
            validate_response_content(actual_response=response_content[0],
                                       expected_response=expected_data[0])
