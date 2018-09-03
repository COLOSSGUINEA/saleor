import os
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from amazon.api import AmazonAPI # https://github.com/yoavaviram/python-amazon-simple-product-api
from saleor.product.models import Category, ProductType, Product


class Command(BaseCommand):
    help = 'Fetch data from amazon'
    
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
    AWS_ASSOCIATE_TAG = os.environ.get('AWS_ASSOCIATE_TAG', None)
    AWS_REGION = os.environ.get('AWS_ASSOCIATE_TAG', 'FR')

    # the search index on amazon
    SearchIndex = (
        'All',
        'Appareil',
        'Appliances',
        'ArtsAndCrafts',
        'Automotive',
        'Baby',
        'Beauty',
        'Blended',
        'Books',
        'Classical',
        'Collectibles',
        'DVD',
        'DigitalMusic',
        'Electronics',
        'GiftCards',
        'GourmetFood',
        'Grocery',
        'HealthPersonalCare',
        'HomeGarden',
        'Industrial',
        'Jewelry',
        'KindleStore',
        'Kitchen',
        'LawnAndGarden',
        'Marketplace',
        'MP3Downloads',
        'Magazines',
        'Miscellaneous',
        'Music',
        'MusicTracks',
        'MusicalInstruments',
        'MobileApps',
        'OfficeProducts',
        'OutdoorLiving',
        'PCHardware',
        'PetSupplies',
        'Photo',
        'Shoes',
        'Software',
        'SportingGoods',
        'Tools',
        'Toys',
        'UnboxVideo',
        'VHS',
        'Video',
        'VideoGames',
        'Watches',
        'Wireless',
        'WirelessAccessories'
    )

    keywords = (

    )



    def add_arguments(self, parser):
        parser.add_argument(
            '--keyword',
            '-k',
            dest='keyword',
            required=True,
            help='Keyword of the items on amazon'
        )

        parser.add_argument(
            '--index',
            '-i',
            dest='index',
            default= 'All',
            help='The search Index of the Items on amazon'
        )
        
    def fetch_amazon(self, keyword, index):
        print('fetching now from amazone....')

        if not index in self.SearchIndex:
            print('the given search index is not valide')

        if self.AWS_ACCESS_KEY_ID and self.AWS_SECRET_ACCESS_KEY and self.AWS_ASSOCIATE_TAG:
            amazon = AmazonAPI(self.AWS_ACCESS_KEY_ID, self.AWS_SECRET_ACCESS_KEY, self.AWS_ASSOCIATE_TAG)
            products = amazon.search(Keywords=keyword, SearchIndex=index)

            for p in products:
                product = Product()
                product.name = p.title
                product.description = p.discription
                product.price = p.price_and_currency
                product.is_published = False
                product.save()
        else:
            print('the amazon environement variables does not existes')

    
    def handle(self, *args, **options):
        keyword = options['keyword']
        index = options['index']

        self.fetch_amazon(keyword, index)
        
