from sanic.response import json
from utility import roles_required


'''

@app.route('/')
async def handler(request):
    data = await collection.find().to_list(None)
    for doc in data:
        del doc['_id']
    return json(data)


@app.route('/del')
async def handler(request):
    data = await collection.remove()
    return text('done')

'''


def crud(blue, collection):
    """
    :param blue:
    :param collection:
    :return: crud

    '''
    GET /tickets - Retrieves a list of tickets
    GET /tickets/12 - Retrieves a specific ticket
    POST /tickets - Creates a new ticket
    PUT /tickets/12 - Updates ticket #12
    PATCH /tickets/12 - Partially updates ticket #12
    DELETE /tickets/12 - Deletes ticket #12
    '''
    """
    @blue.route('/find', methods=['GET', 'POST'])
    @roles_required(['dev'])
    async def _find(request, payload):
        query = request.form['query'] if request.form['query'] else request.args['query']
        return json(await collection.aggregate(query))

    @blue.route('/', methods=['POST'])
    @roles_required(['dev'])
    async def _post(request, payload):
        _document = document(request)
        result = await collection.inser_one(_document)
        return json({'status': 'created'}, 200)

    @blue.route('/', methods=['PUT'])
    @roles_required(['dev'])
    async def _put(request, payload):
        pass

    @blue.route('/', methods=['PATCH'])
    @roles_required(['dev'])
    async def _patch(request, payload):
        pass

    @blue.route('/', methods=['DELETE'])
    @roles_required(['dev'])
    async def _delete(request, payload):
        pass