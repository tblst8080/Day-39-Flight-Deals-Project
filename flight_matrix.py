import pandas as pd
from sheetyAPI import Destination, Subscriber
from tequilaAPI import FlightSearch


class PriceMatrix:
    def __init__(self, dest_obj:Destination, sub_obj:Subscriber):
        self.dest_obj = dest_obj
        self.sub_obj = sub_obj
        self.df = pd.read_csv('destination-origin matrix.csv', index_col="Origin/Destination")

        self.destinations = [row['iataCode'] for row in self.dest_obj.content]
        self.origins = [row['iataCode'] for row in self.sub_obj.content]

        self.routes = []

    def fill_matrix(self):
        for destination in self.destinations:
            if destination not in self.df.columns.values:
                self.df[destination] = 500

        for origin in self.origins:
            if origin not in self.df.index.values:
                self.df.loc[origin] = [500 for item in self.df.columns.values]

        for column in self.df.columns.values:
            if column not in self.destinations:
                self.df.drop(columns=column, inplace=True)

        for row in self.df.index.values:
            if row not in self.origins:
                self.df.drop(index=row, inplace=True)

        self.df.to_csv('destination-origin matrix.csv')

    def generate_routes(self):
        for row in self.df.index.values:
            for column in self.df.columns.values:
                self.routes.append({'origin':row,
                                    'destination':column,
                                    'price':self.df.at[row, column]})





if __name__ == "__main__":
    my_destination = Destination()
    my_subscriptions = Subscriber()
    my_matrix = PriceMatrix(dest_obj=my_destination, sub_obj=my_subscriptions)
    my_matrix.fill_matrix()
    my_matrix.generate_routes()


    my_searcher = FlightSearch()
    for route in my_matrix.routes:
        my_searcher.lookup_flights(origin=route['origin'], destination=route['destination'], lowest_price=route['price'], stopovers=1)

