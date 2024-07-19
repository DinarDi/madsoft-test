import json
from pathlib import Path

import pytest
from httpx import Response

file_to_upload = Path(__file__).parent / '2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg'


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    'data_for_mocker, payload, file, expected',
    [
        (
                Response(
                    status_code=201,
                    json={
                        'img_link': 'localhost:9000/test/string2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg'
                    },

                ),
                json.dumps({
                    'title': 'testexample',
                    'description': 'Test description'
                }, ),
                True,
                {
                    'status_code': 201,
                    'data': {
                        "title": "testexample",
                        "description": "Test description",
                        "img_url": 'localhost:9000/test/string2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg',
                        "id": 1
                    }
                }
        ),
    ]
)
async def test_post_ok(
        client,
        mocker,
        data_for_mocker,
        payload,
        file,
        expected,
):
    mocker.patch(
        's3connect.s3connect.create_file',
        return_value=Response(
            status_code=201,
            json={
                'img_link': 'localhost:9000/test/string2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg'
            },
        ),
    )

    response = await client.post(
        '/api/v1/memes/',
        files={
            'file': open(file_to_upload, 'rb')
        },
        data={
            'payload': payload
        },
        headers={
            'content_type': 'multipart/form-data'
        }
    )

    assert response.status_code == expected.get('status_code')
    assert response.json()['data'] == expected['data']


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    'data_for_mocker, payload, file, expected',
    [
        (
                Response(
                    status_code=500,
                    json={
                        'detail': {
                            'error_message': 'Something went wrong'
                        }
                    },
                ),
                json.dumps({
                    'title': 'testexample',
                    'description': 'Test description'
                }, ),
                True,
                {
                    'status_code': 500,
                    'detail': {
                        'error_message': 'Something went wrong'
                    }
                }
        ),
        (
                Response(
                    status_code=201,
                    json={
                        'img_link': 'localhost:9000/test/string2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg'
                    },
                ),
                json.dumps({
                    'title': 'Test example',
                    'description': 'Test description'
                }, ),
                True,
                {
                    'status_code': 422,
                    'detail': {
                        'error_message': 'Title must contain only a-z and 0-9'
                    }
                }
        )
    ]
)
async def test_post_wrong(
        client,
        mocker,
        data_for_mocker,
        payload,
        file,
        expected
):
    mocker.patch(
        's3connect.s3connect.create_file',
        return_value=data_for_mocker
    )

    response = await client.post(
        '/api/v1/memes/',
        files={
            'file': open(file_to_upload, 'rb')
        },
        data={
            'payload': payload
        },
        headers={
            'content_type': 'multipart/form-data'
        }
    )

    assert response.status_code == expected.get('status_code')
    assert response.json()['detail'] == expected.get('detail')


@pytest.mark.asyncio()
async def test_get_memes(
        client,
        mocker,
):
    mocker.patch(
        's3connect.s3connect.create_file',
        return_value=Response(
            status_code=201,
            json={
                'img_link': 'localhost:9000/test/string2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg'
            },
        ),
    )
    await client.post(
        '/api/v1/memes/',
        files={
            'file': open(file_to_upload, 'rb')
        },
        data={
            'payload': json.dumps({
                'title': 'testtitle',
                'description': 'Test description'
            })
        },
        headers={
            'content_type': 'multipart/form-data'
        }
    )
    expected_data = {
        'page': 1,
        'limit': 10,
        'data': [
            {
                'title': 'testtitle',
                'description': 'Test description',
                'img_url': 'localhost:9000/test/string2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg',
                'id': 1
            },
        ]
    }
    response = await client.get('/api/v1/memes/')
    assert response.status_code == 200
    assert response.json() == expected_data


@pytest.mark.asyncio
async def test_get_meme(
        client,
        mocker,
):
    mocker.patch(
        's3connect.s3connect.create_file',
        return_value=Response(
            status_code=201,
            json={
                'img_link': 'localhost:9000/test/string2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg'
            },
        ),
    )
    res = await client.post(
        '/api/v1/memes/',
        files={
            'file': open(file_to_upload, 'rb')
        },
        data={
            'payload': json.dumps({
                'title': 'testtitle',
                'description': 'Test description'
            })
        },
        headers={
            'content_type': 'multipart/form-data'
        }
    )
    expected_data = {
        'data': {
            'title': 'testtitle',
            'description': 'Test description',
            'img_url': 'localhost:9000/test/string2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg',
            'id': res.json()['data']['id']
        },
    }

    response = await client.get(f'/api/v1/memes/{res.json()['data']['id']}')
    assert response.status_code == 200
    assert response.json() == expected_data


@pytest.mark.asyncio
async def test_get_meme_wrong(
        client,
        mocker,
):
    mocker.patch(
        's3connect.s3connect.create_file',
        return_value=Response(
            status_code=201,
            json={
                'img_link': 'localhost:9000/test/string2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg'
            },
        ),
    )
    res = await client.post(
        '/api/v1/memes/',
        files={
            'file': open(file_to_upload, 'rb')
        },
        data={
            'payload': json.dumps({
                'title': 'testtitle',
                'description': 'Test description'
            })
        },
        headers={
            'content_type': 'multipart/form-data'
        }
    )
    expected_data = {
        'error_message': 'Meme not found'
    }

    response = await client.get('/api/v1/memes/10')
    assert response.status_code == 404
    assert response.json()['detail'] == expected_data


@pytest.mark.asyncio
async def test_update_meme(
        client,
        mocker
):
    mocker.patch(
        's3connect.s3connect.create_file',
        return_value=Response(
            status_code=201,
            json={
                'img_link': 'localhost:9000/test/string2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg'
            },
        ),
    )
    res = await client.post(
        '/api/v1/memes/',
        files={
            'file': open(file_to_upload, 'rb')
        },
        data={
            'payload': json.dumps({
                'title': 'testtitle',
                'description': 'Test description'
            })
        },
        headers={
            'content_type': 'multipart/form-data'
        }
    )

    payload = {
        'title': 'newtitle'
    }
    response = await client.put(
        f'/api/v1/memes/{res.json()['data']['id']}',
        data={
            'payload': json.dumps(payload)
        }
    )

    assert response.status_code == 200
    assert response.json()['data']['title'] == payload['title']


@pytest.mark.asyncio
async def test_delete_meme(
        client,
        mocker,
):
    mocker.patch(
        's3connect.s3connect.create_file',
        return_value=Response(
            status_code=201,
            json={
                'img_link': 'localhost:9000/test/string2018Animals___Cats_Large_gray_cat_with_a_surprised_look_123712_.jpg'
            },
        ),
    )
    res = await client.post(
        '/api/v1/memes/',
        files={
            'file': open(file_to_upload, 'rb')
        },
        data={
            'payload': json.dumps({
                'title': 'testtitle',
                'description': 'Test description'
            })
        },
        headers={
            'content_type': 'multipart/form-data'
        }
    )

    mocker.patch(
        's3connect.s3connect.delete_file',
        return_value=Response(
            status_code=204
        ),
    )
    response = await client.delete(
        f'/api/v1/memes/{res.json()['data']['id']}',
    )
    assert response.status_code == 204
