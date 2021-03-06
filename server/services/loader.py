import os.path
from flask.json import jsonify, load
from collections import OrderedDict
import pandas as pd

# Class that will parse and return data from excel


class Loader:
    def __init__(self):
        pass

    #  function to get the sentimental data for the graph
    def get_sentimentals_of_all_airlines(self):
        pos = 0
        neg = 0
        neut = 0

        df = self._parse_csv()

        for sent in df['airline_sentiment']:
            if sent == 'positive':
                pos += 1
            if sent == 'negative':
                neg += 1
            if sent == 'neutral':
                neut += 1

        return {
            "optionsBar": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": 'Airlines Sentimental Analysis'
                    }
                }
            },
            "optionsDoughnut": {
                "plugins": {
                    "title": {
                        "display": True,
                        "text": 'Airlines Sentimental Analysis'
                    }
                }
            },
            "data": {
                "labels": ['Positive', 'Neutral', 'Negative'],
                "datasets": [
                    {
                        "label": 'Total',
                        "data": [pos, neut, neg],
                        "backgroundColor": [
                            'rgba(40, 158, 81, 0.8)',
                            'rgba(106, 121, 112, 0.36)',
                            'rgba(179, 35, 78, 0.36)',
                        ],
                        "borderColor": [
                            'rgba(40, 158, 81, 0.8)',
                            'rgba(106, 121, 112, 0.36)',
                            'rgba(179, 35, 78, 0.36)',
                        ],
                        "borderWidth": 1,
                    },
                ],
            }
        }

    # function to get airline count data
    # Will aggregrate the data set that is required for the chart
    def get_airline_count(self):
        df = self._parse_csv()

        airline_dict = {}
        data = []
        labels = []

        for airline in df['airline']:
            if airline not in airline_dict:
                airline_dict[airline] = 1
            else:
                airline_dict[airline] = airline_dict[airline] + 1

        for k, v in airline_dict.items():
            labels.append(k + ' Airlines')
            data.append(v)

        return {
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": 'Total',
                        "data": data,
                        "backgroundColor": 'rgba(255, 99, 132, 0.5)',
                    },
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "position": 'top',
                    },
                    "title": {
                        "display": True,
                        "text": 'Airline Counts',
                    },
                },
            }
        }

    

    # This function will keep count of the many different reasons why the tweet was considered a negative
    def get_null_values_from_all_columns(self):
        df = self._parse_csv()

        labels = []
        data = []

        null_counts = {}

        # looping through each column 
        # within each column iteration, looping through all values of that column (row)
        for col, row in df.items():
            null_counts[col] = 0
            for d in row:
                if pd.isna(d) or pd.isnull(d):
                    null_counts[col] = null_counts[col] + 1
        
                
        for k,v in null_counts.items():
            data.append(v)
            labels.append(k)

        return {
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": 'Total',
                        "data": data,
                        "backgroundColor": 'rgba(106, 121, 112, 0.36)',
                    },
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "position": 'top',
                    },
                    "title": {
                        "display": True,
                        "text": 'Null Values in Data set',
                    },
                },
            }
        }
    
    # This function will return the accuracy percentage for each of the Machine Learning models
    def get_accuracy_for_models(self):
        return {
            "data": {
                "labels": ['Logistic Regression', 'Support Vector Machine'],
                "datasets": [
                    {
                        "label": 'Percentage',
                        "data": ['90','94'],
                        "backgroundColor": ['#87CEFA','#F5F5DC'],
                    },
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "position": 'top',
                    },
                    "title": {
                        "display": True,
                        "text": 'Machine Learning Model Accuracy',
                    },
                },
            }
        }

    # This function will get the negative reason counts for each of the airlines
    def get_negative_reason_count(self):
        df = self._parse_csv()
        
        data = [int(df.negativereason.value_counts()[0]), int(df.negativereason.value_counts()[1]),
                int(df.negativereason.value_counts()[2]), int(df.negativereason.value_counts()[3]),
                int(df.negativereason.value_counts()[4]), int(df.negativereason.value_counts()[5]),
                int(df.negativereason.value_counts()[6]), int(df.negativereason.value_counts()[7]),
                int(df.negativereason.value_counts()[8]), int(df.negativereason.value_counts()[9])]

        labels = ['Customer Service Issue', 'Late Flight', "Can't Tell",'Cancelled Flight', 'Lost Luggage',
                  'Bad Flight', 'Flight Booking Problems','Flight Attendant Complaints',
                  'longlines', 'Damaged Luggage']

        return {
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": 'Total',
                        "data": data,
                        "backgroundColor": 'rgba(40, 158, 81, 0.8)',
                    },
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "position": 'top',
                    },
                    "title": {
                        "display": True,
                        "text": 'Negative Reasons Count',
                    },
                },
            }
        }
    
    # Get all the negative counts per category of a particular airline
    def get_negative_reason_count_per_airline(self,airline):
        # We want to loop through the rows of the csv
        df = self._parse_csv()
        # Filter out those that are not 'airline'
        # REFERENCE : https://cmdlinetips.com/2018/02/how-to-subset-pandas-dataframe-based-on-values-of-a-column/#:~:text=One%20way%20to%20filter%20by%20rows%20in%20Pandas,subset%20the%20dataframe%20based%20on%20year%E2%80%99s%20value%202002.
        filtered_cols = df[df.airline == airline]

        labels = []
        data = []

        negative_reasons = {}

        for reason in filtered_cols['negativereason']:
            if pd.isna(reason) or pd.isnull(reason):
                continue
            elif reason not in negative_reasons:
                negative_reasons[reason] = 1
            else:
                negative_reasons[reason] = negative_reasons[reason] + 1
        
        for k,v in sorted(negative_reasons.items()):
            labels.append(k)
            data.append(v)
        
        
        return {
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": 'Total',
                        "data": data,
                        "backgroundColor": ['#DEB887','#F0F8FF','#DA70D6','#708090','#20B2AA','#FFFAF0', '#4682B4', '#BC8F8F', '#F08080', '#87CEFA'],
                    },
                ],
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "position": 'top',
                    },
                    "title": {
                        "display": True,
                        "text": f'Negative reasons for {airline}',
                    },
                },
            }
        }



    # function to parse and return the data within the csv file
    def _parse_csv(self):
        return pd.read_csv(os.path.dirname(__file__) + '/../Tweets.csv') 


if __name__ == '__main__':

    loader = Loader()
    # print(loader.get_sentimentals_of_all_airlines())
    # print(loader.get_airline_count())
    # print(jsonify(loader.get_negative_reason_count()))
    print(loader.get_negative_reason_count_per_airline('Virgin America'))
