from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
    'hotel_id': "1",
    'nome': 'Alpha Hotel',
    'estrelas': 3.0,
    'diaria': 300.0,
    'cidade': 'Curitiba',
    'estado': 'PR'
    }, 
    {
    'hotel_id': "2",
    'nome': 'Ryan Hotel',
    'estrelas': 4.0,
    'diaria': 400.0,
    'cidade': 'Manaus',
    'estado': 'AM'
    },
    {
    'hotel_id': "3",
    'nome': 'Rei Hotel',
    'estrelas': 5.0,
    'diaria': 500.0,
    'cidade': 'Santa Catarina',
    'estado': 'SC'
    }
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    argumentos.add_argument('estado')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404
    
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': 'Hotel id {} already exists.'.format(hotel_id)}, 400
        
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 200

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return  hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return  {'message': 'Hotel deleted'}, 200 
        return  {'message': 'Hotel not found'}, 404