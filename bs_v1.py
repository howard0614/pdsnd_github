#This is for assignment
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'satursday', 'sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #while cn in CITY_DATA
    cc = input("enter city name: ").lower()
    while CITY_DATA.get(cc) is None:
          print('----- 3 options only: chicago, new york or washington')
          cc = input("enter city name: ").lower()
    # get user input for month (all, january, february, ... , june)
    mm = input("enter month: ").lower()
    while mm not in MONTHS:
          print('INVALID INPUT')
          mm = input("enter month: ").lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    dd = input("enter day of week: ").lower()
    while dd not in DAYS:
          print('INVALID INPUT')
          dd = input("enter day of week: ").lower()

    print('-'*40)
    return cc, mm, dd

#def load_data(city, month, day):
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # use the index of the months list to get the corresponding int
    # filter by month to create the new dataframe
    if month != 'all':
       month = MONTHS.index(month) + 1
       df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
       df = df[df['day_of_week'] == day.title()]
        # filter by day of week to create the new dataframe

    row_index = 0
    while True:
        show_data = input("see 5 lines of raw data? (yes or no) ").lower()
        if show_data == 'yes':
            print(df.iloc[row_index:row_index + 5])
            row_index += 5
        elif show_data == 'no':
            break
        else:
            print("INVALID INPUT")

    print('-'*40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df_ss = df['month'].value_counts().keys()
    print('the most common month: ', int(df_ss[0]))
    # display the most common day of week
    df_dw = df['day_of_week'].value_counts().keys()
    print('the most common day of week: ',df_dw[0])
    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    df_hh = df['hour'].value_counts().keys()
    print('the most common start hour: ',int(df_hh[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    df_ss = df['Start Station'].value_counts().keys()
    print('the most commonly used station station: ',df_ss[0])
    # display most commonly used end station
    df_es = df['End Station'].value_counts().keys()
    print('the most commonly used station station: ',df_es[0])

    # display most frequent combination of start station and end station trip
    df_tp = df.filter(['Start Station', 'End Station']).value_counts().keys()
    print('the most frequent combination from start to end station: ',df_tp[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df_tt = df['Trip Duration'].sum() / 60 / 60 / 24
    print('total travel time: ', int(df_tt), 'days')

    # display mean travel time
    df_mt = np.mean(df['Trip Duration']) / 60
    print('mean travel time: ', int(df_mt), 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #if city != 'washington':
    df_ut = df.filter(['User Type']).value_counts()
    print('counts of user types: ', df_ut)
    print()

    #else:
    #   print('nothing')

    # Display counts of gender
    if 'Gender' in df:
       df_gd = df.filter(['Gender']).value_counts()
       print('counts of gender: ', df_gd)
    else:
       print('no gender data')
    print()
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
       df_el = int(min(df['Birth Year']))
       df_mr = int(max(df['Birth Year']))
       df_mc = df['Birth Year'].value_counts().keys()
       #df_mc = df_mc
       print('the earliest, most recent, and most common year of birth: {}, {}, and {}'.format(df_el, df_mr, int(df_mc[0])))
    else:
       print('no year of birth data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
           break

if __name__ == "__main__":
	main()
